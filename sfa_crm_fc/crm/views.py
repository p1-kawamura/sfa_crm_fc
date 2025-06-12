from django.shortcuts import render
from django.shortcuts import render,redirect
from .models import Customer,Crm_action
from sfa.models import Sfa_data
from sfa.models import Member
import datetime
import calendar
import jpholiday
from django_pandas.io import read_frame
import json
import requests
from django.contrib.auth.decorators import login_required
from django.db.models import Max


def index(request):
    return render(request,"crm/index.html")


# アラート設定表
@login_required
def alert_index(request):
    if "alert_month" not in request.session:
        request.session["alert_month"]=datetime.datetime.now().strftime("%Y-%m")

    alert_month=request.session["alert_month"]
    y=int(alert_month[:4])
    m=int(alert_month[-2:])

    ins=calendar.monthrange(y,m)
    last_day=ins[1]

    alert_dic={}
    we_dic={0:"月",1:"火",2:"水",3:"木",4:"金",5:"土",6:"日",}
    for i in range(1,last_day+1):
        day=datetime.date(y,m,i)
        week=we_dic[day.weekday()]

        if jpholiday.is_holiday(day):
            week_color="2"
        elif week == "土":
            week_color="1"
        elif week == "日":
            week_color="2"
        else:
            week_color="0"

        alert_dic[day.strftime("%Y-%m-%d")]={"week":week,"week_color":week_color,"text_all":[]}

    tantou_id=request.session["tantou_id"]
    ins=Crm_action.objects.filter(tantou_id=tantou_id,type=6)
    for i in ins:
        if str(i.day[:7])==alert_month:
            cus=list(Customer.objects.filter(cus_id=i.cus_id).values())[0]
            dic={"text":i.text,"check":i.alert_check,"cus":cus}
            alert_dic[i.day]["text_all"].append(dic)
    
    # 操作者
    sousa_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sousa_busho=Member.objects.get(tantou_id=tantou_id).busho
    sousa_tantou=Member.objects.get(tantou_id=tantou_id).tantou
    act_user=Member.objects.get(tantou_id=tantou_id).tantou
    print(sousa_time,sousa_busho,sousa_tantou,"■ アラート設定表")


    params={
        "alert_month":alert_month,
        "act_user":act_user,
        "alert_dic":alert_dic,
        "today":datetime.date.today().strftime("%Y-%m-%d"),
        "modal_sort":request.session["modal_sort"],
    }

    return render(request,"crm/alert.html",params)


# アラート表_検索
def alert_search(request):
    request.session["alert_month"]=request.POST["alert_month"]
    return redirect("crm:alert_index")


# 顧客最終履歴
@login_required
def contact_index(request):
    if "contact_month" not in request.session:
        request.session["contact_month"]=datetime.datetime.now().strftime("%Y-%m")

    contact_month=request.session["contact_month"]
    y=int(contact_month[:4])
    m=int(contact_month[-2:])

    ins=calendar.monthrange(y,m)
    last_day=ins[1]

    contact_dic={}
    we_dic={0:"月",1:"火",2:"水",3:"木",4:"金",5:"土",6:"日",}
    for i in range(1,last_day+1):
        day=datetime.date(y,m,i)
        week=we_dic[day.weekday()]

        if jpholiday.is_holiday(day):
            week_color="2"
        elif week == "土":
            week_color="1"
        elif week == "日":
            week_color="2"
        else:
            week_color="0"

        contact_dic[day.strftime("%Y-%m-%d")]={"week":week,"week_color":week_color,"text_all":[]}

    tantou_id=request.session["tantou_id"]
    cus_act=set(Crm_action.objects.filter(tantou_id=tantou_id,type__in=[1,2,4,5]).values_list("cus_id",flat=True).order_by("cus_id").distinct())
    cus_est_all=list(Sfa_data.objects.filter(tantou_id=tantou_id).values_list("cus_id",flat=True).order_by("cus_id").distinct())
    cus_est_month=set(Customer.objects.filter(cus_id__in=cus_est_all,update_last_day__startswith=contact_month).values_list("cus_id",flat=True).order_by("cus_id").distinct())
    cus_list=list(cus_act | cus_est_month)
 
    for i in cus_list:
        ins=Customer.objects.get(cus_id=i)
        ins2=Sfa_data.objects.get(mitsu_num=ins.update_last_num,mitsu_ver=ins.update_last_ver)
        ins3=Crm_action.objects.filter(cus_id=i,type__in=[1,2,4,5]).order_by("day","act_id").reverse()
        
        dic={
            "cus_id":i,
            "cus_url":ins.cus_url,
            "cus_com":ins.com,
            "cus_sei":ins.sei,
            "cus_mei":ins.mei,
            "est_last":ins.update_last_day[:10],
            "est_status":ins2.s_status,
            "est_num":ins2.mitsu_num,
            "est_ver":ins2.mitsu_ver,
            "est_url":ins2.mitsu_url,
            "est_kubun":ins2.order_kubun,
            "est_money":ins2.money,
            }
        
        if ins3.count()==0:
            dic["day"]=ins.update_last_day[:10]

        elif max(ins3[0].day[:7],ins.update_last_day[:7])==contact_month:
            dic["day"]=max(ins3[0].day,ins.update_last_day[:10])
            dic["act_day"]=ins3[0].day
            dic["act_type"]=ins3[0].type
            dic["act_text"]=ins3[0].text

        else:
            continue

        contact_dic[dic["day"]]["text_all"].append(dic)

    
    # 操作者
    sousa_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sousa_busho=Member.objects.get(tantou_id=tantou_id).busho
    sousa_tantou=Member.objects.get(tantou_id=tantou_id).tantou
    act_user=Member.objects.get(tantou_id=tantou_id).tantou
    print(sousa_time,sousa_busho,sousa_tantou,"■ 顧客最終履歴")

    params={
        "contact_month":contact_month,
        "act_user":act_user,
        "contact_dic":contact_dic,
        "modal_sort":request.session["modal_sort"],
    }

    return render(request,"crm/contact.html",params)


# 顧客最終履歴_検索
def contact_search(request):
    request.session["contact_month"]=request.POST["contact_month"]
    return redirect("crm:contact_index")


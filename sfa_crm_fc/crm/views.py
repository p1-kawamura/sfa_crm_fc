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
    
    # アクティブ担当
    if tantou_id=="":
        act_user="担当者が未設定です"
    else:
        act_user=Member.objects.get(tantou_id=tantou_id).tantou

    # 操作者
    sousa_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        sousa_busho=Member.objects.get(tantou_id=tantou_id).busho
        sousa_tantou=Member.objects.get(tantou_id=tantou_id).tantou
        print(sousa_time,sousa_busho,sousa_tantou,"■ アラート設定表")
    except:
        print(sousa_time,"担当不明","■ アラート設定表")

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


# 顧客履歴
@login_required
def history_index(request):
    if "history" not in request.session:
        request.session["history"]={}
    if "his_st" not in request.session["history"]:
        request.session["history"]["his_st"]=""
    if "his_ed" not in request.session["history"]:
        request.session["history"]["his_ed"]=""

    ses=request.session["history"]
    tantou_id=request.session["tantou_id"]

    fil_1={}
    if ses["his_st"] != "":
        fil_1["make_day__gte"]=ses["his_st"]
    if ses["his_ed"] != "":
        fil_1["make_day__lte"]=ses["his_ed"]

    fil_2={}
    if ses["his_st"] != "":
        fil_2["day__gte"]=ses["his_st"]
    if ses["his_ed"] != "":
        fil_2["day__lte"]=ses["his_ed"]

    if len(fil_1)>0:
        df_sfa=set(Sfa_data.objects.filter(tantou_id=tantou_id,**fil_1).values_list("cus_id",flat=True).order_by("cus_id").distinct())
        df_act=set(Crm_action.objects.filter(tantou_id=tantou_id,**fil_2).values_list("cus_id",flat=True).order_by("cus_id").distinct())
        cus_list=list(df_sfa | df_act)
    else:
        cus_list=[]

    cus_history=[]
    for i in cus_list:

        # 顧客情報
        cus_det=list(Customer.objects.filter(cus_id=i).values())[0]

        # 見積
        res_est=[]
        ins=list(Sfa_data.objects.filter(cus_id=i,**fil_1).order_by("mitsu_id").values())
        for h in ins:
            dic={}
            dic["kubun"]="est"
            dic["day"]=h["make_day"]
            dic["detail"]=h
            res_est.append(dic)
        res_est.reverse()

        # コメント
        res_cmt=[]
        ins2=Crm_action.objects.filter(cus_id=i,**fil_2)
        for h in ins2:
            dic={}
            dic["kubun"]="act"
            dic["day"]=h.day
            dic["type"]=h.type
            dic["text"]=h.text
            res_cmt.append(dic)
        res_cmt.reverse()

        res_det=res_est + res_cmt

        # 並び替え
        res_det=sorted(res_det,key=lambda x: x["day"], reverse=True)

        cus_history.append({"cus":cus_det,"history":res_det})


    # アクティブ担当
    if tantou_id=="":
        act_user="担当者が未設定です"
    else:
        act_user=Member.objects.get(tantou_id=tantou_id).tantou

    # 操作者
    sousa_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        sousa_busho=Member.objects.get(tantou_id=tantou_id).busho
        sousa_tantou=Member.objects.get(tantou_id=tantou_id).tantou
        print(sousa_time,sousa_busho,sousa_tantou,"■ 顧客履歴")
    except:
        print(sousa_time,"担当不明","■ 顧客履歴")

    params={
        "cus_history":cus_history,
        "ses":ses,
        "act_user":act_user,
        "modal_sort":request.session["modal_sort"],
    }
    return render(request,"crm/history.html",params)


# 顧客履歴_検索
def history_search(request):
    request.session["history"]["his_st"]=request.POST["his_st"]
    request.session["history"]["his_ed"]=request.POST["his_ed"]
    return redirect("crm:history_index")
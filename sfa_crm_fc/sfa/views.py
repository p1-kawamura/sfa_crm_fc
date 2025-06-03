from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import Sfa_data,Member
from crm.models import Customer,Crm_action
import json
import requests
from datetime import date
import datetime
from django_pandas.io import read_frame
from django.contrib.auth.decorators import login_required



# APIデータ取得
@login_required
def index_api(request):
    tantou_id=request.session["tantou_id"]

    if tantou_id != "":
        
        last_api=Member.objects.get(tantou_id=tantou_id).last_api
        url="https://core-sys.p1-intl.co.jp/p1web/v1/estimations/?handledById=" + tantou_id + "&updatedAtFrom=" + last_api
        res=requests.get(url)
        res=res.json()
        res=res["estimations"]
        for i in res:
            ins=Sfa_data.objects.filter(mitsu_id=i["id"])
            if (ins.count()==0 and i["status"]=="終了") or i["customerId"]==None:
                continue
            
            # ------------------------
            # 案件
            # ------------------------
            Sfa_data.objects.update_or_create(
            mitsu_id=i["id"],
            defaults={
                "mitsu_id":i["id"],
                "mitsu_num":i["number"],
                "mitsu_ver":i["version"],
                "mitsu_url":i["estimationPageUrl"],
                "order_kubun":i["orderType"],
                "nouhin_kigen":i["deliveryLimitDate"],
                "nouhin_shitei":i["deliveryAppointedDate"],
                "make_day":i["createdAt"],
                "update_day":i["updatedAt"],
                "juchu_day":i["orderReceivedDate"],
                "hassou_day":i["shippedDate"],
                "cus_id":i["customerId"],
                "sei":i["ordererNameLast"],
                "mei":i["ordererNameFirst"],
                "com":i["ordererCorporateName"],
                "money":i["totalPrice"],
                "busho_id":i["handledDepartmentId"],
                "tantou_id":i["handledById"],
                "eye":0,
                }
            )
            # ステータス
            d={"見積中":"未","見積送信":"見","イメージ":"イ","受注":"受","発送完了":"発","キャンセル":"キ","終了":"終","保留":"保","":""}
            ins=Sfa_data.objects.get(mitsu_id=i["id"])
            ins.status=i["status"]
            ins.s_status=d[i["status"]]
            ins.save()


            # ------------------------
            # 顧客
            # ------------------------
            url2="https://core-sys.p1-intl.co.jp/p1web/v1/customers/" + str(i["customerId"])
            res2=requests.get(url2)
            res2=res2.json()

            tel_search=None
            if res2["tel"] != None:
                tel_search=res2["tel"].replace("-","")
            tel_mob_search=None
            if res2["mobilePhone"] != None:
                tel_mob_search=res2["mobilePhone"].replace("-","")
            
            try:
                ins=Customer.objects.get(cus_id=i["customerId"])
                update_last_day=ins.update_last_day
                update_last_num=ins.update_last_num
                update_last_ver=ins.update_last_ver
                if i["updatedAt"]>update_last_day:
                    update_last_day=i["updatedAt"]
                    update_last_num=i["number"]
                    update_last_ver=i["version"]
                else:
                    update_last_day=update_last_day
                    update_last_num=update_last_num
                    update_last_ver=update_last_ver
            except:
                update_last_day=i["updatedAt"]
                update_last_num=i["number"]
                update_last_ver=i["version"]
 
            Customer.objects.update_or_create(
            cus_id=res2["id"],
            defaults={
                "cus_id":res2["id"],
                "cus_url":res2["customerMstPageUrl"],
                "cus_touroku":res2["createdAt"],
                "com":res2["corporateName"],
                "com_busho":res2["departmentName"],
                "sei":res2["nameLast"],
                "mei":res2["nameFirst"],
                "pref":res2["prefecture"],
                "city":res2["city"],
                "address_1":res2["address1"],
                "address_2":res2["address2"],
                "tel":res2["tel"],
                "tel_search":tel_search,
                "tel_mob":res2["mobilePhone"],
                "tel_mob_search":tel_mob_search,
                "mail":res2["contactEmail"],
                "mitsu_all":res2["totalEstimations"],
                "juchu_all":res2["totalReceivedOrders"],
                "juchu_money":res2["totalReceivedOrdersPrice"],
                "mitsu_last":res2["lastEstimatedAt"],
                "juchu_last":res2["lastOrderReceivedDate"],
                "update_last_day":update_last_day,
                "update_last_num":update_last_num,
                "update_last_ver":update_last_ver,
                "mitsu_last_busho_id":res2["lastHandledDepartmentId"],
                "mitsu_last_busho":res2["lastHandledDepartmentName"],
                "mitsu_last_tantou_id":res2["lastHandledId"],
                "mitsu_last_tantou":res2["lastHandledName"],
                "taimen":res2["isVisited"],
                }
            )

        # API取得日時
        ins=Member.objects.get(tantou_id=tantou_id)
        ins.last_api=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ins.save()

    return redirect("sfa:index")


# TOPページ表示
@login_required
def index(request):
    if "busho_id" not in request.session:
        request.session["busho_id"]=""
    if "tantou_id" not in request.session:
        request.session["tantou_id"]=""
    if "modal_sort" not in request.session:
        request.session["modal_sort"]="1"

    if "search" not in request.session:
        request.session["search"]={}
    if "com" not in request.session["search"]:
        request.session["search"]["com"]=""
    if "cus_sei" not in request.session["search"]:
        request.session["search"]["cus_sei"]=""
    if "cus_mei" not in request.session["search"]:
        request.session["search"]["cus_mei"]=""
    if "page_num" not in request.session["search"]:
        request.session["search"]["page_num"]=1
    if "all_page_num" not in request.session["search"]:
        request.session["search"]["all_page_num"]=""
    
    
    ses=request.session["search"]
    
    # ユーザー情報
    busho_id=request.user.username
    tantou_id=request.session["tantou_id"]
    busho_name=Member.objects.filter(busho_id=busho_id)[0].busho
    request.session["busho_id"]=busho_id

    # アクティブ担当
    if tantou_id=="":
        act_user="担当者が未設定です"
    else:
        act_user=Member.objects.get(tantou_id=tantou_id).tantou

    # フィルター
    fil={}
    fil["show"]=0
    fil["tantou_id"]=tantou_id
    
    flag=False
    if ses["com"] != "":
        fil["com__contains"]=ses["com"].strip()
        flag=True
    if ses["cus_sei"] != "":
        fil["sei__contains"]=ses["cus_sei"].strip()
        flag=True
    if ses["cus_mei"] != "":
        flag=True
        fil["mei__contains"]=ses["cus_mei"].strip()
    
    ins=Sfa_data.objects.filter(**fil)
    sfa_list=[]
    alert_all=0

    if tantou_id != "":
        # 検索なし
        if flag==False:
            df=read_frame(Sfa_data.objects.filter(tantou_id=tantou_id))
        # 検索あり
        else:
            df=read_frame(ins.filter(tantou_id=tantou_id))

        today=str(date.today())
        alert_list=list(Crm_action.objects.filter(type=6,alert_check=0,day__lte=today).values_list("cus_id",flat=True).order_by("cus_id").distinct())
        alert_set=list(Crm_action.objects.filter(type=6,alert_check=0,day__gt=today).values_list("cus_id",flat=True).order_by("cus_id").distinct())
        df["alert"]=df["cus_id"].isin(alert_list)

        df.sort_values(by=["alert","update_day"],ascending=[False,False],inplace=True)
        df.drop_duplicates("cus_id",inplace=True)
        parent_list=df["cus_id"].to_list()
        
        for i in parent_list:
            ins_parent=list(Customer.objects.filter(cus_id=i).values())[0]
            ins_child=list(ins.filter(cus_id=i).values().order_by("make_day").reverse())

            # ステータス
            st_list=["未","見","イ","受","発","終"]
            st_dic={}
            for h in st_list:
                st_dic[h]=ins.filter(cus_id=i,s_status=h).count()
            ins_parent["status_count"]=st_dic

            # アラート発生
            if i in alert_list:
                ins_parent["alert"]=1
                alert_all +=1
            else:
                ins_parent["alert"]=0

            # アラート設定中
            if i in alert_set:
                ins_parent["alert_set"]=1
            else:
                ins_parent["alert_set"]=0

            # オープン
            ins_parent["eye_count_0"]=ins.filter(cus_id=i,eye=0).count()
            ins_parent["eye_count_1"]=ins.filter(cus_id=i,eye=1).count()

            dic={"parent":ins_parent,"child":ins_child}
            sfa_list.append(dic)

    # ページネーション
    result=len(sfa_list)
    if result == 0:
        all_num = 1
    elif result % 30 == 0:
        all_num = result / 30
    else:
        all_num = result // 30 + 1
    all_num=int(all_num)
    request.session["search"]["all_page_num"]=all_num
    num=ses["page_num"]
    if all_num==1:
        num=1
        request.session["search"]["page_num"]=1

    sfa_list=sfa_list[(num-1)*30 : num*30]

    # その他情報
    tantou_list=Member.objects.filter(busho_id=busho_id)
    modal_sort=request.session["modal_sort"]

    params={
        "tantou_id":tantou_id,
        "sfa_list":sfa_list,
        "busho_name":busho_name,
        "tantou_list":tantou_list,
        "ses":ses,
        "modal_sort":modal_sort,
        "alert_all":alert_all,
        "num":num,
        "all_num":all_num,
        "act_user":act_user,
    }
    return render(request,"sfa/index.html",params)


# 案件表示/検索
def sfa_search(request):
    request.session["tantou_id"]=request.POST["tantou_id"]
    request.session["search"]["com"]=request.POST["com"]
    request.session["search"]["cus_sei"]=request.POST["cus_sei"]
    request.session["search"]["cus_mei"]=request.POST["cus_mei"]
    request.session["search"]["page_num"]=1
    return redirect("sfa:index")


# 案件のオープン表示
def open_eye(request):
    mitsu_id=request.POST.get("mitsu_id")
    ins=Sfa_data.objects.get(mitsu_id=mitsu_id)
    if ins.eye==0:
        ins.eye=1
    else:
        ins.eye=0
    ins.save()
    d={"eye":ins.eye}
    return JsonResponse(d)


# 案件の非表示
def show_hidden(request):
    mitsu_id=request.POST.get("mitsu_id")
    ins=Sfa_data.objects.get(mitsu_id=mitsu_id)
    ins.show=1
    ins.hidden_day=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ins.save()
    d={}
    return JsonResponse(d)


# モーダルで詳細表示
def cus_modal_show(request):
    cus_id=request.POST.get("cus_id")
    cus_info=list(Customer.objects.filter(cus_id=cus_id).values())[0]
    today=str(date.today())
    ins=list(Crm_action.objects.filter(cus_id=cus_id,type=6,alert_check=0,day__lte=today).values())
    if len(ins)>0:
        alert={"set":1,"act_id":ins[0]["act_id"],"text":ins[0]["text"]}
    else:
        alert={"set":0}

    modal_sort=request.session["modal_sort"]
    res_det=modal_act_list(cus_id,modal_sort)

    d={"cus_info":cus_info,"res_det":res_det,"alert":alert}
    return JsonResponse(d)



# モーダルの備考内容
def cus_modal_bikou(request):
    cus_id=request.POST.get("cus_id")
    bikou=request.POST.get("bikou")
    ins=Customer.objects.get(cus_id=cus_id)
    try:
        ins.bikou=bikou
        ins.save()
        res="ok"
    except:
        res="error"
    d={"res":res}
    return JsonResponse(d)


# モーダル下部（TEL、メール、メモ、来店、外商、アラート）
def cus_modal_bot(request):
    act_id=request.POST.get("act_id")
    cus_id=request.POST.get("cus_id")
    day=request.POST.get("day")
    type=request.POST.get("type")
    text=request.POST.get("text")
    tantou_id=modal_sort=request.session["tantou_id"]
    modal_sort=request.session["modal_sort"]

    try:
        if act_id =="":
            Crm_action.objects.create(cus_id=cus_id,tantou_id=tantou_id,day=day,type=type,text=text)
        else:
            ins=Crm_action.objects.get(act_id=act_id)
            ins.day=day
            ins.type=type
            ins.text=text
            ins.save()

        res_det=modal_act_list(cus_id,modal_sort)
        
    except:
        res_det="error"

    d={"res_det":res_det}
    return JsonResponse(d)


# FUNC モーダルの履歴一覧
def modal_act_list(cus_id,modal_sort):
    res_est=[]
    res_cmt=[]

    # 見積
    url="https://core-sys.p1-intl.co.jp/p1web/v1/customers/" + cus_id + "/receivedOrders"
    res=requests.get(url)
    res=res.json()
    res=res["receivedOrders"]
    for i in res:        
        dic={}
        dic["kubun"]="est"
        dic["day"]=i["firstEstimationDate"]
        dic["est_num"]=i["estimationNumber"] + "-" + str(i["estimationVersion"])
        dic["status"]=i["estimationStatus"]
        dic["money"]=i["totalPrice"]
        dic["tantou"]=i["handledByName"]
        res_est.append(dic)
    if modal_sort=="0":
        res_est.reverse()

    # コメント
    ins=Crm_action.objects.filter(cus_id=cus_id)
    for i in ins:
        dic={}
        dic["kubun"]="act"
        dic["day"]=i.day
        dic["type"]=i.type
        dic["text"]=i.text
        dic["act_id"]=i.act_id
        res_cmt.append(dic)
    if modal_sort=="1":
        res_cmt.reverse()

    res_det=res_est + res_cmt

    # 並び替え
    if modal_sort=="0":
        res_det=sorted(res_det,key=lambda x: x["day"])
    else:
        res_det=sorted(res_det,key=lambda x: x["day"], reverse=True)

    return res_det


# モダール履歴リストクリック
def cus_modal_list_click(request):
    act_id=request.POST.get("act_id")
    ins=Crm_action.objects.get(act_id=act_id)
    res={"type":ins.type,"day":ins.day,"text":ins.text}
    d={"res":res}
    return JsonResponse(d)


# モーダル下部_削除
def cus_modal_bot_del(request):
    act_id=request.POST.get("act_id")
    cus_id=request.POST.get("cus_id")
    modal_sort=request.session["modal_sort"]
    Crm_action.objects.get(act_id=act_id).delete()
    res_det=modal_act_list(cus_id,modal_sort)
    d={"res_det":res_det}
    return JsonResponse(d)


# モーダル履歴_表示順
def cus_modal_sort(request):
    jun=request.POST.get("jun")
    cus_id=request.POST.get("cus_id")
    request.session["modal_sort"]=jun
    res_det=modal_act_list(cus_id,jun)
    d={"res_det":res_det}
    return JsonResponse(d)


# モーダル_アラート解除
def modal_alert_check(request):
    alert_num=request.POST.get("alert_num")
    ins=Crm_action.objects.get(act_id=alert_num)
    ins.alert_check=1
    ins.save()
    d={}
    return JsonResponse(d)


# ページネーション（前）
def sfa_page_prev(request):
    num=request.session["search"]["page_num"]
    if num-1 > 0:
        request.session["search"]["page_num"] = num - 1
    return redirect("sfa:index")


# ページネーション（最初）
def sfa_page_first(request):
    request.session["search"]["page_num"] = 1
    return redirect("sfa:index")


# ページネーション（次）
def sfa_page_next(request):
    num=request.session["search"]["page_num"]
    all_num=request.session["search"]["all_page_num"]
    if num+1 <= all_num:
        request.session["search"]["page_num"] = num + 1
    return redirect("sfa:index")


# ページネーション（最後）
def sfa_page_last(request):
    all_num=request.session["search"]["all_page_num"]
    request.session["search"]["page_num"]=all_num
    return redirect("sfa:index")


# 非表示一覧の表示
@login_required
def hidden_index(request):
    if "hidden" not in request.session:
        request.session["hidden"]={}
    if "mitsu_num" not in request.session["hidden"]:
        request.session["hidden"]["mitsu_num"]=""
    if "com" not in request.session["hidden"]:
        request.session["hidden"]["com"]=""
    if "cus_sei" not in request.session["hidden"]:
        request.session["hidden"]["cus_sei"]=""
    if "cus_mei" not in request.session["hidden"]:
        request.session["hidden"]["cus_mei"]=""

    tantou_id=request.session["tantou_id"]
    ses=request.session["hidden"]

    fil={}
    fil["show"]=1
    fil["tantou_id"]=tantou_id
    if ses["mitsu_num"] != "":
        fil["mitsu_num"]=ses["mitsu_num"].strip()
    if ses["com"] != "":
        fil["com__contains"]=ses["com"].strip()
    if ses["cus_sei"] != "":
        fil["sei__contains"]=ses["cus_sei"].strip()
    if ses["cus_mei"] != "":
        fil["mei__contains"]=ses["cus_mei"].strip()
    
    ins=Sfa_data.objects.filter(**fil).order_by("hidden_day").reverse()[:300] #直近300件

    # アクティブ担当
    if tantou_id=="":
        act_user="担当者が未設定です"
    else:
        act_user=Member.objects.get(tantou_id=tantou_id).tantou

    params={
        "list":ins,
        "act_user":act_user,
        "ses":ses,
    }
    return render(request,"sfa/hidden.html",params)


# 非表示一覧の検索
def hidden_search(request):
    request.session["hidden"]["mitsu_num"]=request.POST["mitsu_num"]
    request.session["hidden"]["com"]=request.POST["com"]
    request.session["hidden"]["cus_sei"]=request.POST["cus_sei"]
    request.session["hidden"]["cus_mei"]=request.POST["cus_mei"]
    return redirect("sfa:hidden_index")


# 非表示一覧から再表示
def hidden_to_show(request):
    hidden_list=request.POST.get("hidden_list")
    hidden_list=json.loads(hidden_list)
    for i in hidden_list:
        ins=Sfa_data.objects.get(mitsu_id=i)
        ins.show=0
        ins.hidden_day=""
        ins.save()
    d={}
    return JsonResponse(d)












# 自由に使うため
def free(request):

    # ins=Sfa_data.objects.all()
    # for i in ins:
    #     i.show=0
    #     i.save()

    # Sfa_data.objects.all().delete()
    # Customer.objects.all().delete()
    Crm_action.objects.all().delete()

    return redirect("sfa:index")
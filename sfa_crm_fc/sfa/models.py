from django.db import models

class Sfa_data(models.Model):
    mitsu_id=models.CharField("見積ID",max_length=255,unique=True)
    mitsu_num=models.CharField("見積番号",max_length=255)
    mitsu_ver=models.CharField("見積バージョン",max_length=255)
    mitsu_url=models.CharField("見積URL",max_length=255,blank=True,null=True)
    status=models.CharField("ステータス",max_length=255,blank=True,null=True)
    order_kubun=models.CharField("注文区分",max_length=255,blank=True,null=True)
    nouhin_kigen=models.CharField("納品期限日",max_length=255,blank=True,null=True)
    nouhin_shitei=models.CharField("納品指定日",max_length=255,blank=True,null=True)
    make_day=models.CharField("見積作成日",max_length=255,blank=True)
    update_day=models.CharField("更新日",max_length=255,blank=True)
    juchu_day=models.CharField("受注日",max_length=255,blank=True,null=True)
    hassou_day=models.CharField("発送完了日",max_length=255,blank=True,null=True)
    cus_id=models.CharField("顧客ID",max_length=255,blank=True,null=True)
    sei=models.CharField("姓",max_length=255,blank=True,null=True)
    mei=models.CharField("名",max_length=255,blank=True,null=True)
    com=models.CharField("会社名",max_length=255,blank=True,null=True)
    money=models.IntegerField("金額",blank=True,null=True)
    busho_id=models.CharField("部署ID",max_length=255)
    tantou_id=models.CharField("担当ID",max_length=255)
    show=models.IntegerField("案件表示",default=0)
    eye=models.IntegerField("オープン表示",default=0)
    hidden_day=models.CharField("非表示日時",max_length=255,blank=True,default="")
    s_status=models.CharField("s_ステータス",max_length=255,blank=True,null=True)

    def __str__(self):
        return self.mitsu_id
    
    # show（案件表示） 0:表示　1：非表示
    # eye（オープン表示） 0:表示　1：非表示




class Member(models.Model):
    busho=models.CharField("部署",max_length=255,blank=True,null=True)
    busho_id=models.CharField("部署ID",max_length=255,blank=True,null=True)
    tantou=models.CharField("担当",max_length=255,blank=True,null=True)
    tantou_id=models.CharField("担当ID",max_length=255,blank=True,null=True)
    last_api=models.CharField("最終API接続",max_length=255,blank=True)

    def __str__(self):
        return self.tantou_id

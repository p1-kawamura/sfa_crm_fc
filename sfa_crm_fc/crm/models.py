from django.db import models

class Customer(models.Model):
    cus_id=models.CharField("顧客ID",max_length=10,unique=True)
    cus_url=models.CharField("顧客URL",max_length=255,blank=True,null=True)
    cus_touroku=models.CharField("顧客登録日",max_length=255,blank=True,null=True)
    com=models.CharField("会社名",max_length=255,blank=True,null=True)
    com_busho=models.CharField("部課名",max_length=255,blank=True,null=True)
    sei=models.CharField("姓",max_length=255,blank=True,null=True)
    mei=models.CharField("名",max_length=255,blank=True,null=True)
    pref=models.CharField("都道府県",max_length=255,blank=True,null=True)
    city=models.CharField("市区町村",max_length=255,blank=True,null=True)
    address_1=models.CharField("番地",max_length=255,blank=True,null=True)
    address_2=models.CharField("建物名",max_length=255,blank=True,null=True)
    tel=models.CharField("電話番号",max_length=255,blank=True,null=True)
    tel_search=models.CharField("電話番号_検索",max_length=255,blank=True,null=True)
    tel_mob=models.CharField("携帯番号",max_length=255,blank=True,null=True)
    tel_mob_search=models.CharField("携帯番号_検索",max_length=255,blank=True,null=True)
    mail=models.CharField("メール",max_length=255,blank=True,null=True)
    juchu_all=models.IntegerField("受注総数",default=0)
    juchu_money=models.BigIntegerField("受注総金額",default=0)
    update_last_day=models.CharField("最終更新日",max_length=255,blank=True,null=True)
    update_last_num=models.CharField("最終更新_見積番号",max_length=255,blank=True,null=True)
    update_last_ver=models.CharField("最終更新_バージョン",max_length=255,blank=True,null=True)

    def __str__(self):
        return self.cus_id
    


class Crm_action(models.Model):
    act_id=models.AutoField("行動ID",primary_key=True)
    cus_id=models.CharField("顧客ID",max_length=10)
    tantou_id=models.CharField("担当ID",max_length=10)
    day=models.CharField("日付",max_length=10)
    type=models.IntegerField("種類",null=False)
    text=models.TextField("内容",blank=True)
    alert_check=models.IntegerField("アラート",default=0)

    def __str__(self):
        return self.cus_id
    
    # type（種類） 1:TEL　 2：メール　 3：メモ　4：来店　5：外商　6：アラート
           


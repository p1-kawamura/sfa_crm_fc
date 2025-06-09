from django.contrib import admin
from .models import Customer,Crm_action
from django.contrib.admin import ModelAdmin

class A_Customer(ModelAdmin):
    model=Customer
    list_display = ["cus_id","sei","mei"]
    search_fields=("cus_id")

class A_Crm_action(ModelAdmin):
    model=Crm_action
    list_display = ["act_id","cus_id","tantou_id","day","type","text","alert_check"]
    search_fields=("cus_id")


admin.site.register(Customer,A_Customer)
admin.site.register(Crm_action,A_Crm_action)

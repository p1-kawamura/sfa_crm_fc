from django.contrib import admin
from .models import Sfa_data,Member
from django.contrib.admin import ModelAdmin

class A_Sfa_data(ModelAdmin):
    model=Sfa_data
    list_display = ["tantou_id","mitsu_num","mitsu_ver","sei","mei","juchu_day"]

class A_Member(ModelAdmin):
    model=Member
    list_display = ["busho_id","busho","tantou_id","tantou","last_api"]


admin.site.register(Sfa_data,A_Sfa_data)
admin.site.register(Member,A_Member)

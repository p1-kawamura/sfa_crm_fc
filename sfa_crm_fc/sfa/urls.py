from django.urls import path
from django.contrib.auth import views as auth_views
from .views import index_api,index,sfa_search,open_eye,show_hidden,cus_modal_show,cus_modal_bikou,cus_modal_bot,cus_modal_list_click, \
                    cus_modal_bot_del,cus_modal_sort,modal_alert_check,hidden_index,hidden_search,hidden_to_show,\
                    sfa_page_prev,sfa_page_first,sfa_page_next,sfa_page_last,free
                    



app_name="sfa"
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='sfa/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', index, name="index"),
    path('index_api/', index_api, name="index_api"),
    path('sfa_search/', sfa_search, name="sfa_search"),
    path('sfa_page_prev/', sfa_page_prev, name="sfa_page_prev"),
    path('sfa_page_first/', sfa_page_first, name="sfa_page_first"),
    path('sfa_page_next/', sfa_page_next, name="sfa_page_next"),
    path('sfa_page_last/', sfa_page_last, name="sfa_page_last"),
    path('open_eye/', open_eye, name="open_eye"),
    path('show_hidden/', show_hidden, name="show_hidden"),
    path('cus_modal_show/', cus_modal_show, name="cus_modal_show"),
    path('cus_modal_bikou/', cus_modal_bikou, name="cus_modal_bikou"),
    path('cus_modal_bot/', cus_modal_bot, name="cus_modal_bot"),
    path('cus_modal_bot_del/', cus_modal_bot_del, name="cus_modal_bot_del"),
    path('cus_modal_list_click/', cus_modal_list_click, name="cus_modal_list_click"),
    path('cus_modal_sort/', cus_modal_sort, name="cus_modal_sort"),
    path('modal_alert_check/', modal_alert_check, name="modal_alert_check"),
    path('hidden_index/', hidden_index, name="hidden_index"),
    path('hidden_search/', hidden_search, name="hidden_search"),
    path('hidden_to_show/', hidden_to_show, name="hidden_to_show"),
    path('free/', free, name="free"),
]
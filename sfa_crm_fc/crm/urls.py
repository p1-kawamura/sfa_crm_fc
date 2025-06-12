from django.urls import path
from .views import index,alert_index,alert_search,contact_index,contact_search,history_index,history_search

app_name="crm"
urlpatterns = [
    path('', index, name="index"),
    path('alert_index/', alert_index, name="alert_index"),
    path('alert_search/', alert_search, name="alert_search"),
    path('contact_index/', contact_index, name="contact_index"),
    path('contact_search/', contact_search, name="contact_search"),
    path('history_index/', history_index, name="history_index"),
    path('history_search/', history_search, name="history_search"),
]
from django.urls import path
from .views import index,alert_index,alert_search,contact_index,contact_search

app_name="crm"
urlpatterns = [
    path('', index, name="index"),
    path('alert_index/', alert_index, name="alert_index"),
    path('alert_search/', alert_search, name="alert_search"),
    path('contact_index/', contact_index, name="contact_index"),
    path('contact_search/', contact_search, name="contact_search"),
]
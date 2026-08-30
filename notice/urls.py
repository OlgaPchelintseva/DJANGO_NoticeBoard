from django.urls import path
from . import views

app_name = 'notice'
urlpatterns = [
    path('', views.notice_list, name='notice_list'),
    path('notice/<int:notice_id>/', views.notice_detail, name='notice_details'),
]
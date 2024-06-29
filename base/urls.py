from django.urls import path
from . import views
urlpatterns = [
    path('login', views.login, name="login"),
    path("forgot-password", views.forgot_password_view, name="forgot_password"),
    path("reset-password/<str:token>", views.reset_password_view, name="reset_password"),
    path("change-password/<str:pk>", views.change_password, name="change_password"),
    path("reset-password", views.reset_password_for_admin, name="reset_password"),
    path("update-account", views.update_account, name="update_account"),
    path('update_info/<str:pk>/', views.update_infor, name='update_info'),
    path('thongbao/', views.thongbao_list_create, name='thongbao_list_create'),
    path('thongbao/<str:pk>/', views.thongbao_detail, name='thongbao_detail'),
]
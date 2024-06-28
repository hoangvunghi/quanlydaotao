from django.urls import path
from . import views
urlpatterns = [
    path('login', views.login, name="login"),
    path("forgot-password", views.forgot_password_view, name="forgot_password"),
    path("reset-password/<str:token>", views.reset_password_view, name="reset_password"),

]
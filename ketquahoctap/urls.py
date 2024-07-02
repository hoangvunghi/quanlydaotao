from django.urls import path
from . import views
urlpatterns = [
    path('ketquahoctap', views.ketquahoctap_list_create, name='ketquahoctap_list_create'),
    path('ketquahoctap/<str:pk>', views.ketquahoctap_detail, name='ketquahoctap_detail'),
    path("cap-nhat-diem-qua-trinh/<str:pk>", views.cap_nhat_diem_qua_trinh, name="cap_nhat_diem_qua_trinh"),
]
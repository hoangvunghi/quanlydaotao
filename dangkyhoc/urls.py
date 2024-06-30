from django.urls import path
from . import views
urlpatterns = [
    path('monhoc', views.monhoc_list_create, name='monhoc_list_create'),
    path('monhoc/<str:pk>', views.monhoc_detail, name='monhoc_detail'),
    path('dieukientienquyet', views.dieukientienquyet_list_create, name='dieukientienquyet_list_create'),
    path('dieukientienquyet/<str:pk>', views.dieukientienquyet_detail, name='dieukientienquyet_detail'),
]
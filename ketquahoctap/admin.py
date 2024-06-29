from django.contrib import admin
from .models import KetQuaHocTap

@admin.register(KetQuaHocTap)
class KetQuaHocTapAdmin(admin.ModelAdmin):
    list_display = ('ID', 'MaSinhVien', 'MaMon', 'DiemQuaTrinh', 'DiemThi', 'DiemTongKet', 'DiemChu', 'HocKy', 'NamHoc', 'Status')
    search_fields = ('MaSinhVien__Ten', 'MaMon__TenMon', 'HocKy', 'NamHoc', 'Status')
    list_filter = ('HocKy', 'NamHoc', 'Status')
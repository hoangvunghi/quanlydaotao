from django.contrib import admin
from .models import KetQuaHocTap, HeSoMonHoc

@admin.register(KetQuaHocTap)
class KetQuaHocTapAdmin(admin.ModelAdmin):
    list_display = ('ID', 'MaSinhVien', 'MaMon', 'DiemQuaTrinh', 'DiemThi', 'DiemTongKet', 'DiemChu', 'HocKy', 'NamHoc', 'Status')
    search_fields = ('MaSinhVien__Ten', 'MaMon__TenMon', 'HocKy', 'NamHoc', 'Status')
    list_filter = ('HocKy', 'NamHoc', 'Status')
@admin.register(HeSoMonHoc)
class HeSoMonHocAdmin(admin.ModelAdmin):
    list_display = ('ID', 'MaMon', 'HeSoDiemQuaTrinh', 'HeSoTongKet', 'HeSoKN1', 'HeSoKN2', 'HeSoKN3', 'HeSoKN4', 'HeSoTongKetKN1', 'HeSoTongKetKN2', 'HeSoTongKetKN3', 'HeSoTongKetKN4')
    search_fields = ('MaMon__TenMon',)
    list_filter = ('HeSoDiemQuaTrinh', 'HeSoTongKet')
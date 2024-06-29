from django.contrib import admin
from .models import MonHoc, DieuKienTienQuyet, DangKyHocPhan, KetQuaDangKy

@admin.register(MonHoc)
class MonHocAdmin(admin.ModelAdmin):
    list_display = ('MaMon', 'TenMon', 'SoTinChi', 'SoTietLyThuyet', 'SoTietThucHanh', 'MaKhoa', 'Status', 'HeSo')
    search_fields = ('MaMon', 'TenMon', 'MaKhoa__TenKhoa', 'Status')
    list_filter = ('SoTinChi', 'MaKhoa', 'Status')

@admin.register(DieuKienTienQuyet)
class DieuKienTienQuyetAdmin(admin.ModelAdmin):
    list_display = ('ID', 'MaMon', 'MaMonTienQuyet')
    search_fields = ('MaMon__TenMon', 'MaMonTienQuyet__TenMon')
    list_filter = ('MaMon', 'MaMonTienQuyet')

@admin.register(DangKyHocPhan)
class DangKyHocPhanAdmin(admin.ModelAdmin):
    list_display = ('MaLopHocPhan', 'GioHoc', 'PhongHoc', 'MaGiangVien', 'SoLuongToiDa', 'Status', 'Loai', 'MaMon', 'MaLopLyThuyet')
    search_fields = ('MaLopHocPhan', 'MaGiangVien__TenGiangVien', 'MaMon__TenMon', 'Loai')
    list_filter = ('Status', 'Loai', 'MaGiangVien', 'MaMon')

@admin.register(KetQuaDangKy)
class KetQuaDangKyAdmin(admin.ModelAdmin):
    list_display = ('ID', 'MaSinhVien', 'MaLopHocPhan', 'NamHoc', 'HocKy')
    search_fields = ('MaSinhVien__TenSinhVien', 'MaLopHocPhan__MaLopHocPhan', 'NamHoc')
    list_filter = ('NamHoc', 'HocKy')
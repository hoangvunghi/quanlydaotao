from django.contrib import admin
from .models import Khoa, GiangVien, Lop, SinhVien, UserAccount, ThongBao

@admin.register(Khoa)
class KhoaAdmin(admin.ModelAdmin):
    list_display = ('MaKhoa', 'TenKhoa', 'created_at', 'updated_at')
    search_fields = ('MaKhoa', 'TenKhoa')

@admin.register(GiangVien)
class GiangVienAdmin(admin.ModelAdmin):
    list_display = ('MaGV', 'HoTen', 'DienThoai', 'Email', 'MaKhoa', 'GioiTinh', 'Role', 'Status', 'created_at', 'updated_at')
    search_fields = ('MaGV', 'HoTen', 'Email', 'MaKhoa__TenKhoa')

@admin.register(Lop)
class LopAdmin(admin.ModelAdmin):
    list_display = ('MaLop', 'MaKhoa', 'MaGV', 'created_at', 'updated_at')
    search_fields = ('MaLop', 'MaKhoa__TenKhoa', 'MaGV__HoTen')

@admin.register(SinhVien)
class SinhVienAdmin(admin.ModelAdmin):
    list_display = ('Msv', 'Ten', 'NgaySinh', 'GioiTinh', 'CCCD', 'MaLop', 'Email', 'DienThoai', 'Status', 'MaKhoa', 'MaGiangVien', 'HinhThucDaoTao', 'Role', 'created_at', 'updated_at')
    search_fields = ('Msv', 'Ten', 'CCCD', 'Email', 'MaLop', 'MaKhoa__TenKhoa', 'MaGiangVien__HoTen')

@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'UserStatus', 'is_staff', 'last_login', 'created_at', 'updated_at')
    search_fields = ('username', 'email')

@admin.register(ThongBao)
class ThongBaoAdmin(admin.ModelAdmin):
    list_display = ('MaTB', 'MaGV', 'MaLop', 'TieuDe', 'NoiDung', 'NgayDang', 'LoaiTB', 'Status', 'created_at', 'updated_at')
    search_fields = ('MaTB', 'TieuDe', 'MaGV__HoTen', 'MaLop__MaLop')
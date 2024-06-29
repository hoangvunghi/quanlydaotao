from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

class ModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, editable=False,
                                   related_name='%(class)s_created', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, editable=False,
                                   related_name='%(class)s_updated', on_delete=models.CASCADE)
    objects = ModelManager()

    class Meta:
        abstract = True

class Khoa(BaseModel):  
    MaKhoa = models.CharField(max_length=50, unique=True)
    TenKhoa = models.CharField(max_length=100)
    class Meta:
        verbose_name = "Khoa"
        verbose_name_plural = "Khoa"


class GiangVien(BaseModel):  
    UserAccount = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    MaGV = models.CharField(max_length=50, unique=True,primary_key=True) 
    HoTen = models.CharField(max_length=100)
    DienThoai = models.CharField(max_length=20)
    Email = models.EmailField()
    MaKhoa = models.ForeignKey(Khoa, on_delete=models.SET_NULL, null=True, blank=True)
    Avatar = models.ImageField(upload_to='avatar/', default='default.jpg')
    GioiTinh = models.CharField(max_length=10)
    Role = models.CharField(max_length=50,default="Giảng viên")
    Status = models.CharField(max_length=50)
    class Meta:
        verbose_name = "Giảng viên"
        verbose_name_plural = "Giảng viên"

class Lop(BaseModel):  
    MaLop = models.CharField(max_length=50, unique=True)
    MaKhoa = models.ForeignKey(Khoa, on_delete=models.SET_NULL, null=True, blank=True)
    MaGV = models.ForeignKey(GiangVien, on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        verbose_name = "Lớp"
        verbose_name_plural = "Lớp"

class SinhVien(BaseModel):  
    UserAccount = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    Msv = models.CharField(max_length=50, unique=True,primary_key=True) 
    Ten = models.CharField(max_length=100)
    NgaySinh = models.DateField()
    Avatar = models.ImageField(upload_to='avatar/', default='default.jpg')
    GioiTinh = models.CharField(max_length=10)
    CCCD = models.CharField(max_length=20)
    MaLop = models.CharField(max_length=50)
    MaDanToc = models.CharField(max_length=50)
    Email = models.EmailField()
    DienThoai = models.CharField(max_length=20)
    NgapCapCCCD = models.DateField(null=True, blank=True)
    NoiCapCCCD = models.CharField(max_length=100, null=True, blank=True)
    QuocGia = models.CharField(max_length=50)
    Tinh = models.CharField(max_length=50)
    Huyen = models.CharField(max_length=50)
    Xa = models.CharField(max_length=50)
    SoNha = models.CharField(max_length=100,blank=True, null=True)
    TenDuong = models.CharField(max_length=100,blank=True, null=True)
    DiaChiLienLac = models.TextField()
    StatusCha = models.BooleanField(default=True)
    StatusMe = models.BooleanField(default=True)
    TenCha = models.CharField(max_length=100, null=True, blank=True)
    TenMe = models.CharField(max_length=100, null=True, blank=True)
    NgheNghiepCha = models.CharField(max_length=100, null=True, blank=True)
    NgheNghiepMe = models.CharField(max_length=100, null=True, blank=True)
    DienThoaiCha = models.CharField(max_length=20, null=True, blank=True)
    DienThoaiMe = models.CharField(max_length=20, null=True, blank=True)
    EmailCha = models.EmailField(null=True, blank=True)
    EmailMe = models.EmailField(null=True, blank=True)
    HoKhauCha = models.TextField(null=True, blank=True)
    HoKhauMe = models.TextField(null=True, blank=True)
    Status = models.CharField(max_length=50)
    MaKhoa = models.ForeignKey(Khoa, on_delete=models.SET_NULL, null=True, blank=True)
    MaGiangVien = models.ForeignKey(GiangVien, on_delete=models.SET_NULL, null=True, blank=True)
    HinhThucDaoTao = models.CharField(max_length=100)
    Role = models.CharField(max_length=50,default="Sinh viên")
    
    class Meta:
        verbose_name = "Sinh viên"
        verbose_name_plural = "Sinh viên"
class UserAccountManager(BaseUserManager):
    def create_user(self, username, password=None, email=None):
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, email=None):
        user = self.create_user(username=username, password=password, email=email)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        return self.get(username=username)

class UserAccount(BaseModel, AbstractBaseUser, PermissionsMixin):
    id=models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    UserStatus = models.BooleanField(default=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True, null=True, blank=True) 

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['email']

    objects = UserAccountManager()
    class Meta:
        verbose_name = "Tài khoản"
        verbose_name_plural = "Tài khoản"
class ThongBao(BaseModel):  
    MaTB = models.CharField(max_length=50, unique=True)
    MaGV = models.ForeignKey(GiangVien, on_delete=models.SET_NULL, null=True, blank=True)
    MaLop = models.ForeignKey(Lop, on_delete=models.SET_NULL, null=True, blank=True)
    TieuDe = models.CharField(max_length=100)
    NoiDung = models.TextField()
    NgayDang = models.DateTimeField(auto_now_add=True)
    LoaiTB = models.CharField(max_length=50)
    Status = models.CharField(max_length=50)
    class Meta:
        verbose_name = "Thông báo"
        verbose_name_plural = "Thông báo"
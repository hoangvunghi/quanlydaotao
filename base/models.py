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

class GiangVien(BaseModel):  
    UserAccount = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    MaGV = models.CharField(max_length=50, unique=True,primary_key=True) 
    HoTen = models.CharField(max_length=100)
    DienThoai = models.CharField(max_length=20)
    Email = models.EmailField()
    MaKhoa = models.ForeignKey(Khoa, on_delete=models.SET_NULL, null=True, blank=True)

class Lop(BaseModel):  
    MaLop = models.CharField(max_length=50, unique=True)
    MaKhoa = models.ForeignKey(Khoa, on_delete=models.SET_NULL, null=True, blank=True)
    MaGV = models.ForeignKey(GiangVien, on_delete=models.SET_NULL, null=True, blank=True)

class SinhVien(BaseModel):  
    UserAccount = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    Msv = models.CharField(max_length=50, unique=True,primary_key=True) 
    Ten = models.CharField(max_length=100)
    NgaySinh = models.DateField()
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

class UserAccountManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username=username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        return self.get(username=username)

class UserAccount(BaseModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True,primary_key=True)
    UserStatus = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserAccountManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    @property
    def email(self):
        return f"{self.username}@example.com" 

    @email.setter
    def email(self, value):
        pass  

    last_login = models.DateTimeField(auto_now=True, null=True, blank=True) 

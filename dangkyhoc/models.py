from django.db import models
from base.models import *
# Create your models here.

class MonHoc(BaseModel):
    MaMon=models.CharField(max_length=10,unique=True,primary_key=True)
    TenMon=models.CharField(max_length=100)
    SoTinChi=models.IntegerField()
    SoTietLyThuyet=models.IntegerField()
    SoTietThucHanh=models.IntegerField()
    MaKhoa=models.ForeignKey(Khoa,on_delete=models.CASCADE)
    Status=models.CharField(max_length=20,default='Chưa học')
    HeSo=models.FloatField()

class DieuKienTienQuyet(BaseModel):
    ID=models.AutoField(primary_key=True)
    MaMon=models.ForeignKey(MonHoc,on_delete=models.CASCADE,related_name='Mon_chinh')
    MaMonTienQuyet=models.ForeignKey(MonHoc,on_delete=models.CASCADE,related_name='mon_tien_quyet') 

class DangKyHocPhan(BaseModel):
    MaLopHocPhan=models.CharField(max_length=10,unique=True,primary_key=True)
    GioHoc=models.CharField(max_length=100)
    PhongHoc=models.CharField(max_length=100)
    MaGiangVien=models.ForeignKey(GiangVien,on_delete=models.CASCADE)
    SoLuongToiDa=models.IntegerField()
    Status=models.BooleanField(default=False)
    #Loai là kiểu như lí thuyết hoặc thực hành 
    Loai=models.CharField(max_length=20)
    MaMon=models.ForeignKey(MonHoc,on_delete=models.CASCADE)
    #lớp bài tập sẽ có lớp lí thuyết, lí thuyết thì không cần có
    MaLopLyThuyet=models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True)

class KetQuaDangKy(BaseModel):
    ID=models.AutoField(primary_key=True)
    MaSinhVien=models.ForeignKey(SinhVien,on_delete=models.CASCADE)
    MaLopHocPhan=models.ForeignKey(DangKyHocPhan,on_delete=models.CASCADE)
    NamHoc=models.CharField(max_length=10)
    HocKy=models.IntegerField()
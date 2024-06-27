from django.db import models
from base.models import *
from dangkyhoc.models import *
# Create your models here.

class KetQuaHocTap(BaseModel):
    ID=models.AutoField(primary_key=True)
    MaSinhVien=models.ForeignKey(SinhVien,on_delete=models.CASCADE)
    MaMon=models.ForeignKey(MonHoc,on_delete=models.CASCADE)
    DiemQuaTrinh=models.FloatField()
    DiemThi=models.FloatField()
    DiemTongKet=models.FloatField()
    DiemChu=models.CharField(max_length=10)
    HocKy=models.IntegerField()
    NamHoc=models.CharField(max_length=10)
    DiemKN1=models.FloatField()
    DiemKN2=models.FloatField()
    DiemKN3=models.FloatField()
    DiemKN4=models.FloatField()
    TongKetKN1=models.FloatField()
    TongKetKN2=models.FloatField()
    TongKetKN3=models.FloatField()
    TongKetKN4=models.FloatField()
    Status=models.CharField(max_length=20,default='Chưa qua')
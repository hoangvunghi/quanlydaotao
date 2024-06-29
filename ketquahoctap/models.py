from django.db import models
from base.models import *
from dangkyhoc.models import *
# Create your models here.

class KetQuaHocTap(BaseModel):
    ID=models.AutoField(primary_key=True)
    MaSinhVien=models.ForeignKey(SinhVien,on_delete=models.CASCADE)
    MaMon=models.ForeignKey(MonHoc,on_delete=models.SET_NULL,null=True)
    DiemQuaTrinh=models.FloatField(null=True,blank=True)
    DiemThi=models.FloatField(blank=True,null=True)
    DiemTongKet=models.FloatField(blank=True,null=True)
    DiemChu=models.CharField(max_length=100,blank=True,null=True)
    HocKy=models.IntegerField(blank=True,null=True)
    NamHoc=models.CharField(max_length=10,blank=True,null=True)
    DiemKN1=models.FloatField(blank=True,null=True)
    DiemKN2=models.FloatField(blank=True,null=True)
    DiemKN3=models.FloatField(blank=True,null=True)
    DiemKN4=models.FloatField(blank=True,null=True)
    TongKetKN1=models.FloatField(blank=True,null=True)
    TongKetKN2=models.FloatField(blank=True,null=True)
    TongKetKN3=models.FloatField(blank=True,null=True)
    TongKetKN4=models.FloatField(blank=True,null=True)
    Status=models.CharField(max_length=20,default='Chưa qua')

    class Meta:
        verbose_name='Kết quả học tập'
        verbose_name_plural='Kết quả học tập'
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import KetQuaHocTap, HeSoMonHoc
from dangkyhoc.models import MonHoc
from .libs import diem_qua_trinh, diem_thi, diem_thi_lai, diem_tong_ket

@receiver(post_save, sender=KetQuaHocTap)
def update_scores(sender, instance, **kwargs):
    if 'update_scores' in kwargs:
        return

    KetQuaHocTap.objects.filter(pk=instance.pk).update(
        DiemQuaTrinh=diem_qua_trinh(instance.MaMon_id, instance.MaSinhVien_id),
        DiemThi=diem_thi(instance.MaMon_id, instance.MaSinhVien_id),
        DiemThiLai=diem_thi_lai(instance.MaMon_id, instance.MaSinhVien_id),
        DiemTongKet=diem_tong_ket(instance.MaMon_id, instance.MaSinhVien_id)
    )

@receiver(post_save, sender=MonHoc)
def create_he_so_mon_hoc(sender, instance, created, **kwargs):
    if created:
        HeSoMonHoc.objects.create(MaMon=instance)

from .models import *

def tong_he_so(heso1,heso2,heso3,heso4):
    heso=heso1+heso2+heso3+heso4
    if heso != 1:
        return False
    return True

MIN_PROCESS_SCORE = 4
MIN_FINAL_SCORE = 4
EXCEPTIONAL_SCORE_THRESHOLD = 7

def diem_qua_trinh(mamon, masv):
    try:
        monhoc = KetQuaHocTap.objects.get(MaMon=mamon, MaSinhVien=masv)
        heso = HeSoMonHoc.objects.get(MaMon=mamon)
    except (KetQuaHocTap.DoesNotExist, HeSoMonHoc.DoesNotExist):
        return None

    if not monhoc.DiemKN1:
        return 0
    else:
        diem_qt = (monhoc.DiemKN1 * heso.HeSoKN1 + monhoc.DiemKN2 * heso.HeSoKN2 +
                   monhoc.DiemKN3 * heso.HeSoKN3 + monhoc.DiemKN4 * heso.HeSoKN4)
        return diem_qt

def diem_thi(mamon, masv):
    try:
        monhoc = KetQuaHocTap.objects.get(MaMon=mamon, MaSinhVien=masv)
        heso = HeSoMonHoc.objects.get(MaMon=mamon)
    except (KetQuaHocTap.DoesNotExist, HeSoMonHoc.DoesNotExist):
        return None

    if not monhoc.TongKetKN1:
        return 0
    else:
        diem_thi = (monhoc.TongKetKN1 * heso.HeSoTongKetKN1 + monhoc.TongKetKN2 * heso.HeSoTongKetKN2 +
                    monhoc.TongKetKN3 * heso.HeSoTongKetKN3 + monhoc.TongKetKN4 * heso.HeSoTongKetKN4)
        return diem_thi

def diem_thi_lai(mamon, masv):
    try:
        monhoc = KetQuaHocTap.objects.get(MaMon=mamon, MaSinhVien=masv)
        heso = HeSoMonHoc.objects.get(MaMon=mamon)
    except (KetQuaHocTap.DoesNotExist, HeSoMonHoc.DoesNotExist):
        return None

    if not monhoc.DiemThiLai1:
        return 0
    else:
        diem_thi_lai = (monhoc.DiemThiLai1 * heso.HeSoTongKetKN1 + monhoc.DiemThiLai2 * heso.HeSoTongKetKN2 +
                        monhoc.DiemThiLai3 * heso.HeSoTongKetKN3 + monhoc.DiemThiLai4 * heso.HeSoTongKetKN4)
        return diem_thi_lai

def diem_tong_ket(mamon, masv):
    try:
        monhoc = KetQuaHocTap.objects.get(MaMon=mamon, MaSinhVien=masv)
        heso = HeSoMonHoc.objects.get(MaMon=mamon)
    except (KetQuaHocTap.DoesNotExist, HeSoMonHoc.DoesNotExist):
        return None

    qua_trinh = diem_qua_trinh(mamon, masv)
    if qua_trinh is None or qua_trinh < MIN_PROCESS_SCORE:
        return 0

    diem_thi_final = diem_thi(mamon, masv)
    if diem_thi_final is None:
        return None

    diem_thi_lai_final = diem_thi_lai(mamon, masv)
    if diem_thi_lai_final and diem_thi_lai_final > diem_thi_final:
        diem_thi_final = diem_thi_lai_final

    diem_tong_ket = qua_trinh * heso.HeSoDiemQuaTrinh + diem_thi_final * heso.HeSoTongKet
    if diem_thi_lai_final and diem_thi_final == diem_thi_lai_final:
        diem_tong_ket = max(diem_tong_ket, EXCEPTIONAL_SCORE_THRESHOLD)

    return diem_tong_ket
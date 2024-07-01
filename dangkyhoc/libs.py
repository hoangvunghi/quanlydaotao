from .models import *
from ketquahoctap.models import *

#check 1 môn có được mở trong học kì này hay không bằng cách xem DangKyHocPhan có môn đó không
def check_opened_course(mamon):
    try:
        course=DangKyHocPhan.objects.get(MaMon=mamon)
        return True
    except DangKyHocPhan.DoesNotExist:
        return False
    
#check xem có được học môn đó không bằng điều kiện tiên quyết, bây giờ sẽ xét 1 môn có được học không bằng cách kiểm tra những 
#môn tiên quyết của nó, nếu có 1 môn tiên quyết nào đó chưa qua thì không được học (kết quả học tập có status là chưa qua)
def check_course_prerequisite(mamon,masv):
    try:
        prerequisites=DieuKienTienQuyet.objects.filter(MaMon=mamon)
        for prerequisite in prerequisites:
            try:
                result=KetQuaDangKy.objects.get(MaSinhVien=masv,MaLopHocPhan=prerequisite.MaMonTienQuyet.MaMon)
                if result.Status=='Chưa qua':
                    return False
            except KetQuaDangKy.DoesNotExist:
                return False
        return True
    except DieuKienTienQuyet.DoesNotExist:
        return True

def lay_thoi_khoa_bieu_da_dang_ky(ma_sinh_vien, nam_hoc, hoc_ky):
    ket_qua_dang_ky = KetQuaDangKy.objects.filter(MaSinhVien=ma_sinh_vien, NamHoc=nam_hoc, HocKy=hoc_ky)
    thoi_khoa_bieu = []
    for ket_qua in ket_qua_dang_ky:
        lop_hoc_phan = DangKyHocPhan.objects.get(MaLopHocPhan=ket_qua.MaLopHocPhan.MaLopHocPhan)
        thoi_khoa_bieu.append({
            'MaLopHocPhan': lop_hoc_phan.MaLopHocPhan,
            'GioHoc': lop_hoc_phan.GioHoc,
            'PhongHoc': lop_hoc_phan.PhongHoc
        })
    return thoi_khoa_bieu

def lay_gio_hoc(thoi_khoa_bieu):
    gio_hoc_list = [item['GioHoc'] for item in thoi_khoa_bieu]
    gio_hoc_chung = ", ".join(gio_hoc_list)
    return gio_hoc_chung

def parse_schedule(schedule_str):
    day_to_num = {'thứ 2': 2, 'thứ 3': 3, 'thứ 4': 4, 'thứ 5': 5, 'thứ 6': 6, 'thứ 7': 7, 'chủ nhật': 1}
    parts = schedule_str.split(', ')    
    result = []
    for part in parts:
        time_part, day_part = part.split(' thứ ')
        day_num = day_to_num['thứ ' + day_part]
        result.append((time_part, day_num))
    return result

def kiem_tra_trung_lich(lich_hoc_moi,lich_hoc):
    lich_hoc_moi=parse_schedule(lich_hoc_moi)
    lich_hoc=parse_schedule(lich_hoc)
    for lich in lich_hoc_moi:
        for lich2 in lich_hoc:
            if lich[1]==lich2[1]:
                if lich[0]==lich2[0]:
                    return True
    return False

    

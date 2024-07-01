from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from .libs import *
@api_view(['GET', 'POST'])
def monhoc_list_create(request):
    if request.method == 'GET':
        monhocs = MonHoc.objects.all()
        serializer = MonHocSerializer(monhocs, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MonHocSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PATCH', 'DELETE'])
def monhoc_detail(request, pk):
    try:
        monhoc = MonHoc.objects.get(MaTB=pk)
    except MonHoc.DoesNotExist:
        return Response({'error': 'monhoc not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MonHocSerializer(monhoc)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = MonHocSerializer(monhoc, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        monhoc.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#tương tự với điều kiện tiên quyết
@api_view(['GET', 'POST'])
def dieukientienquyet_list_create(request):
    if request.method == 'GET':
        dieukiens = DieuKienTienQuyet.objects.all()
        serializer = DieuKienTienQuyetSerializer(dieukiens, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DieuKienTienQuyetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH', 'DELETE'])
def dieukientienquyet_detail(request, pk):
    try:
        dieukien = DieuKienTienQuyet.objects.get(ID=pk)
    except DieuKienTienQuyet.DoesNotExist:
        return Response({'error': 'dieukien not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DieuKienTienQuyetSerializer(dieukien)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = DieuKienTienQuyetSerializer(dieukien, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        dieukien.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
api_view(['POST'])
def register_course(request):
    ma_lop_hoc_phan=request.data['MaLopHocPhan']
    hocky=request.data['HocKy']
    namhoc=request.data['NamHoc']
    ma_mon = DangKyHocPhan.objects.get(MaLopHocPhan=ma_lop_hoc_phan).MaMon
    open=check_opened_course(ma_mon,hocky,namhoc)  
    if open:
        dieu_kien_tien_quyet=check_course_prerequisite(ma_mon,request.data['MaSinhVien'])
        if dieu_kien_tien_quyet:
            thoi_khoa_bieu_hien_tai = lay_thoi_khoa_bieu_da_dang_ky(request.data['MaSinhVien'], namhoc, hocky)
            gio_hoc_thoi_khoa_bieu_hien_tai = parse_schedule(lay_gio_hoc(thoi_khoa_bieu_hien_tai))
            gio_hoc_moi = DangKyHocPhan.objects.get(MaLopHocPhan=ma_lop_hoc_phan).GioHoc
            trung_lich=kiem_tra_trung_lich(gio_hoc_moi, gio_hoc_thoi_khoa_bieu_hien_tai)
            if not trung_lich:
                serializer = KetQuaDangKySerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response("message: 'Đăng ký thành công'", status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Schedule conflict'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Not enough prerequisite'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Course not opened'}, status=status.HTTP_404_NOT_FOUND) 
    
@api_view(['Delete'])
def delete_course(request):
    ma_lop_hoc_phan=request.data['MaLopHocPhan']
    hocky=request.data['HocKy']
    namhoc=request.data['NamHoc']
    try:
        ket_qua=KetQuaDangKy.objects.get(MaLopHocPhan=ma_lop_hoc_phan,HocKy=hocky,NamHoc=namhoc)
        ket_qua.delete()
        return Response("message: 'Xóa thành công'", status=status.HTTP_204_NO_CONTENT)
    except KetQuaDangKy.DoesNotExist:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
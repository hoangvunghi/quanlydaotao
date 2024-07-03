from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from .libs import *
# Create your views here.

@api_view(['GET', 'POST'])
def ketquahoctap_list_create(request):
    if request.method == 'GET':
        ketquas = KetQuaHocTap.objects.all()
        serializer = KetQuaHocTapSerializer(ketquas, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = KetQuaHocTapSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH', 'DELETE'])
def ketquahoctap_detail(request, pk):
    try:
        ketqua = KetQuaHocTap.objects.get(ID=pk)
    except KetQuaHocTap.DoesNotExist:
        return Response({'error': 'ketqua not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = KetQuaHocTapSerializer(ketqua)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = KetQuaHocTapSerializer(ketqua, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        ketqua.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def cap_nhat_diem_KN(mamon, masv, diemKN1=None, diemKN2=None, diemKN3=None, diemKN4=None):
    monhoc = KetQuaHocTap.objects.get(MaMon=mamon, MaSinhVien=masv)
    if monhoc.DiemQuaTrinh is None or monhoc.DiemQuaTrinh == 0:
        if diemKN1 is not None:
            monhoc.DiemKN1 = diemKN1
        if diemKN2 is not None:
            monhoc.DiemKN2 = diemKN2
        if diemKN3 is not None:
            monhoc.DiemKN3 = diemKN3
        if diemKN4 is not None:
            monhoc.DiemKN4 = diemKN4
        monhoc.save()
    else:
        print("Không thể cập nhật điểm KN sau khi đã có điểm quá trình.")

@api_view(['PATCH'])
def cap_nhat_diem_qua_trinh(request,pk):
    try:
        ket_qua = KetQuaHocTap.objects.get(ID=pk)
    except KetQuaHocTap.DoesNotExist:
        return Response({'error': 'ketqua not found'}, status=status.HTTP_404_NOT_FOUND)
    diem_qua_trinh= ket_qua.DiemQuaTrinh
    if diem_qua_trinh is not None:
        return Response({'error': 'Điểm quá trình đã được cập nhật'}, status=status.HTTP_400_BAD_REQUEST)
    serializer = KetQuaHocTapSerializer(ket_qua, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
def cap_nhat_diem_tong_ket(request,pk):
    try:
        ket_qua = KetQuaHocTap.objects.get(ID=pk)
    except KetQuaHocTap.DoesNotExist:
        return Response({'error': 'ketqua not found'}, status=status.HTTP_404_NOT_FOUND)
    if ket_qua.DiemQuaTrinh is None or ket_qua.DiemQuaTrinh < 4 :
        return Response({'error': 'Chưa cập nhật điểm quá trình hoặc không thể cập nhật do trượt môn'}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PATCH':
        serializer = KetQuaHocTapSerializer(ket_qua, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

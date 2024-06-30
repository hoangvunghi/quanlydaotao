from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status

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
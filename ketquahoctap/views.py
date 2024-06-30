from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
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

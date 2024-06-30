from rest_framework import serializers
from .models import MonHoc,DangKyHocPhan,DieuKienTienQuyet,KetQuaDangKy

class MonHocSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonHoc
        fields = '__all__'

class DangKyHocPhanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DangKyHocPhan
        fields = '__all__'

class DieuKienTienQuyetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DieuKienTienQuyet
        fields = '__all__'

class KetQuaDangKySerializer(serializers.ModelSerializer):
    class Meta:
        model = KetQuaDangKy
        fields = '__all__'


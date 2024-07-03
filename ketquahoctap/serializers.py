from rest_framework import serializers
from .models import KetQuaHocTap, HeSoMonHoc

class KetQuaHocTapSerializer(serializers.ModelSerializer):
    class Meta:
        model = KetQuaHocTap
        fields = '__all__'

class HeSoMonHocSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeSoMonHoc
        fields = '__all__'
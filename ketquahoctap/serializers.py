from rest_framework import serializers
from .models import KetQuaHocTap

class KetQuaHocTapSerializer(serializers.ModelSerializer):
    class Meta:
        model = KetQuaHocTap
        fields = '__all__'

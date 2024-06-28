from rest_framework import serializers
from .models import Khoa, GiangVien, Lop, SinhVien, UserAccount

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')

        if password != password2:
            raise serializers.ValidationError("Passwords do not match")

        return data
    
class KhoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Khoa
        fields = '__all__'

class GiangVienSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiangVien
        fields = '__all__'

class LopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lop
        fields = '__all__'

class SinhVienSerializer(serializers.ModelSerializer):
    class Meta:
        model = SinhVien
        fields = '__all__'

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'
        extra_kwargs = {
        'password': {'write_only': True},
        }
    def create(self, validated_data):
        password = validated_data.get('password')
        user = UserAccount.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    def update(self, instance, validated_data):
        validated_data.update(self.initial_data)
        return super().update(instance=instance, validated_data=validated_data)

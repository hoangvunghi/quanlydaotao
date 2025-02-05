# Generated by Django 5.0.6 on 2024-06-28 15:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('UserStatus', models.BooleanField(default=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('last_login', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('updated_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Khoa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('MaKhoa', models.CharField(max_length=50, unique=True)),
                ('TenKhoa', models.CharField(max_length=100)),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GiangVien',
            fields=[
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('MaGV', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('HoTen', models.CharField(max_length=100)),
                ('DienThoai', models.CharField(max_length=20)),
                ('Email', models.EmailField(max_length=254)),
                ('UserAccount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
                ('MaKhoa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.khoa')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Lop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('MaLop', models.CharField(max_length=50, unique=True)),
                ('MaGV', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.giangvien')),
                ('MaKhoa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.khoa')),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SinhVien',
            fields=[
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('Msv', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('Ten', models.CharField(max_length=100)),
                ('NgaySinh', models.DateField()),
                ('GioiTinh', models.CharField(max_length=10)),
                ('CCCD', models.CharField(max_length=20)),
                ('MaLop', models.CharField(max_length=50)),
                ('MaDanToc', models.CharField(max_length=50)),
                ('Email', models.EmailField(max_length=254)),
                ('DienThoai', models.CharField(max_length=20)),
                ('NgapCapCCCD', models.DateField(blank=True, null=True)),
                ('NoiCapCCCD', models.CharField(blank=True, max_length=100, null=True)),
                ('QuocGia', models.CharField(max_length=50)),
                ('Tinh', models.CharField(max_length=50)),
                ('Huyen', models.CharField(max_length=50)),
                ('Xa', models.CharField(max_length=50)),
                ('SoNha', models.CharField(blank=True, max_length=100, null=True)),
                ('TenDuong', models.CharField(blank=True, max_length=100, null=True)),
                ('DiaChiLienLac', models.TextField()),
                ('StatusCha', models.BooleanField(default=True)),
                ('StatusMe', models.BooleanField(default=True)),
                ('TenCha', models.CharField(blank=True, max_length=100, null=True)),
                ('TenMe', models.CharField(blank=True, max_length=100, null=True)),
                ('NgheNghiepCha', models.CharField(blank=True, max_length=100, null=True)),
                ('NgheNghiepMe', models.CharField(blank=True, max_length=100, null=True)),
                ('DienThoaiCha', models.CharField(blank=True, max_length=20, null=True)),
                ('DienThoaiMe', models.CharField(blank=True, max_length=20, null=True)),
                ('EmailCha', models.EmailField(blank=True, max_length=254, null=True)),
                ('EmailMe', models.EmailField(blank=True, max_length=254, null=True)),
                ('HoKhauCha', models.TextField(blank=True, null=True)),
                ('HoKhauMe', models.TextField(blank=True, null=True)),
                ('Status', models.CharField(max_length=50)),
                ('HinhThucDaoTao', models.CharField(max_length=100)),
                ('MaGiangVien', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.giangvien')),
                ('MaKhoa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.khoa')),
                ('UserAccount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

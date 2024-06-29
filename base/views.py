from .models import *
from .serializers import *
from rest_framework import permissions
from .permissions import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password,check_password
from .serializers import ForgotPasswordSerializer, ResetPasswordSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from itsdangerous import URLSafeTimedSerializer as Serializer, BadData
from .libs import *
from django.shortcuts import get_object_or_404
UserAccount = get_user_model()
import base64
from django.core.files.base import ContentFile
@api_view(["POST"])
@permission_classes([AllowAny])
def forgot_password_view(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        email = serializer.validated_data['email']
        try:
            useraccount = UserAccount.objects.get(email=email)  
        except UserAccount.DoesNotExist:
            return Response({"message": "UserAccount not found for the provided email"},
                            status=status.HTTP_404_NOT_FOUND)
        try:
            s = Serializer(settings.SECURITY_PASSWORD_SALT)
            token = s.dumps({"username": useraccount.username})

        except Exception as e: 
            return Response({"error": "Failed to generate reset token",
                             "details": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        email_subject = "Password Reset Request"
        email_message = f"Here's an email about forgetting the password for account: {useraccount.username} \n" 
        email_message += f"Click the following link to reset your password: {settings.BACKEND_URL}/reset-password/{token}"

        send_mail(
            email_subject,
            email_message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return Response({"message": "Password reset email sent successfully"},
                        status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password_view(request, token):
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        s = Serializer(settings.SECURITY_PASSWORD_SALT)
        try:
            data = s.loads(token, max_age=3600) 
            user = UserAccount.objects.get(username=data["username"])  
        except (BadData, UserAccount.DoesNotExist):
            return Response({"error": "Invalid or expired reset token"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        new_password = serializer.validated_data['password']
        if not new_password:
            raise ValidationError("New password is required")
        
        user.password = make_password(new_password)
        user.save()

        return Response({"message": "Password reset successfully"},
                        status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def login(request):
    if request.method == "POST":
        try:
            username = request.data.get("username", "").lower()
            password = request.data.get("password", "")
            
            if not username or not password:
                return Response(
                    {"error": "Username and password are required", "status": status.HTTP_400_BAD_REQUEST},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if not user.UserStatus:
                    return Response(
                        {"error": "Account has been locked.", "status": status.HTTP_401_UNAUTHORIZED},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
                try:
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                except TokenError as e:
                    if isinstance(e, InvalidToken) and e.args[0] == "Token has expired":
                        return Response(
                            {"error": "Access token has expired. Please refresh the token.",
                             "status": status.HTTP_401_UNAUTHORIZED},
                            status=status.HTTP_401_UNAUTHORIZED
                        )
                    else:
                        return Response(
                            {"error": "Invalid token.", "status": status.HTTP_401_UNAUTHORIZED},
                            status=status.HTTP_401_UNAUTHORIZED
                        )
                except Exception as e:
                    return Response(
                        {"error": str(e), "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                data_login = UserAccountSerializer(user).data
                response_data = {
                    "response": "Login successful",
                    "data": data_login,
                    'token': {
                        'refresh': str(refresh),
                        'access': access_token,
                    },
                    "status": status.HTTP_200_OK,
                }
                response = Response(response_data, status=status.HTTP_200_OK)
                return response
            else:
                return Response(
                    {'error': 'Invalid username or password', "status": status.HTTP_401_UNAUTHORIZED},
                    status=status.HTTP_401_UNAUTHORIZED
                )

        except Exception as e:
            return Response(
                {'error': str(e), "status": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadonly])
def change_password(request, pk):
    if request.method == 'POST':
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        
        if not strong_password(new_password):
            return Response({'success': False, 'message': 'New password must be at least 8 characters long and contain at least one uppercase letter.',
                             "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)

        UserAccount = get_user_model()
        try:
            user_account = UserAccount.objects.get(EmpID=pk)
        except UserAccount.DoesNotExist:
            return Response({'success': False, 'message': 'User not found.',
                             "status": status.HTTP_404_NOT_FOUND},
                            status=status.HTTP_404_NOT_FOUND)
        
        if not check_password(current_password, user_account.password):
            return Response({'success': False, 'message': 'Current password is incorrect.',
                             "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)

        user_account.set_password(new_password)
        user_account.save()
        
        return Response({'success': True, 'message': 'Password changed successfully.',
                         "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)

    return Response({'success': False, 'message': 'Invalid request method.',
                     "status": status.HTTP_400_BAD_REQUEST},
                    status=status.HTTP_400_BAD_REQUEST)

## viết api cập nhật thông tin cho giảng viên và sinh viên --done
##viết api cập nhật tài khoản, đổi mật khẩu, reset mật khẩu -- done
# viết model notice, viết api thông báo cho sinh viên và giảng viên --done

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadonly])
def update_account(request, pk):
    try:
        employee = UserAccount.objects.get(id=pk)
    except UserAccount.DoesNotExist:
        return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PATCH':
        email = request.data.get('email', None)
        if email is None:
            return Response({"error": "Email field is required", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        errors = validate_email(email)  
        if errors:
            return Response({"error": errors, "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        employee.email = email
        employee.save()
        serializer = UserAccountSerializer(employee)
        return Response({"message": "Email update successful", "data": serializer.data, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminUserOrNoAccess])
def reset_password_for_admin(request, pk):
    try:
        user = UserAccount.objects.get(id=pk)
    except UserAccount.DoesNotExist:
        return Response({"error": "User Account not found",
                         "status": status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)

    new_password = request.data.get('new_password')

    if not new_password:
        return Response({"error": "New password is required",
                         "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)

    hashed_password = make_password(new_password)
    
    user.password = hashed_password
    user.save()

    refresh = RefreshToken.for_user(user)
    
    serializer = UserAccountSerializer(user)
    return Response({"message": "Password reset successfully",
                     "data": serializer.data,
                     "status": status.HTTP_200_OK},
                    status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadonly])
def update_infor(request, pk):
    role = role_member(pk)
    if role == "sv":
        member = SinhVien.objects.get(Msv=pk)
    elif role == "gv":
        member = GiangVien.objects.get(MaGV=pk)
    else:
        return Response({"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        errors = validate_to_update(member, request.data)
        if errors:
            return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)

        new_base64_image = request.data.get('Avatar', None)
        if new_base64_image:
            if member.Avatar and member.Avatar.name != 'default.jpg':
                member.Avatar.delete()
            try:
                image_data = base64.b64decode(new_base64_image.split(',')[1])
                image_file = ContentFile(image_data, name='uploaded_image.jpg')
                member.Avatar = image_file
            except Exception as e:
                return Response({"error": "Error decoding base64 image", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        new_email = request.data.get('Email', '')
        if new_email and validate_email(new_email) is False:
            return Response({"error": "Invalid email format"}, status=status.HTTP_400_BAD_REQUEST)

        phone_number = request.data.get('Phone', '')
        if phone_number and validate_phone(phone_number) is False:
            return Response({"error": "Invalid phone number format"}, status=status.HTTP_400_BAD_REQUEST)

        obj_update(member, request.data)

        if role == "sv":
            serializer = SinhVienSerializer(member)
        else:
            serializer = GiangVienSerializer(member)

        serialized_data = []
        data = serializer.data
        id_field = "Msv" if role == "sv" else "MaGV"
        id_value = data[id_field]
        try:
            user = UserAccount.objects.get(username=id_value)
            username = user.username
            pass_word = user.get_password()
            data["username"] = username
            data["password"] = pass_word
        except UserAccount.DoesNotExist:
            data["username"] = None
            data["password"] = None

        serialized_data.append(data)
        return Response({"message": "Update successful", "data": serialized_data, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
    
##thông báo
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ThongBao
from .serializers import ThongBaoSerializer

@api_view(['GET', 'POST'])
def thongbao_list_create(request):
    if request.method == 'GET':
        thongbaos = ThongBao.objects.all()
        serializer = ThongBaoSerializer(thongbaos, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ThongBaoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH', 'DELETE'])
def thongbao_detail(request, pk):
    try:
        thongbao = ThongBao.objects.get(MaTB=pk)
    except ThongBao.DoesNotExist:
        return Response({'error': 'ThongBao not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ThongBaoSerializer(thongbao)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = ThongBaoSerializer(thongbao, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        thongbao.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
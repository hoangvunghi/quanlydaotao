from .models import Khoa, GiangVien, Lop, SinhVien,UserAccount
from .serializers import KhoaSerializer, GiangVienSerializer, LopSerializer, SinhVienSerializer, UserAccountSerializer
from rest_framework import permissions
from .permissions import IsOwnerOrReadonly
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .serializers import ForgotPasswordSerializer, ResetPasswordSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from itsdangerous import URLSafeTimedSerializer as Serializer, BadData

UserAccount = get_user_model()

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


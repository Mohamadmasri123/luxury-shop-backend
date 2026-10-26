from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
import traceback
from .serializers import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    """
    نظام تسجيل المستخدمين التقليدي (بالاسم وكلمة المرور والبريد)
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class GoogleLoginView(APIView):
    """
    نظام تسجيل الدخول والتحقق الآمن عبر جوجل (Google OAuth 2.0 Token Verification)
    """
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        
        if not token:
            return Response({'error': 'Google token is missing.'}, status=400)

        try:
            CLIENT_ID = settings.GOOGLE_CLIENT_ID
            
            # التحقق من التوكن عبر جوجل
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

            email = idinfo.get('email')
            if not email:
                return Response({'error': 'Email not found in Google token.'}, status=400)

            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')
            username = email.split('@')[0]

            # إنشاء المستخدم أو جلبه بأمان تام في قاعدة بيانات Neon
            user, created = User.objects.get_or_create(email=email, defaults={
                'username': username,
                'first_name': first_name,
                'last_name': last_name
            })

            # توليد رموز الـ JWT الخاصة بنظامك لتستمر الجلسة بسلاسة
            refresh = RefreshToken.for_user(user)

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.username,
                'email': user.email
            }, status=200)
            
        except ValueError as e:
            print("ValueError during Google Token verification:", str(e))
            return Response({'error': f'Invalid Google Token: {str(e)}'}, status=400)
        except Exception as e:
            print("Unexpected Error:", str(e))
            traceback.print_exc()
            return Response({'error': str(e)}, status=500)


class UserProfileView(APIView):
    """
    جلب بيانات المستخدم الحالي المحمي برمز الـ JWT
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        })
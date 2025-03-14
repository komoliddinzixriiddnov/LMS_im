from django.shortcuts import render

from random import randint

from django.core.cache import cache
from django.template.context_processors import request
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, MeSerializer, ChangePasswordSerializer, ResetPasswordSerializer, \
    VerifyOTPSerializer, SetNewPasswordSerializer
from app_users.models import User


class LoginAPIView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        phone = request.data.get("phone")
        password = request.data.get("password")

        user = User.objects.filter(phone=phone).first()

        if user and user.check_password(password):

            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })

        return Response({"status":False,"detail": "Telefon raqam yoki parol noto‘g‘ri"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Tokenni qora ro‘yxatga qo‘shish
            return Response({"message": "Logout successful"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

class CurrentUserView(RetrieveAPIView):
    serializer_class = MeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"status":False,"detail": "Eski parolingiz xato"}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data['new_password'])
            user.save()

            return Response({"status":True,"detail": "Parolingiz muaffaqiyatli yangilandi!"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    @swagger_auto_schema(request_body=ResetPasswordSerializer)
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            user = User.objects.filter(phone=phone).first()

            if user:
                otp_code = str(randint(1000, 9999))
                print("Yaratilgan OTP:", otp_code)
                cache.set(phone, otp_code, timeout=900)

                return Response({"status": True, "detail": "OTP muvaffaqiyatli yuborildi"}, status=status.HTTP_200_OK)

            return Response({"status": False, "detail": "Bunday telefon raqam mavjud emas"},
                            status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    @swagger_auto_schema(request_body=VerifyOTPSerializer)
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            cache.set(f"verified_{phone}", True, timeout=900)
            return Response({"status": True, "detail": "OTP muvaffaqiyatli tasdiqlandi"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SetNewPasswordView(APIView):
    @swagger_auto_schema(request_body=SetNewPasswordSerializer)
    def post(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            verified = cache.get(f"verified_{phone}")

            if not verified:
                return Response({"status": False, "detail": "OTP tasdiqlanmagan"}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.filter(phone=phone).first()
            if user:
                user.set_password(serializer.validated_data['new_password'])
                user.save()

                return Response({"status": True, "detail": "Parol muvaffaqiyatli o‘rnatildi"}, status=status.HTTP_200_OK)
            return Response({"status": False, "detail": "Foydalanuvchi topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#
#
# from django.core.cache import cache
# from random import randint
# from drf_yasg.utils import swagger_auto_schema
# from rest_framework import status
# from rest_framework.generics import RetrieveAPIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
#
# from .serializers import (
#     LoginSerializer,
#     MeSerializer,
#     ChangePasswordSerializer,
#     ResetPasswordSerializer,
#     VerifyOTPSerializer,
#     SetNewPasswordSerializer,
# )
# from app_users.models import User
#
#
# class LoginAPIView(APIView):
#     @swagger_auto_schema(request_body=LoginSerializer)
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             phone = serializer.validated_data['phone']
#             password = serializer.validated_data['password']
#
#             user = User.objects.filter(phone=phone).first()
#
#             if user and user.check_password(password):
#                 refresh = RefreshToken.for_user(user)
#                 return Response({
#                     "refresh": str(refresh),
#                     "access": str(refresh.access_token),
#                 })
#
#             return Response(
#                 {"status": False, "detail": "Telefon raqam yoki parol noto‘g‘ri"},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()  # Tokenni qora ro‘yxatga qo‘shish
#             return Response({"message": "Logout successful"}, status=200)
#         except Exception as e:
#             return Response({"error": str(e)}, status=400)
#
#
# class CurrentUserView(RetrieveAPIView):
#     serializer_class = MeSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_object(self):
#         return self.request.user
#
#
# class ChangePasswordView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     @swagger_auto_schema(request_body=ChangePasswordSerializer)
#     def post(self, request):
#         serializer = ChangePasswordSerializer(data=request.data)
#         if serializer.is_valid():
#             user = request.user
#             if not user.check_password(serializer.validated_data['old_password']):
#                 return Response(
#                     {"status": False, "detail": "Eski parolingiz xato"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#
#             user.set_password(serializer.validated_data['new_password'])
#             user.save()
#
#             return Response(
#                 {"status": True, "detail": "Parolingiz muaffaqiyatli yangilandi!"},
#                 status=status.HTTP_200_OK,
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class ResetPasswordView(APIView):
#     @swagger_auto_schema(request_body=ResetPasswordSerializer)
#     def post(self, request):
#         serializer = ResetPasswordSerializer(data=request.data)
#         if serializer.is_valid():
#             phone = serializer.validated_data['phone']
#             user = User.objects.filter(phone=phone).first()
#
#             if user:
#                 otp_code = str(randint(1000, 9999))
#                 print("Yaratilgan OTP:", otp_code)
#                 cache.set(phone, otp_code, timeout=900)
#
#                 return Response(
#                     {"status": True, "detail": "OTP muvaffaqiyatli yuborildi"},
#                     status=status.HTTP_200_OK,
#                 )
#
#             return Response(
#                 {"status": False, "detail": "Bunday telefon raqam mavjud emas"},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class VerifyOTPView(APIView):
#     @swagger_auto_schema(request_body=VerifyOTPSerializer)
#     def post(self, request):
#         serializer = VerifyOTPSerializer(data=request.data)
#         if serializer.is_valid():
#             phone = serializer.validated_data['phone']
#             otp = serializer.validated_data['otp']
#             cached_otp = cache.get(phone)
#
#             if cached_otp and str(cached_otp) == otp:
#                 cache.set(f"verified_{phone}", True, timeout=900)
#                 return Response(
#                     {"status": True, "detail": "OTP muvaffaqiyatli tasdiqlandi"},
#                     status=status.HTTP_200_OK,
#                 )
#             return Response(
#                 {"status": False, "detail": "Noto‘g‘ri yoki eskirgan OTP"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class SetNewPasswordView(APIView):
#     @swagger_auto_schema(request_body=SetNewPasswordSerializer)
#     def post(self, request):
#         serializer = SetNewPasswordSerializer(data=request.data)
#         if serializer.is_valid():
#             phone = serializer.validated_data['phone']
#             verified = cache.get(f"verified_{phone}")
#
#             if not verified:
#                 return Response(
#                     {"status": False, "detail": "OTP tasdiqlanmagan"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#
#             user = User.objects.filter(phone=phone).first()
#             if user:
#                 user.set_password(serializer.validated_data['new_password'])
#                 user.save()
#                 cache.delete(f"verified_{phone}")  # OTP tasdiqlanganligini o'chirish
#                 return Response(
#                     {"status": True, "detail": "Parol muvaffaqiyatli o‘rnatildi"},
#                     status=status.HTTP_200_OK,
#                 )
#             return Response(
#                 {"status": False, "detail": "Foydalanuvchi topilmadi"},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

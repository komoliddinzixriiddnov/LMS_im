from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from app_auth.views import (
    LoginAPIView,
    CurrentUserView,
    ChangePasswordView,
    ResetPasswordView,
    VerifyOTPView,
    SetNewPasswordView,
    LogoutView,
)

app_name = 'auth'

urlpatterns = [
    # path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', CurrentUserView.as_view(), name='me'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set_new_password'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login qilish
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
]



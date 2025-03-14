from django.test import TestCase

from app_auth.serializers import ChangePasswordSerializer, VerifyOTPSerializer, LoginSerializer
from app_users.serializers import *
from app_users.models import User

class SerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone="+998901234567",
            password="testpassword",
            full_name="Test User"
        )

    def test_login_serializer(self):
        data = {"phone": "+998901234567", "password": "testpassword"}
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_change_password_serializer(self):
        data = {
            "old_password": "testpassword",
            "new_password": "newpassword",
            "confirm_password": "newpassword",
        }
        serializer = ChangePasswordSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_verify_otp_serializer(self):
        cache.set("+998901234567", "123456")
        data = {"phone": "+998901234567", "otp": "123456"}
        serializer = VerifyOTPSerializer(data=data)
        self.assertTrue(serializer.is_valid())
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from app_users.models import User, Student, Teacher, Parent

# Barcha foydalanuvchilarni serializer qilish uchun
class UserAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

# Foydalanuvchi serializeri
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "password", "full_name", "phone")

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

# O‘qituvchi serializeri
class TeacherSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Teacher
        fields = ('id', 'user', 'courses', 'description')

# Talaba serializeri
class StudentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Student
        fields = ('id', 'user', 'group', 'courses', 'description')

# Ota-ona serializeri
class ParentSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Parent
        fields = ('id', 'name', 'surname', 'address', 'phone', 'description', 'students')


class GetStudentsByIdsSerializer(serializers.Serializer):
    student_ids = serializers.ListField(child=serializers.IntegerField())


class GetTeachersByIdsSerializer(serializers.Serializer):
    teacher_ids = serializers.ListField(child=serializers.IntegerField())


class UserAndTeacherSerializer(serializers.Serializer):
    user = UserSerializer()
    teacher = TeacherSerializer()


class UserAndStudentSerializer(serializers.Serializer):
    user = UserSerializer()
    student = StudentSerializer()
    parent = ParentSerializer()

# Super foydalanuvchi yaratish uchun serializer
class SuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'password','full_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_superuser(**validated_data)
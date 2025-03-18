from rest_framework import serializers

from app_courses.models import *

# Guruhlarni serializer qilish
class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

# Berilgan ID'lar bo‘yicha guruhlarni olish uchun serializer

class GetGroupsByIdsSerializer(serializers.Serializer):
    group_ids = serializers.ListField(child=serializers.IntegerField())

class SubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class TableSheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'

class TableTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableType
        fields = '__all__'

# Uy vazifalarining topshirilishini serializer qilish

class HomeworksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = '__all__'
        extra_kwargs = {'teacher': {'read_only': True}}

    def create(self, validated_data):
        request = self.context['request']  # Serializer context dan request olish
        teacher = getattr(request.user, 'teacher', None)  # Teacher borligini tekshirish
        if not teacher:
            raise serializers.ValidationError({"teacher": "User is not linked to a teacher."})

        validated_data['teacher'] = teacher  # `teacher` ni qo‘shish
        return super().create(validated_data)

class HomeworksSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkSubmission
        fields = '__all__'
        extra_kwargs = {'student': {'read_only': True},
                        'is_checked': {'read_only': True}}

class HomeworksReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkReview
        fields = '__all__'
        extra_kwargs = {
            'teacher': {'read_only': True}
        }


# Guruhdan talabalarni olib tashlash uchun serializer
class RemoveStudentsFromGroupSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()

class RemoveTeachersFromGroupSerializer(serializers.Serializer):
    teacher_id = serializers.IntegerField()

class GroupAddStudent(serializers.Serializer):
    student_id = serializers.IntegerField()

# Guruhga o‘qituvchi qo‘shish uchun serializer
class GroupAddTeacher(serializers.Serializer):
    teacher_id = serializers.IntegerField()
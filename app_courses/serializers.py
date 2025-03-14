from rest_framework import serializers

from app_courses.models import *


class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

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

class HomeworksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = '__all__'
        extra_kwargs = {'teacher': {'read_only': True}}

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


class RemoveStudentsFromGroupSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()

class RemoveTeachersFromGroupSerializer(serializers.Serializer):
    teacher_id = serializers.IntegerField()

class GroupAddStudent(serializers.Serializer):
    student_id = serializers.IntegerField()

class GroupAddTeacher(serializers.Serializer):
    teacher_id = serializers.IntegerField()
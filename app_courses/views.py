from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app_courses.models import Group
from app_courses.serializers import *
from app_users.models import Student, Teacher
from app_base.permissions import AdminUser
from app_base.pagination import Pagination


class GroupViewSet(viewsets.ViewSet):
    permission_classes = [AdminUser]

    def list(self, request):
        """
        Barcha faol guruhlarni paginatsiya bilan qaytaradi.
        """
        groups = Group.objects.filter(active=True).select_related('subject', 'table').prefetch_related('teacher', 'students')
        paginator = Pagination()
        result_page = paginator.paginate_queryset(groups, request)
        serializer = GroupsSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Berilgan IDga ega bo'lgan guruhni qaytaradi.
        """
        group = get_object_or_404(Group.objects.select_related('subject', 'table').prefetch_related('teacher', 'students'), pk=pk)
        serializer = GroupsSerializer(group)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='create/group')
    @swagger_auto_schema(request_body=GroupsSerializer)
    def create_group(self, request):
        """
        Yangi guruh yaratadi.
        """
        serializer = GroupsSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='update/group')
    @swagger_auto_schema(request_body=GroupsSerializer)
    def update_group(self, request, pk=None):
        """
        Mavjud guruhni yangilaydi.
        """
        group = get_object_or_404(Group, pk=pk)
        serializer = GroupsSerializer(group, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='delete/group')
    def delete_group(self, request, pk=None):
        """
        Guruhni o'chiradi (soft delete).
        """
        group = get_object_or_404(Group, pk=pk)
        group.is_active = False
        group.save()
        return Response({'status': True, 'detail': 'Guruh muvaffaqiyatli o\'chirildi.'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path='add-student')
    @swagger_auto_schema(request_body=GroupAddStudent)
    def add_student(self, request, pk=None):
        """
        Talabani guruhga qo'shadi.
        """
        group = get_object_or_404(Group, pk=pk)
        serializer = GroupAddStudent(data=request.data)

        if serializer.is_valid():
            student_id = serializer.validated_data['student_id']
            student = get_object_or_404(Student, pk=student_id)
            group.students.add(student)
            return Response(
                {'status': True, 'detail': f'Talaba {student.user.full_name} guruhga qo\'shildi: {group.title}'},
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='remove-student')
    @swagger_auto_schema(request_body=RemoveStudentsFromGroupSerializer)
    def remove_student(self, request, pk=None):
        """
        Talabani guruhdan olib tashlaydi.
        """
        group = get_object_or_404(Group, pk=pk)
        serializer = RemoveStudentsFromGroupSerializer(data=request.data)

        if serializer.is_valid():
            student_id = serializer.validated_data['student_id']
            student = get_object_or_404(Student, pk=student_id)
            if group.students.filter(id=student.id).exists():
                group.students.remove(student)
                return Response(
                    {'status': True, 'detail': f'Talaba {student.user.full_name} guruhdan olib tashlandi.'},
                    status=status.HTTP_200_OK)
            return Response({'status': False, 'detail': 'Bu talaba guruhga tegishli emas.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='add-teacher')
    @swagger_auto_schema(request_body=GroupAddTeacher)
    def add_teacher(self, request, pk=None):
        """
        O'qituvchini guruhga qo'shadi.
        """
        group = get_object_or_404(Group, pk=pk)
        serializer = GroupAddTeacher(data=request.data)

        if serializer.is_valid():
            teacher_id = serializer.validated_data['teacher_id']
            teacher = get_object_or_404(Teacher, pk=teacher_id)
            group.teacher.add(teacher)
            return Response(
                {'status': True, 'detail': f'O\'qituvchi {teacher.user.full_name} guruhga qo\'shildi: {group.title}'},
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='remove-teacher')
    @swagger_auto_schema(request_body=RemoveTeachersFromGroupSerializer)
    def remove_teacher(self, request, pk=None):
        """
        O'qituvchini guruhdan olib tashlaydi.
        """
        group = get_object_or_404(Group, pk=pk)
        serializer = RemoveTeachersFromGroupSerializer(data=request.data)

        if serializer.is_valid():
            teacher_id = serializer.validated_data['teacher_id']
            teacher = get_object_or_404(Teacher, pk=teacher_id)
            if group.teacher.filter(id=teacher.id).exists():
                group.teacher.remove(teacher)
                return Response(
                    {'status': True, 'detail': f'O\'qituvchi {teacher.user.full_name} guruhdan olib tashlandi.'},
                    status=status.HTTP_200_OK)
            return Response({'status': False, 'detail': 'Bu o\'qituvchi guruhga tegishli emas.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
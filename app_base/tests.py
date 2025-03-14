# from django.test import TestCase
# from django.test import TestCase, RequestFactory
# from .permissions import AdminUser, AdminOrTeacher, AdminOrStudent, AdminOrOwner
# from .models import BaseModel
# from django.contrib.auth import get_user_model
#
# User = get_user_model()
#
# class PermissionTests(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.admin_user = User.objects.create(username='admin', is_admin=True)
#         self.teacher_user = User.objects.create(username='teacher', is_teacher=True)
#         self.student_user = User.objects.create(username='student', is_student=True)
#         self.regular_user = User.objects.create(username='regular')
#
#     def test_admin_user_permission(self):
#         request = self.factory.get('/')
#         request.user = self.admin_user
#         self.assertTrue(AdminUser().has_permission(request, None))
#
#     def test_admin_or_teacher_permission(self):
#         request = self.factory.get('/')
#         request.user = self.teacher_user
#         self.assertTrue(AdminOrTeacher().has_permission(request, None))
#
#     def test_admin_or_student_permission(self):
#         request = self.factory.get('/')
#         request.user = self.student_user
#         self.assertTrue(AdminOrStudent().has_permission(request, None))
#
#     def test_admin_or_owner_permission(self):
#         obj = BaseModel.objects.create(user=self.regular_user)
#         request = self.factory.get('/')
#         request.user = self.regular_user
#         self.assertTrue(AdminOrOwner().has_object_permission(request, None, obj))
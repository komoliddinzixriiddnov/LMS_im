from rest_framework.permissions import BasePermission

class AdminUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_authenticated and request.user.is_admin or request.user.is_staff

class AdminOrTeacher(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_authenticated and request.user.is_teacher or request.user.is_staff or request.user.is_admin

class AdminOrStudent(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_authenticated and request.user.is_student or request.user.is_staff or request.user.is_admin

class AdminOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return request.user.is_authenticated and obj.user == request.user or request.user.is_staff or request.user.is_admin





# from rest_framework.permissions import BasePermission
# from rest_framework.exceptions import PermissionDenied
#
# class UserRoles:
#     @staticmethod
#     def is_admin(user):
#         # Foydalanuvchi admin ekanligini tekshiradi.
#         return user.is_authenticated and user.is_admin
#
#     @staticmethod
#     def is_staff(user):
#         # Foydalanuvchi staff (xodim) ekanligini tekshiradi.
#         return user.is_authenticated and user.is_staff
#
#     @staticmethod
#     def is_teacher(user):
#         # Foydalanuvchi o'qituvchi ekanligini tekshiradi.
#         return user.is_authenticated and user.is_teacher
#
#     @staticmethod
#     def is_student(user):
#         # Foydalanuvchi talaba ekanligini tekshiradi.
#         return user.is_authenticated and user.is_student
#
# class BaseUserPermission(BasePermission):
#     def _is_authenticated_admin_or_staff(self, user):
#         # Foydalanuvchi admin yoki staff ekanligini tekshiradi.
#         return UserRoles.is_admin(user) or UserRoles.is_staff(user)
#
# class AdminUser(BaseUserPermission):
#     def has_permission(self, request, view):
#         # Foydalanuvchi admin ekanligini tekshiradi.
#         if not UserRoles.is_admin(request.user):
#             raise PermissionDenied("Sizda admin huquqi yo'q.")
#         return True
#
# class AdminOrTeacher(BaseUserPermission):
#     def has_permission(self, request, view):
#         # Foydalanuvchi admin, staff yoki o'qituvchi ekanligini tekshiradi.
#         if not (self._is_authenticated_admin_or_staff(request.user) or
#                 UserRoles.is_teacher(request.user)):
#             raise PermissionDenied("Sizda ruxsat yo'q.")
#         return True
#
# class AdminOrStudent(BaseUserPermission):
#     def has_permission(self, request, view):
#         # Foydalanuvchi admin, staff yoki talaba ekanligini tekshiradi.
#         if not (self._is_authenticated_admin_or_staff(request.user) or
#                 UserRoles.is_student(request.user)):
#             raise PermissionDenied("Sizda ruxsat yo'q.")
#         return True
#
# class AdminOrOwner(BaseUserPermission):
#     def has_object_permission(self, request, view, obj):
#         # Foydalanuvchi admin, staff yoki obyekt egasi ekanligini tekshiradi.
#         if not (self._is_authenticated_admin_or_staff(request.user) or
#                 request.user.is_authenticated and obj.user == request.user):
#             raise PermissionDenied("Sizda ruxsat yo'q.")
#         return True
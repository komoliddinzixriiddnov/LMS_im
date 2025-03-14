# app_courses/urls.py
from django.urls import path
from .views import GroupViewSet

app_name = 'courses'  # app_name ni belgilang

urlpatterns = [
    path('groups/', GroupViewSet.as_view({'get': 'list', 'post': 'create'}), name='group-list'),
    path('groups/<int:pk>/', GroupViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='group-detail'),
    # Boshqa yo'nalishlar...
]


'''

HTTP Metodi	URL	Tavsif
GET	/api/v1/courses/groups/	Barcha guruhlarni olish
GET	/api/v1/courses/groups/<pk>/	ID bo'yicha guruhni olish
POST	/api/v1/courses/groups/create/group/	Yangi guruh yaratish
PUT	/api/v1/courses/groups/<pk>/update/group/	Guruhni yangilash
DELETE	/api/v1/courses/groups/<pk>/delete/group/	Guruhni o'chirish (soft delete)
POST	/api/v1/courses/groups/<pk>/add-student/	Talabani guruhga qo'shish
POST	/api/v1/courses/groups/<pk>/remove-student/	Talabani guruhdan olib tashlash
POST	/api/v1/courses/groups/<pk>/add-teacher/	O'qituvchini guruhga qo'shish
POST	/api/v1/courses/groups/<pk>/remove-teacher/	O'qituvchini guruhdan olib tashlash

'''

# app_courses/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GroupViewSet
from .views import *

app_name = 'courses'  # app_name ni belgilang
router = DefaultRouter()
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'tables', TableViewSet, basename='table')
router.register(r'table-types', TableTypeViewSet, basename='table-type')
router.register('homeworks',HomeworkViewSet,basename='homework')
router.register('homework-submissions',HomeworkSubmissionViewSet,basename='homework-submission')
router.register('homework-reviews',HomeworkReviewViewSet,basename='homework-review')

urlpatterns = [
    path('get-groups-by-ids/',GetGroupByIds.as_view(), name='get-groups-by-ids'),
    path('', include(router.urls)),

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

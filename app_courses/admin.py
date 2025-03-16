from django.contrib import admin
from app_courses.models import *

admin.site.register([Course,Homework,Group,Subject,HomeworkSubmission,HomeworkReview,Table,TableType])
# app_courses/admin.py
from django.contrib import admin
from .models import Group

# @admin.register(Group)
# class GroupAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')  # Admin panelida ko'rsatiladigan maydonlar
#     search_fields = ('name',)      # Qidirish uchun maydonlar
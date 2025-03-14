from django.contrib import admin

from app_users.models import User, Teacher, Student, Parent

admin.site.register([User,Teacher,Student,Parent])

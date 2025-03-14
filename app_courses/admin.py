from django.contrib import admin
from app_courses.models import *

admin.site.register([Course,Homework,Group,Subject,HomeworkSubmission,HomeworkReview])
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from anns1.views import StatusViewSet, AttendanceViewSet

app_name = 'anns1'
router = DefaultRouter()
router.register(r'status', StatusViewSet, basename='status')
router.register('attendance', AttendanceViewSet, basename='attendance')

urlpatterns = [
    path('', include(router.urls)),
]
from django.urls import path, include
from .views import (
    AdminCourseViewSet,
    HomeCourseListView,
    AllCourseListView,
    CourseDetailView
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("admin-courses", AdminCourseViewSet)

urlpatterns = [
    path("home-courses/", HomeCourseListView.as_view()),
    path("", AllCourseListView.as_view()),
    path("detail/<int:pk>/", CourseDetailView.as_view()),  
    path("", include(router.urls)),  
]
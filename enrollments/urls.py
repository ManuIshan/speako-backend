from django.urls import path
from .views import EnrollmentCreateView, CourseDetailView, MyEnrollmentsView
from rest_framework.routers import DefaultRouter
from .views import AdminEnrollmentViewSett

router = DefaultRouter()
router.register("admin-enrollments", AdminEnrollmentViewSett)

urlpatterns = [
    path("my/", MyEnrollmentsView.as_view(), name="my-enrollments"),
    path("create/", EnrollmentCreateView.as_view()),
    path("course/<int:pk>/", CourseDetailView.as_view()),
    
]

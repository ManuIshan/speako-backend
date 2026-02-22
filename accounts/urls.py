from django.urls import path, include
from .views import (
    AdminUserViewSet,
    ChangePasswordView,
    DashboardView,
    RegisterView,
    ProfileView,
    UpdateProfileView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("admin-users", AdminUserViewSet)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("profile/", ProfileView.as_view()),
    path("update-profile/", UpdateProfileView.as_view()),
    path("change-password/", ChangePasswordView.as_view()),
    path("dashboard/", DashboardView.as_view()),
    path("", include(router.urls)), 
]
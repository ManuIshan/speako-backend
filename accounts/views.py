from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    EnrollmentSerializer,
    ChangePasswordSerializer,
)
from enrollments.models import Enrollment
from rest_framework.permissions import IsAuthenticated
from courses.models import Course
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        enrollments = Enrollment.objects.filter(user=user)

        courses = [
            {
                "id": e.course.id,
                "title": e.course.title,
                "category": e.course.category,
                "lessons": e.course.lessons,
                "level": e.course.level,
                "duration": e.course.duration,
                "image": e.course.image.url if e.course.image else None,
                "discount_percent": e.course.discount_percent,
            }
            for e in enrollments if e.status == "approved"
        ]

        payments = [
            {
                "course": e.course.title,
                "payment_id": e.payment_id,
                "status": e.status,
                "date": e.created_at.strftime("%Y-%m-%d"),
            }
            for e in enrollments
        ]

        return Response({
            "username": user.username,
            "email": user.email,
            "profile_picture": user.profile_picture.url if user.profile_picture else None,
            "courses": courses,
            "payments": payments,
        })
class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]



class UpdateProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request):
        user = request.user

        user.username = request.data.get("username", user.username)
        user.email = request.data.get("email", user.email)

        if "profile_picture" in request.FILES:
            user.profile_picture = request.FILES["profile_picture"]

        user.save()

        return Response({"message": "Profile updated successfully"})



class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user

            if not user.check_password(serializer.validated_data["old_password"]):
                return Response(
                    {"error": "Old password incorrect"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(serializer.validated_data["new_password"])
            user.save()

            return Response({"message": "Password updated successfully"})

        return Response(serializer.errors, status=400)

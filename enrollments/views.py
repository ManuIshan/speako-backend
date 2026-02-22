from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView
from django.shortcuts import get_object_or_404
from .models import Enrollment
from .serializers import EnrollmentSerializer
from courses.models import Course
from rest_framework import status   
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets

class CourseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        course = get_object_or_404(Course, id=pk)

        enrolled = Enrollment.objects.filter(
            user=request.user,
            course=course,
            status="approved"
        ).exists()

        data = {
            "id": course.id,
            "title": course.title,
            "description": course.content.description if hasattr(course, "content") else "",
            "pdf": course.content.pdf_file.url if enrolled and hasattr(course, "content") else None,
            "is_unlocked": enrolled
        }

        return Response(data)


class MyEnrollmentsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user)


class EnrollmentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        course_id = request.data.get("course_id")

        if not course_id:
            return Response(
                {"error": "course_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, id=course_id)

        existing = Enrollment.objects.filter(
            user=request.user,
            course=course
        ).first()

        if existing:
            return Response(
                {"message": f"Already enrolled - Status: {existing.status}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        Enrollment.objects.create(
            user=request.user,
            course=course,
            status="pending"
        )

        return Response(
            {"message": "Enrollment request sent successfully"},
            status=status.HTTP_201_CREATED
        )
class AdminEnrollmentViewSett(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAdminUser]


#  manuishan password admin
# username manuish


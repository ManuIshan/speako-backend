from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import random

from .models import Course
from .serializers import CourseSerializer
from enrollments.models import Enrollment
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets

class HomeCourseListView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Course.objects.filter(show_on_home=True)


class AllCourseListView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]
    queryset = Course.objects.all()


class CourseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        course = get_object_or_404(Course, id=pk)

        enrolled = Enrollment.objects.filter(
            user=request.user,
            course=course,
            status="approved"
        ).exists()

        # Ensure content exists
        if not hasattr(course, "content"):
            return Response(
                {"error": "Admin has not added content yet"},
                status=404
            )

        content = course.content

        module_data = [
            {
                "title": m.title,
                "lessons_count": m.lessons_count
            }
            for m in course.modules.all()
        ]

        # Assessments
        assessment_data = [
            {"title": a.title}
            for a in course.assessments.all()
        ]

        # Assessment Images
        image_data = [
            img.image.url
            for img in course.assessment_images.all()
        ]

        # Related Courses
        related_queryset = Course.objects.exclude(id=course.id)
        related_list = list(related_queryset)

        if len(related_list) >= 2:
            related_courses = random.sample(related_list, 2)
        else:
            related_courses = related_list

        related_data = [
            {
                "id": c.id,
                "title": c.title,
                "lessons": c.lessons,
                "level": c.level,
                "duration": c.duration,
                "image": c.image.url if c.image else None,
            }
            for c in related_courses
        ]

        return Response({
            "id": course.id,
            "title": course.title,
            "category": course.category,
            "lessons": course.lessons,
            "level": course.level,
            "duration": course.duration,
            "discount_percent": course.discount_percent,
            "price": course.price,

            "overview": content.overview,
            "pdf": content.pdf_file.url if enrolled else None,
            "is_unlocked": enrolled,

            "modules": module_data,
            "assessments": assessment_data,
            "assessment_images": image_data if enrolled else [],

            "related": related_data
        })
class AdminCourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminUser]

from rest_framework import serializers
from django.contrib.auth import get_user_model
from enrollments.models import Enrollment

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "profile_picture"]

    def create(self, validated_data):
        profile_picture = validated_data.pop("profile_picture", None)

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        if profile_picture:
            user.profile_picture = profile_picture
            user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "profile_picture"]


class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title")
    course_id = serializers.IntegerField(source="course.id")

    class Meta:
        model = Enrollment
        fields = [
            "id",
            "course_id",
            "course_title",
            "status",
            "payment_id",
            "created_at",
        ]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

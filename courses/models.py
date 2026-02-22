from django.db import models


class Course(models.Model):

    CATEGORY_CHOICES = [
        ("essentials", "Essentials"),
        ("exam", "Exam Prep"),
        ("career", "Career Focus"),
        ("skill", "Skill Levels"),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    short_description = models.TextField(blank=True)

    lessons = models.IntegerField()
    level = models.CharField(max_length=50)
    duration = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    discount_percent = models.IntegerField(default=0)

    image = models.FileField(upload_to="courses/", blank=True, null=True)

    show_on_home = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CourseContent(models.Model):
    course = models.OneToOneField(
        Course,
        on_delete=models.CASCADE,
        related_name="content"
    )
    overview = models.TextField()
    pdf_file = models.FileField(upload_to="course_pdfs/")

    def __str__(self):
        return f"Content for {self.course.title}"


class CourseModule(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="modules"
    )
    title = models.CharField(max_length=200)
    lessons_count = models.IntegerField()

    def __str__(self):
        return self.title


class CourseAssessment(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="assessments"
    )
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class AssessmentImage(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="assessment_images"
    )
    image = models.FileField(upload_to="assessment_images/")

    def __str__(self):
        return f"Assessment Image - {self.course.title}"

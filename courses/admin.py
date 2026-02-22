from django.contrib import admin
from .models import (
    Course,
    CourseContent,
    CourseModule,
    CourseAssessment
)

# ---------- INLINE SECTIONS ----------

class CourseContentInline(admin.StackedInline):
    model = CourseContent
    extra = 0

class CourseModuleInline(admin.TabularInline):
    model = CourseModule
    extra = 1

class CourseAssessmentInline(admin.TabularInline):
    model = CourseAssessment
    extra = 1


# ---------- MAIN COURSE ADMIN ----------

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price", "created_at")
    inlines = [
        CourseContentInline,
        CourseModuleInline,
        CourseAssessmentInline,
    ]


# ---------- ALSO REGISTER THEM SEPARATELY ----------

@admin.register(CourseContent)
class CourseContentAdmin(admin.ModelAdmin):
    list_display = ("course",)

@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ("course", "title", "lessons_count")

@admin.register(CourseAssessment)
class CourseAssessmentAdmin(admin.ModelAdmin):
    list_display = ("course", "title")

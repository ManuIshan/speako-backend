from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "created_at")
    list_filter = ("level",)
    search_fields = ("name", "comment")

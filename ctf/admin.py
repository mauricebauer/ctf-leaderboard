from django.contrib import admin
from ctf.models import Content, Flag, Participant, Submission


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("participant", "flag", "created_at")
    list_filter = ("participant", "flag")


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("name", "custom_name")


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("content", "created_at")
    list_filter = ("created_at",)


admin.site.register(Flag)

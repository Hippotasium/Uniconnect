from django.contrib import admin
from .models import Job
from .models import StudentProfile
from .models import Announcement
from .models import MentorshipPost


admin.site.register(StudentProfile)
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'payment', 'post_approved', 'created_at')
    list_filter = ('post_approved', 'created_at')
    search_fields = ('title', 'description', 'requirements', 'contact_information')

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'student_id', 'degree', 'graduation_year', 'role', 'approved')
    list_filter = ('approved', 'degree', 'role')
    search_fields = ('full_name', 'student_id', 'user__email')
    readonly_fields = ('user', 'graduation_certificate')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)

@admin.register(MentorshipPost)
class MentorshipPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'mentor', 'class_date', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'class_date')
    search_fields = ('title', 'mentor__username', 'mentor__email')
    actions = ['approve_posts']

    def approve_posts(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected posts have been approved.")
    approve_posts.short_description = "Approve selected mentorship posts"
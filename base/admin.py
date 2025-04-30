from django.contrib import admin
from .models import Job
from .models import StudentProfile
from .models import Announcement


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
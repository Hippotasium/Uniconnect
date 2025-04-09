from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now  # Import timezone for default values

class StudentProfile(models.Model):
    ROLE_CHOICES = [
        ('Student', 'Student'),
        ('Alumni', 'Alumni'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to Django's User model
    student_id = models.CharField(max_length=20, unique=True, default="default_student_id")  # Default Student ID
    full_name = models.CharField(max_length=100, default="Unknown")  # Default full name
    date_of_birth = models.DateField(default=now)  # Default to current date
    degree = models.CharField(max_length=50, default="Undeclared")  # Default degree
    graduation_year = models.IntegerField(default=2000)  # Default graduation year
    CGPA = models.FloatField(null=True, blank=True, default=0.0)  # Default CGPA
    graduation_certificate = models.FileField(
        upload_to='certificates/', 
        default='certificates/default_certificate.pdf',  # Default certificate file
    )  # Field for uploading certificates (PDF or Image)
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='Student'
    )  # Role field with predefined choices

    # Additional fields
    job_title = models.CharField(max_length=100, blank=True, null=True, default="Unemployed")
    company = models.CharField(max_length=100, blank=True, null=True, default="None")
    industry = models.CharField(max_length=100, blank=True, null=True, default="Unknown")
    tagline = models.CharField(max_length=255, blank=True, null=True, default="No tagline provided")
    location = models.CharField(max_length=100, blank=True, null=True, default="Unknown")
    bio = models.TextField(blank=True, null=True, default="No bio provided")
    work_experience = models.JSONField(blank=True, null=True, default=list)  # Store work experience as JSON
    certifications = models.JSONField(blank=True, null=True, default=list)  # Store certifications as JSON
    skills = models.JSONField(blank=True, null=True, default=list)  # Store skills as JSON
    projects = models.JSONField(blank=True, null=True, default=list)  # Store projects as JSON
    open_to_mentorship = models.BooleanField(default=False)
    offering_referrals = models.BooleanField(default=False)
    awards = models.JSONField(blank=True, null=True, default=list)  # Store awards as JSON
    linkedin = models.URLField(blank=True, null=True, default="https://linkedin.com")
    website = models.URLField(blank=True, null=True, default="https://example.com")
    github = models.URLField(blank=True, null=True, default="https://github.com")
    university_name = models.CharField(max_length=100, blank=True, null=True, default="Unknown")

    def save(self, *args, **kwargs):
        """
        Override the save method to ensure that JSON fields are always lists.
        If an integer or invalid data is provided, it will be converted to a list containing the string representation.
        """
        if not isinstance(self.work_experience, list):
            self.work_experience = [str(self.work_experience)] if self.work_experience else []
        if not isinstance(self.certifications, list):
            self.certifications = [str(self.certifications)] if self.certifications else []
        if not isinstance(self.skills, list):
            self.skills = [str(self.skills)] if self.skills else []
        if not isinstance(self.projects, list):
            self.projects = [str(self.projects)] if self.projects else []
        if not isinstance(self.awards, list):
            self.awards = [str(self.awards)] if self.awards else []
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.student_id})"
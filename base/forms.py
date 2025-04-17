from django import forms
from .models import StudentProfile

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'full_name', 'tagline', 'job_title', 'company', 'industry', 'location', 'bio',
            'work_experience', 'university_name', 'degree', 'graduation_year', 'CGPA',
            'certifications', 'skills', 'projects', 'open_to_mentorship', 'offering_referrals',
            'awards', 'linkedin', 'website', 'github'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'work_experience': forms.Textarea(attrs={'rows': 4}),
            'certifications': forms.Textarea(attrs={'rows': 4}),
            'skills': forms.Textarea(attrs={'rows': 4}),
            'projects': forms.Textarea(attrs={'rows': 4}),
            'awards': forms.Textarea(attrs={'rows': 4}),
        }
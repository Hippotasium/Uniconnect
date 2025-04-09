from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import StudentProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import StudentProfileForm
from base.models import StudentProfile
# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')  # Render the dashboard template
def home(request):
    return render(request, 'home.html')
@login_required
def editprofile(request):
    profile = request.user.studentprofile
    if request.method == 'POST':
        profile.full_name = request.POST.get('full_name', profile.full_name)
        profile.date_of_birth = request.POST.get('date_of_birth', profile.date_of_birth)
        profile.degree = request.POST.get('degree', profile.degree)
        profile.graduation_year = request.POST.get('graduation_year', profile.graduation_year)
        profile.CGPA = request.POST.get('cgpa', profile.CGPA)
        profile.job_title = request.POST.get('job_title', profile.job_title)
        profile.company = request.POST.get('company', profile.company)
        profile.industry = request.POST.get('industry', profile.industry)
        profile.tagline = request.POST.get('tagline', profile.tagline)
        profile.location = request.POST.get('location', profile.location)
        profile.bio = request.POST.get('bio', profile.bio)
        profile.work_experience = [exp.strip() for exp in request.POST.get('work_experience', '').split(',')]
        profile.certifications = [cert.strip() for cert in request.POST.get('certifications', '').split(',')]
        profile.skills = [skill.strip() for skill in request.POST.get('skills', '').split(',')]
        profile.projects = [proj.strip() for proj in request.POST.get('projects', '').split(',')]
        profile.open_to_mentorship = 'open_to_mentorship' in request.POST
        profile.awards = [award.strip() for award in request.POST.get('awards', '').split(',')]
        profile.linkedin = request.POST.get('linkedin', profile.linkedin)
        profile.github = request.POST.get('github', profile.github)
        profile.website = request.POST.get('website', profile.website)
        profile.university_name = request.POST.get('university_name', profile.university_name)
 
       # Save the updated profile

        profile.save()

        # Redirect to the profile page after saving
        return redirect('profile')
    # Render the edit profile page with the current profile data
    return render(request, 'editprofile.html', {'user': request.user})
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')  # Redirect to homepage after logout
    return render(request, 'logout.html')  # Render the logout confirmation page
def profile(request):
    return render(request, 'profile.html')


def login_views(request):
    if request.method == 'POST':
        student_id = request.POST['student_id']  # Fetch Student ID from the form (corrected key)
        password = request.POST['password']  # Fetch password from the form
        try:
            # Find the user associated with the Student ID
            #profile = StudentProfile.objects.get(student_id=student_id)
            user = authenticate(request, username=student_id, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to the dashboard page after successful login
            else:
                messages.error(request, 'Invalid Student ID or password')  # Display error message
        except StudentProfile.DoesNotExist:
            messages.error(request, 'Student ID not found')  # Handle case where Student ID does not exist
    return render(request, 'login.html')  # Render the login page for GET requests

def signup(request):
    if request.method == 'POST':
        # Fetch data from the form
        full_name = request.POST['full_name']
        student_id = request.POST['student_id']
        date_of_birth = request.POST['date_of_birth']
        degree = request.POST['degree']
        graduation_year = request.POST['graduation_year']
        cgpa = request.POST.get('cgpa', None)  # Optional field
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        graduation_certificate = request.FILES.get('graduation_certificate', None)
        role = request.POST['role']  # Fetch the role from the form

        # Validate passwords
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'signup.html')

        # Check if Student ID already exists
        if StudentProfile.objects.filter(student_id=student_id).exists():
            messages.error(request, 'Student ID already exists')
            return render(request, 'signup.html')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'signup.html')

        # Create the user
        try:
            user = User.objects.create_user(username=student_id, email=email, password=password)
            user.first_name = full_name.split()[0]  # Optional: Set first name
            user.save()

            # Create the student profile
            StudentProfile.objects.create(
                user=user,
                student_id=student_id,
                full_name=full_name,
                date_of_birth=date_of_birth,
                degree=degree,
                graduation_year=graduation_year,
                CGPA=cgpa,
                graduation_certificate=graduation_certificate,
                role=role  # Save the role
            )

            # Log the user in and redirect to the home page
            login(request, user)
            messages.success(request, 'Account created successfully')
            return redirect('home')

        except Exception as e:
            messages.error(request, f'Error creating account: {e}')
            return render(request, 'signup.html')

    return render(request, 'signup.html')  # Render the signup page for GET requests

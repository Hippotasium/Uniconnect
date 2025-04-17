from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import StudentProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import StudentProfileForm
from base.models import StudentProfile
from .models import Job
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')  

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
 
      

        profile.save()
        return redirect('profile')
    profile = StudentProfile.objects.get(user=request.user)
    
    user_jobs = Job.objects.filter(poster=request.user)

    return render(request, 'editprofile.html', {
        'profile': request.user,
        'user_jobs': user_jobs  
    })
    


@login_required
def settings(request):
    if request.method == 'POST':
       
        user = request.user
        user.studentprofile.full_name = request.POST.get('full_name')
        user.email = request.POST.get('email')
        user.studentprofile.date_of_birth = request.POST.get('date_of_birth')

        
        
        if 'profile_picture' in request.FILES:
            user.studentprofile.profile_picture = request.FILES['profile_picture']

        
       
        new_student_id = request.POST.get('student_id')
        user.studentprofile.student_id = new_student_id
        user.username = new_student_id  

        user.studentprofile.degree = request.POST.get('degree')
        user.studentprofile.graduation_year = request.POST.get('graduation_year')
        user.studentprofile.CGPA = request.POST.get('cgpa')

   
        if 'graduation_certificate' in request.FILES:
            user.studentprofile.graduation_certificate = request.FILES['graduation_certificate']

       
        password = request.POST.get('password')
        if password:
            user.set_password(password)
            update_session_auth_hash(request, user)  

        
        user.save()
        user.studentprofile.save()

        return redirect('profile')

    return render(request, 'settings.html')



@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home') 
    return render(request, 'logout.html') 


@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def job_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')
        payment = request.POST.get('payment')
        contact_information = request.POST.get('contact_information')

        
        Job.objects.create(
            title=title,
            description=description,
            requirements=requirements,
            payment=payment,
            contact_information=contact_information,
            post_approved=False,
            poster=request.user 
        )

       
        return redirect('job_list')  

    return render(request, 'job_post.html')
@login_required
def job_list(request):
   
    jobs = Job.objects.filter(post_approved=True).order_by('-created_at')
    return render(request, 'job_list.html', {'jobs': jobs})


@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, poster=request.user)
    if job.poster != request.user:
        return HttpResponseForbidden("You are not allowed to delete this job.")
    print("Deleting job:", job.title)


    if request.method == "POST":
        job.delete()
        return redirect('edit_profile')


def login_views(request):
    if request.method == 'POST':
        student_id = request.POST['student_id']  
        password = request.POST['password']  
        try:
           
            profile = StudentProfile.objects.get(student_id=student_id)
            user = authenticate(request, username=student_id, password=password)

            if user is not None:
               
                if not profile.approved:
                    messages.error(request, 'Your account is pending admin approval.')
                    return redirect('login') 
                login(request, user)
                return redirect('dashboard')  
            else:
                messages.error(request, 'Invalid Student ID or password')

        except StudentProfile.DoesNotExist:
            messages.error(request, 'Student ID not found')

    return render(request, 'login.html')


def aboutus(request):
    return render(request, 'aboutus.html')

def signup(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']

        student_id = request.POST['student_id']
        date_of_birth = request.POST['date_of_birth']
        degree = request.POST['degree']
        graduation_year = request.POST['graduation_year']
        cgpa = request.POST.get('cgpa', None)
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        graduation_certificate = request.FILES.get('graduation_certificate')
        role = request.POST['role']
       
       

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'signup.html')

        if StudentProfile.objects.filter(student_id=student_id).exists():
            messages.error(request, 'Student ID already exists')
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'signup.html')

        try:
            user = User.objects.create_user(username=student_id, email=email, password=password)
            user.first_name = full_name.split()[0]
            user.save()

            StudentProfile.objects.create(
                user=user,
                student_id=student_id,
                full_name=full_name,
                date_of_birth=date_of_birth,
                degree=degree,
                graduation_year=graduation_year or 0,
                CGPA=cgpa or 0.0,
                graduation_certificate=graduation_certificate,
                role=role,
                approved=False  
            )

            messages.success(request, 'Account created. Please wait for admin approval.')
            return redirect('login')

        except Exception as e:
            messages.error(request, f'Error creating account: {e}')
            return render(request, 'signup.html')

    return render(request, 'signup.html')
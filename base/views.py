from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse
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
from .models import Notification
from .models import Announcement
from .models import MentorshipPost


@login_required
def dashboard(request):
    profile_url = reverse('profile', args=[request.user.id])  
    return render(request, 'dashboard.html', {'profile_url': profile_url})  

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
        return redirect('profile', user_id=request.user.id)

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

        return redirect('profile', user_id=request.user.id)

    return render(request, 'settings.html')



@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home') 
    return render(request, 'logout.html') 


@login_required
def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.studentprofile  
    return render(request, 'profile.html', {'profile': profile})


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
   
    jobs = Job.objects.filter(post_approved=True).select_related('poster__studentprofile').prefetch_related('interested_users')
    return render(request, 'job_list.html', {'jobs': jobs})

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    
    if job.poster != request.user:
        messages.error(request, "You are not allowed to delete this job.")
        return redirect('dashboard')

    job.delete()
    messages.success(request, "Job deleted successfully.")
    return redirect('dashboard')
    
    
@login_required
def job_detail(request, job_id):
            job = get_object_or_404(Job, id=job_id)
            return render(request, 'job_detail.html', {'job': job})

@login_required
def mark_interest(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.user != job.poster:
        if not job.interested_users.filter(id=request.user.id).exists():
            job.interested_users.add(request.user)

            
            Notification.objects.create(
                user=job.poster,
                message=f"{request.user.studentprofile.full_name} has shown interest in your job post: {job.title}."
            )

            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'message': 'You have already marked interest in this job.'})
    return JsonResponse({'success': False, 'message': 'You cannot mark interest on your own job.'})

@login_required
def interested_users(request, job_id):
    job = get_object_or_404(Job, id=job_id, poster=request.user)
    interested_users = job.interested_users.all()
    return render(request, 'interested_users.html', {'job': job, 'interested_users': interested_users})

@login_required
def notifications(request):
    notifications = request.user.notifications.filter(is_read=False).order_by('-created_at')
    return JsonResponse({'notifications': [
        {'id': n.id, 'message': n.message, 'created_at': n.created_at.strftime('%Y-%m-%d %H:%M:%S')}
        for n in notifications
    ]})

@login_required
def mark_notifications_as_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return JsonResponse({'success': True})

def search(request):
    query = request.GET.get('q', '').strip()
    users = User.objects.filter(studentprofile__full_name__icontains=query) if query else []
    jobs = Job.objects.filter(title__icontains=query) if query else []
    return render(request, 'search_results.html', {'query': query, 'users': users, 'jobs': jobs})

@login_required
def dashboard(request):
    announcements = Announcement.objects.all().order_by('-created_at')[:5]
    user_jobs = Job.objects.filter(poster=request.user).order_by('-created_at')  # Fetch jobs posted by the user
    user_mentorships = MentorshipPost.objects.filter(mentor=request.user).order_by('-created_at')  # Fetch mentorship posts

    return render(request, 'dashboard.html', {
        'announcements': announcements,
        'user_jobs': user_jobs,
        'user_mentorships': user_mentorships,
    })

def announcement_detail(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    return render(request, 'announcement_detail.html', {
        'announcement': announcement,
        'user': request.user, 
    })

@login_required
def mentorship_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        preferred_topics = request.POST.get('preferred_topics')
        class_time = request.POST.get('class_time')
        class_date = request.POST.get('class_date')
        jitsi_meet_link = request.POST.get('jitsi_meet_link')

        # Create a new mentorship post
        MentorshipPost.objects.create(
            title=title,
            description=description,
            preferred_topics=preferred_topics,
            class_time=class_time,
            class_date=class_date,
            jitsi_meet_link=jitsi_meet_link,
            mentor=request.user
        )
        return redirect('dashboard')  

    return render(request, 'mentorship_post.html')


def mentorship_list(request):
    mentorship_posts = MentorshipPost.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, 'mentorship_list.html', {'mentorship_posts': mentorship_posts})


def mentorship_detail(request, mentorship_id):
    mentorship = get_object_or_404(MentorshipPost, id=mentorship_id)
    return render(request, 'mentorship_detail.html', {'mentorship': mentorship})

@login_required
def delete_mentorship(request, mentorship_id):
    mentorship = get_object_or_404(MentorshipPost, id=mentorship_id)

    if mentorship.mentor != request.user:
        return HttpResponseForbidden("You are not allowed to delete this mentorship post.")

    mentorship.delete()
    messages.success(request, "Mentorship post deleted successfully.")
    return redirect('dashboard')

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

   
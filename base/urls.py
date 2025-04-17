from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('login/', views.login_views, name='login'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('job_post/', views.job_post, name='job_post'),
    path('job-list/', views.job_list, name='job_list'),
    path('settings/', views.settings, name='settings'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('delete_job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('editprofile/', views.editprofile, name='editprofile'),
    

    
    
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
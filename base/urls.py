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
    path('editprofile/', views.editprofile, name='editprofile'),
    path('job_post/', views.job_post, name='job_post'),
    path('jobs/', views.job_list, name='job_list'),
    path('settings/', views.settings, name='settings'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('delete_job/<int:job_id>/', views.delete_job, name='delete_job'), 
    path('job/<int:job_id>/interest/', views.mark_interest, name='mark_interest'),
    path('job/<int:job_id>/interested_users/', views.interested_users, name='interested_users'),
     path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark-as-read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),
]

    

    
    


# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
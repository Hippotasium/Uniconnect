from django.urls import path
from . import views 


urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('login/',views.login_views, name='login'),
    path('signup/',views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('profile/', views.profile, name='profile'), 
    path('editprofile/', views.editprofile, name='editprofile')
]


from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='school/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
from django.contrib import admin
from django.urls import path,include
from mySch import views

urlpatterns = [
    path('', views.home,name="home"),
    # path('about', views.about,name="about"),
    # path('event', views.event,name="event"),
    path('contact', views.contact,name="contact"),

     # student list
    path('student_list', views.student_list,name="student_list"),
    path('add_student', views.add_student,name="add_student"),
    path('student_details', views.student_details,name="student_details"),
    path('login_student', views.login_student,name="login_student"),
    path('logout_student', views.logout_student,name="logout_student"),

    # teacher list fatchin
    path('teacher_list', views.teacher_list,name="teacher_list"),
    path('teacher_details', views.teacher_details,name="teacher_details"),
    path('teacher_login', views.teacher_login,name="teacher_login"),
    path('logout_teacher', views.logout_teacher,name="logout_teacher"),

    # for the students attendance
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
    path('view_attendance/', views.view_attendance, name='view_attendance'),
]

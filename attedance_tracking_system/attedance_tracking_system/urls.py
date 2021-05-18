"""student_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from attendance_tracking_app import views, StaffViews, StudentViews
from attedance_tracking_system import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('',views.ShowLoginPage,name="show_login"),
    path('get_user_details', views.GetUserDetails),
    path('logout_user', views.logout_user,name="logout"),
    path('doLogin',views.doLogin,name="do_login"),
                  #     Staff URL Path
    path('staff_home', StaffViews.staff_home, name="staff_home"),
    path('staff_take_attendance', StaffViews.staff_start_lecture, name="staff_take_attendance"),
    path('staff_send_notification_student', StaffViews.staff_send_notification_student,name="staff_send_notification_student"),
    path('send_student_notification/', StaffViews.send_student_notification,name="send_student_notification"),
    path('create_attendance_list/', StaffViews.create_attendance_list,name="create_attendance_list"),
    path('view_all_courses/', StaffViews.view_all_courses,name="view_all_courses"),
    path('view_all_subjects/', StaffViews.view_all_subjects, name="view_all_subjects"),
    path('view_all_students/', StaffViews.view_all_students, name="view_all_students"),

    path('student_home', StudentViews.student_home, name="student_home"),
    path('student_view_attendance', StudentViews.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_post', StudentViews.student_view_attendance_post, name="student_view_attendance_post"),
    path('student_mark_attendance', StudentViews.student_mark_attendance, name="student_mark_attendance"),
    path('student_mark_attendance_check_course', StudentViews.student_mark_attendance_check_course, name="student_mark_attendance_check_course"),
    path('student_all_notification',StudentViews.student_all_notification,name="student_all_notification"),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

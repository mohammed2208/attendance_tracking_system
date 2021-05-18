import json
from datetime import datetime
from uuid import uuid4

from django.contrib import messages
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from attendance_tracking_app.models import Subjects, SessionYearModel, Students, Attendance, \
     Staffs, CustomUser, Courses, CourseCount, NotificationStudent

from datetime import date
import datetime

def staff_home(request):
    user=CustomUser.objects.get(id=request.user.id)
    staff=Staffs.objects.get(admin=user)
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    subject_count=subjects.count()
    return render(request,"staff_template/staff_home_template.html",{"subject_count":subject_count, "user":user,"staff":staff})

def staff_start_lecture(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    return render(request,"staff_template/staff_start_lecture.html",{"subjects":subjects})

def view_all_courses(request):
    courses = Courses.objects.all()
    return render(request,"staff_template/view_all_courses.html",{"courses":courses})

@csrf_exempt 
def view_all_subjects(request):
    subjects = Subjects.objects.filter(course_id=Courses.objects.get(id=request.POST.get("courses")))
    return render(request,"staff_template/view_all_subjects.html",{"subjects":subjects,"course_id":request.POST.get("courses")})

@csrf_exempt
def view_all_students(request):
    students = Students.objects.filter(course_id=Courses.objects.get(id=request.POST.get("course_id")))
    student_list = [] 
    for i in students :
        total_lectures = CourseCount.objects.get(subject_id=Subjects.objects.get(id=request.POST.get("subjects")))
        total_lectures_attended = Attendance.objects.filter(student_id=Students.objects.get(id=i.id)).filter(status=1)
        student = CustomUser.objects.get(id = i.admin_id)
        student_list.append([i.id, student.first_name, student.last_name,len(total_lectures_attended) / total_lectures.count_lectures * 100])
        
    return render(request,"staff_template/view_all_students.html",{"student_list":student_list})

def staff_send_notification_student(request):
    students=Students.objects.all()
    print(students)
    return render(request,"staff_template/student_notification.html",{"students":students})

@csrf_exempt
def send_student_notification(request):
    id=request.POST.get("student_id")
    print(id)
    message=request.POST.get("message")
    student=Students.objects.get(admin_id=id)
    notification=NotificationStudent(student_id=student,message=message)
    notification.save()
    return HttpResponseRedirect(reverse("staff_home"))

@csrf_exempt
def create_attendance_list(request):

    try :
        currentcourse = CourseCount.objects.get(subject_id=request.POST.get("subject"))
        courseid = Subjects.objects.get(id=request.POST.get("subject")).course_id
        if (currentcourse.updated_at != date.today()) :
            currentcourse.updated_at = date.today()
            currentcourse.count_lectures = currentcourse.count_lectures+1
            currentcourse.save()
            students = Students.objects.filter(course_id=courseid)
            for i in students:
                print(i)
                attendance = Attendance(student_id=Students.objects.get(id=i.id), subject_id=Subjects.objects.get(id=request.POST.get("subject")))
                attendance.save()
            messages.success(request, "Successfully Added Attendance Sheet")
        else :
            messages.error(request, "Already Added Attendance Sheet")
    except :
        updatecount = CourseCount(subject_id= Subjects.objects.get(id=request.POST.get("subject")), count_lectures= 1)
        updatecount.save()
        students = Students.objects.all()
        for i in students:
            attendance = Attendance(student_id=Students.objects.get(id=i.id), subject_id=Subjects.objects.get(id=request.POST.get("subject")))
            attendance.save()
        messages.success(request, "Successfully Added Attendance Sheet 2")
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    return render(request,"staff_template/staff_start_lecture.html",{"subjects":subjects})
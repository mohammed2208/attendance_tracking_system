import datetime

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

from attendance_tracking_app.models import Students, Courses, Subjects, CustomUser, Attendance, CourseCount,\
     NotificationStudent


def student_home(request):
    student_obj=Students.objects.get(admin=request.user.id)
    attendance_total=Attendance.objects.filter(student_id=student_obj).count()
    attendance_present=Attendance.objects.filter(student_id=student_obj,status=True).count()
    attendance_absent=Attendance.objects.filter(student_id=student_obj,status=False).count()
    course=Courses.objects.get(id=student_obj.course_id.id)
    subjects=Subjects.objects.filter(course_id=course).count()
    subjects_data=Subjects.objects.filter(course_id=course)
    user=CustomUser.objects.get(id=request.user.id)
    student=Students.objects.get(admin=user)
    return render(request,"student_template/student_home_template.html",{"total_attendance":attendance_total,"attendance_absent":attendance_absent,"attendance_present":attendance_present,"subjects":subjects, "user":user,"student":student})



def student_view_attendance(request):
    student=Students.objects.get(admin=request.user.id)
    course=student.course_id
    subjects=Subjects.objects.filter(course_id=course)
    return render(request,"student_template/student_view_attendance.html",{"subjects":subjects})

def student_view_attendance_post(request):
    subject_id=request.POST.get("subject")
    student=Students.objects.get(admin=request.user.id)
    attendance = Attendance.objects.filter(student_id=student.id, subject_id=subject_id)
    subject = Subjects.objects.get(id = subject_id)
    total_lectures = CourseCount.objects.get(subject_id=Subjects.objects.get(id=subject_id))
    total_lectures_attended = Attendance.objects.filter(student_id=student.id).filter(status=1)
    percentange = len(total_lectures_attended) / total_lectures.count_lectures * 100
    return render(request,"student_template/student_attendance_data.html", {"attendance_reports":attendance, "percentage": percentange, "subject": subject})

def student_mark_attendance(request):
    student=Students.objects.get(admin=request.user.id)
    course=student.course_id
    subjects=Subjects.objects.filter(course_id=course)
    return render(request,"student_template/student_mark_attendance.html",{"subjects":subjects})

def student_mark_attendance_check_course(request):
    student=Students.objects.get(admin=request.user.id)
    subject_id=request.POST.get("subject")
    subject = Subjects.objects.get(id=subject_id)
    is_lecture = CourseCount.objects.get(subject_id=subject_id)
    lecture_date = is_lecture.updated_at
    if lecture_date == datetime.date(datetime.now()):
        attendance = Attendance.objects.filter(student_id=student.id, subject_id=subject_id, status=False, attendance_date=datetime.date(datetime.now()))
        if attendance:
            Attendance.objects.filter(student_id=student.id, subject_id=subject_id, attendance_date=datetime.date(datetime.now())).update(status= True)
            attendance = Attendance.objects.filter(student_id=student.id, subject_id=subject_id)
            return render(request,"student_template/student_attendance_data.html", {"attendance_reports":attendance})
        else:
            return render(request, "student_template/student_attendance_already_marked.html", {"subjects" : subject,  "student": student})
    return render(request, "student_template/student_no_lecture.html", {"subjects" : subject })

def student_all_notification(request):
    student=Students.objects.get(admin=request.user.id)
    notifications=NotificationStudent.objects.filter(student_id=student.id)
    return render(request,"student_template/all_notification.html",{"notifications":notifications})


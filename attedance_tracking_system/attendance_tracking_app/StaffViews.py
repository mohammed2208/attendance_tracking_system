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
     Staffs, CustomUser, Courses, NotificationStaffs, CourseCount, NotificationStudent

from datetime import date
import datetime
def staff_home(request):
    #For Fetch All Student Under Staff
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    course_id_list=[]
    for subject in subjects:
        course=Courses.objects.get(id=subject.course_id.id)
        course_id_list.append(course.id)

    final_course=[]
    #removing Duplicate Course ID
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)

    students_count=Students.objects.filter(course_id__in=final_course).count()

    #Fetch All Attendance Count
    attendance_count=Attendance.objects.filter(subject_id__in=subjects).count()

    #Fetch All Approve Leave
    staff=Staffs.objects.get(admin=request.user.id)
    # leave_count=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
    subject_count=subjects.count()

    #Fetch Attendance Data by Subject
    subject_list=[]
    attendance_list=[]
    for subject in subjects:
        attendance_count1=Attendance.objects.filter(subject_id=subject.id).count()
        subject_list.append(subject.subject_name)
        attendance_list.append(attendance_count1)
   
    return render(request,"staff_template/staff_home_template.html",{"students_count":students_count,"subject_count":subject_count,"subject_list":subject_list,"attendance_list":attendance_list})

def staff_take_attendance(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    # session_years=SessionYearModel.object.all()
    return render(request,"staff_template/staff_start_lecture.html",{"subjects":subjects})





def staff_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    staff=Staffs.objects.get(admin=user)
    return render(request,"staff_template/staff_profile.html",{"user":user,"staff":staff})

def staff_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()

            staff=Staffs.objects.get(admin=customuser.id)
            staff.address=address
            staff.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("staff_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("staff_profile"))

@csrf_exempt
def staff_fcmtoken_save(request):
    token=request.POST.get("token")
    try:
        staff=Staffs.objects.get(admin=request.user.id)
        staff.fcm_token=token
        staff.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

    #     return HttpResponse("ERR")
def view_all_courses(request):

    courses = Courses.objects.all()
    return render(request,"staff_template/view_all_courses.html",{"courses":courses})

@csrf_exempt 
def view_all_subjects(request):

    subjects = Subjects.objects.filter(course_id=Courses.objects.get(id=request.POST.get("courses")))
    for i in subjects :
        print(i.subject_name)
    return render(request,"staff_template/view_all_subjects.html",{"subjects":subjects,"course_id":request.POST.get("courses")})

@csrf_exempt
def view_all_students(request):
    print(request.POST.get("course_id"))
    students = Students.objects.filter(course_id=Courses.objects.get(id=request.POST.get("course_id")))
    student_list = [] 
    for i in students :
        total_lectures = CourseCount.objects.get(subject_id=Subjects.objects.get(id=request.POST.get("subjects")))
        total_lectures_attended = Attendance.objects.filter(student_id=Students.objects.get(id=i.id)).filter(status=1)
        print(total_lectures.count_lectures, len(total_lectures_attended))
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
    # token=student.fcm_token
    # url="https://fcm.googleapis.com/fcm/send"
    # body={
    #     "notification":{
    #         "title":"Student Management System",
    #         "body":message,
    #         "click_action": "https://studentmanagementsystem22.herokuapp.com/student_all_notification",
    #         "icon": "http://studentmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
    #     },
    #     "to":token
    # }
    # headers={"Content-Type":"application/json","Authorization":"key=SERVER_KEY_HERE"}
    # data=requests.post(url,data=json.dumps(body),headers=headers)
    notification=NotificationStudent(student_id=student,message=message)
    notification.save()
    # print(data.text)
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
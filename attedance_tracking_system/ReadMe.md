# AttendSheet
## Attendance Tracking Application

AttendSheet is an attendance tracking posting web application. Technology Stack used to develop this easy to use application is - 

 - DataBase - MySQL
 - Backend - Django Framework
 - Frontend - HTML, CSS, JavaScript

## Roles:
- Student
- Staff

## Features

### Staff
- Login into the Staff Portal
- View Attendance - After selecting the course and the subject, the teacher can see the attendance percentage for all the students enrolled in the selected course and subject.
- Start Lecture - Teacher can start lecture for a subject, enabling the students to mark the attendance for that subject for the day.
- Send Notification - Teacher can send some message to a particular student.

### Student
- Login into the Student Portal
- View Attendance - After selecting the subject, student can see the attendance percentage along with the dates he was absent/present on for the selected subject.
- Mark Attendance - After selecting the subject, student can mark the attendance for the subject only if the lecture is commenced today (i.e. the teacher has started the lecture on the portal) and if he has not marked it earlier. The student can mark their attendance only once for the day.
- View Notification - Student can see all the messages sent to him by the teachers.

## Requirements
- Django
- MySQL

## Usage 

#### Clone it
```sh
git clone https://github.com/mohammed2208/attendance_tracking_system.git
```
#### Create a databse on mysql commandline
```sh
create database student_managment_system;
```
#### Create a user and grant all permisions on mysql commandline
```sh
create user 'mohammed2208'@'localhost' identified by 'student_managment_password';
grant all privileges on *.* to 'mohammed2208';
```
#### Go into the project directory and run the commands:
- To migrate the database
```sh
python manage.py makemigrations
python manage.py migrate
```
- To run the web-application locally
```sh
python manage.py runserver
```

- Use the application by navigating to your server address in
your preferred browser.

```sh
127.0.0.1:8000/
```

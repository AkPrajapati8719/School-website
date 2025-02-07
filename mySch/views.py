from django.shortcuts import render, redirect, get_object_or_404
from mySch.models import Contact
from mySch.models import Student
from mySch.models import *
from .models import Teacher

# for login forms only
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
# from .models import StudentAuth

# for the attendance of the students
from .models import Student, Attendance
from datetime import date, timedelta

# for the attendance 
from .models import Attendance
from datetime import date

# Create your views here.

def home(request):
    return render(request,'index.html')
# event gallary here
def event_gallary(request):
    return render(request,'event-gallary.html')
# sport gallary here
def sport_gallary(request):
    return render(request,'sport-gallary.html')
# alumni gallary here
def alumni_gallary(request):
    return render(request,'alumni-gallary.html')
# about here
# def about(request):
#     return render(request,'about.html')
# # our events
# def event(request):
#     return render(request,'event.html')
# contact us
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        contact = Contact(name=name, mobile=mobile)
        contact.save()
    return render(request,'index.html')

# for adding a student into the studen_tlist

def add_student(request):
    if request.method == 'POST':
        # Get data from the POST request
        name = request.POST.get('name')
        father_name = request.POST.get('father_name')
        contact = request.POST.get('contact')
        student_id = request.POST.get('student_id')
        student_class = request.POST.get('student_class')
        total_fees = request.POST.get('total_fees')
        paid_fees = request.POST.get('paid_fees')
        due_fees = request.POST.get('due_fees')
        age = int(request.POST.get('age'))
        monthly_result= request.POST.get('monthly_result')
        # Handle file upload for result_photo
        result_photo = request.FILES.get('result_photo')  # Assuming it's in the form

        # Create a new student instance and save it to the database
        student = Student(
            name=name,
            father_name=father_name,
            contact=contact,
            student_id=student_id,
            student_class=student_class,
            total_fees=total_fees,
            paid_fees=paid_fees,
            due_fees=due_fees,
            age=age,
            result_photo=result_photo,
            monthly_result=monthly_result # Ensure this field is included in the form
        )
        student.save()  
        
        # Add success message
        messages.success(request, 'Student added successfully!')
        
        return redirect('student_list')  # Redirect to a student list page or similar

    return render(request, 'add-student.html')


# list of the students on database
def student_list(request):
    student_list = Student.objects.all()
    context = {
        'student_list':student_list
    }
    return render(request,'student-list.html',context)

# student login pageget
def login_student(request):
    if request.method == 'POST':
        student_id = request.POST.get('studentId')
        password = request.POST.get('password')
        
        # Authenticate using student_id instead of username
        user = authenticate(request, username=student_id, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('student_details')
        else:
            messages.error(request, "Invalid Student ID or Password.")
    
    return render(request,'login_student.html')


# for showing the details of the student
@login_required
def student_details(request):
    if request.user.is_authenticated:
        try:
            # Fetch student data based on the logged-in username
            student = Student.objects.get(student_id=request.user.username)

            # Fetch the attendance records for the student
            attendance_records = Attendance.objects.filter(student=student)

            # Pass the student and their attendance records to the template
            return render(request, 'student_details.html', {
                'student': student,
                'attendance_records': attendance_records
            })
        except Student.DoesNotExist:
            # If no student is found with the logged-in username, try fetching teacher data
            try:
                teacher = Teacher.objects.get(teacher_id=request.user.username)
                return redirect('login_student')  # Redirect to the login page if it's a teacher
            except Teacher.DoesNotExist:
                # If neither a student nor a teacher is found, redirect to the login page
                return redirect('login_student') 
    else:
        return redirect('login_student')  # Redirect if not logged in

# log out page to the student
@login_required
def logout_student(request):
    logout(request)
    return render(request,'login_student.html')


# fetching teacher list here

def teacher_list(request):
    teacher_list =Teacher.objects.all()
    context = {
        'teacher_list':teacher_list
    }
    return render(request,'teacher-list.html',context)

# Teacher Login 
def teacher_login(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacherId')
        password = request.POST.get('password')
        
        # Authenticate using student_id instead of username
        user = authenticate(request, username=teacher_id, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('teacher_details')
        else:
            messages.error(request, "Invalid Student ID or Password.")
    
    return render(request,'teacher_login.html')

@login_required

def teacher_details(request):
    if request.user.is_authenticated:
        try:
            # Try to fetch teacher data based on the logged-in username (teacher_id)
            teacher = Teacher.objects.get(teacher_id=request.user.username)
            return render(request, 'teacher_details.html', {'teacher': teacher})
        except Teacher.DoesNotExist:
            # If no teacher is found with the logged-in username, try fetching student data
            try:
                student = Student.objects.get(student_id=request.user.username)
                return redirect('teacher_login')  # Redirect to the login page if it's a student
            except Student.DoesNotExist:
                # If neither a teacher nor a student is found, redirect to the login page
                return redirect('teacher_login') 
    else:
        return redirect('teacher_login')  # Redirect to login p
    
# teacher logout from the details page

@login_required
def logout_teacher(request):
    logout(request)
    return render(request,'teacher_login.html')

# View for marking attendance

def mark_attendance(request):
    if request.method == 'POST' and 'mark_attendance' in request.POST:
        student_class = request.POST.get('student_class')
        students = Student.objects.filter(student_class=student_class)

        # Mark attendance for the selected students
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status:
                # Create or update attendance record
                Attendance.objects.create(
                    student=student,
                    status=status
                )

        return redirect('mark_attendance')  # Redirect back to the same page after marking attendance

    # Handle GET request (show the form)
    class_selected = request.GET.get('class', '1st')  # Default to 1st class if not selected
    students = Student.objects.filter(student_class=class_selected)

    return render(request, 'mark_attendance.html', {
        'students': students,
        'class': class_selected
    })

# View for viewing attendance
def view_attendance(request):
    class_selected = request.GET.get('class', '1st')  # Default to '1st' if no class is specified
    period = request.GET.get('period', 'weekly')  # Default to 'weekly'
    school_days = int(request.GET.get('school_days', 0))  # Get the number of school days from input

    # Get today's date
    today = date.today()

    # Determine the start and end date based on the selected period
    if period == 'weekly':
        start_date = today - timedelta(days=today.weekday())  # Start of this week (Monday)
        end_date = start_date + timedelta(days=6)  # End of this week (Sunday)
    elif period == 'monthly':
        start_date = today.replace(day=1)  # Start of this month
        # Handle month end case by calculating next month's first day
        if today.month == 12:
            end_date = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_date = today.replace(month=today.month + 1, day=1) - timedelta(days=1)  # End of this month
    else:  # 'yearly'
        start_date = today.replace(month=1, day=1)  # Start of this year
        end_date = today.replace(month=12, day=31)  # End of this year

    # Fetch attendance records for the selected class and date range
    attendance_records = Attendance.objects.filter(
        student__student_class=class_selected,
        date__range=[start_date, end_date]
    ).order_by('student', 'date')

    # Group attendance records by student
    grouped_attendance = {}
    for record in attendance_records:
        if record.student.id not in grouped_attendance:
            grouped_attendance[record.student.id] = []
        grouped_attendance[record.student.id].append(record)

    students = Student.objects.filter(student_class=class_selected)

    # Calculate attendance percentage based on school days
    attendance_percentages = {}
    for student_id, records in grouped_attendance.items():
        total_school_days = school_days  # Number of school days entered by user
        present_days = sum(1 for record in records if record.status == 'P')
        attendance_percentages[student_id] = (present_days / total_school_days) * 100 if total_school_days > 0 else 0

    # Render the template with necessary context
    return render(request, 'view_attendance.html', {
        'students': students,
        'class': class_selected,
        'attendance_records': grouped_attendance,
        'attendance_percentages': attendance_percentages,
        'period': period,
        'school_days': school_days,
        'start_date': start_date,
        'end_date': end_date,
    })

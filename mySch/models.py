from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=122)
    mobile = models.CharField(max_length=12)

    def __str__(self):
        return self.name
    
# student details


class Student(models.Model):
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    student_id = models.CharField(max_length=30)
    student_class = models.CharField(max_length=50)
    total_fees = models.DecimalField(max_digits=10, decimal_places=2)
    paid_fees = models.DecimalField(max_digits=10, decimal_places=2)
    due_fees = models.DecimalField(max_digits=10, decimal_places=2)
    age = models.IntegerField()
    result_photo = models.ImageField(upload_to='result_photos/', null=True, blank=True)  # Add result photo field
    monthly_result = models.IntegerField()
    def __str__(self):
        return f"{self.name} {self.student_id}"


# the teacher details 
class Teacher(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    teacher_id = models.CharField(max_length=30)
    subject = models.CharField(max_length=15)
    joining_date = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    qualification = models.CharField(max_length=50)
    address= models.CharField(max_length=100)
    identity= models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return f"{self.name} {self.teacher_id}"

# attendance of the students 
   
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=1, choices=[('P', 'Present'), ('A', 'Absent'), ('L', 'Leave')])

    def __str__(self):
        return f"Attendance for {self.student.name} class {self.student.student_class}on {self.date} - {self.status}"
    
# teacher attendace 
class Teacher_Attendance(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)  # Reference to the Teacher model
    date = models.DateField(default=timezone.now)  # The date of attendance
    status = models.CharField(
        max_length=1, 
        choices=[('P', 'Present'), ('A', 'Absent'), ('L', 'Leave')],  # Attendance status options
    )

    def __str__(self):
        return f"Attendance for {self.teacher.name} {self.teacher.teacher_id} on {self.date} - {self.get_status_display()}"

# Assuming the Student and Teacher models are already defined as shown in the original code

class Account(models.Model):
    # Define choices for 'identity' to distinguish between student or teacher
    STUDENT = 'student'
    TEACHER = 'teacher'
    IDENTITY_CHOICES = [
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
    ]
    
    # General fields for the Account model
    name = models.CharField(max_length=100)
    account_id = models.CharField(max_length=50, unique=True)
    identity = models.CharField(max_length=10, choices=IDENTITY_CHOICES) 
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2) 
    due_amount = models.DecimalField(max_digits=10, decimal_places=2)  
    date = models.DateTimeField(auto_now_add=True) 
    
    # Linking to Student or Teacher based on identity
    student = models.ForeignKey('Student', null=True, blank=True, on_delete=models.CASCADE)  
    teacher = models.ForeignKey('Teacher', null=True, blank=True, on_delete=models.CASCADE)  
    
    def save(self, *args, **kwargs):
        # Ensure either the student or teacher is filled based on identity
        if self.identity == self.STUDENT:
            self.teacher = None 
        elif self.identity == self.TEACHER:
            self.student = None 
        super(Account, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.identity}) - {self.account_id}"

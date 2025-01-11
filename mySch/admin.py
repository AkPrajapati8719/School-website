from django.contrib import admin
from mySch.models import Contact
from mySch.models import Student
from mySch.models import Teacher
from mySch.models import Attendance
from mySch.models import Account
# from mySch.models import StudentAuth

# Register your models here.
admin.site.register(Contact)
# admin.site.register(Student)
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'father_name', 'contact', 'student_id', 'student_class', 'total_fees', 'paid_fees', 'due_fees','age')
    search_fields = ('name', 'student_id')
    list_filter = ('student_class', 'age')

# admin.site.register(Teacher)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher_id', 'subject', 'joining_date', 'salary','contact','qualification','address','identity','age')
    search_fields = ('name', 'teacher_id')
    ordering = ('name',)

# admin.site.register(Attendance)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status')
    list_filter = ('date', 'status')
    search_fields = ('student__name', 'student__student_id')
    ordering = ('-date',)
# admin.site.register(Account)

@admin.register(Account)
class Account(admin.ModelAdmin):
    list_display = ('name','account_id','identity','total_amount','paid_amount','due_amount', 'date')
    list_filter = ( 'account_id','name','identity')
    search_fields = ('name', 'account_id','identity')
    ordering = ('-date',)


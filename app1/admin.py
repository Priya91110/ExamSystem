from django.contrib import admin
from . models import Student

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    model = Student 
    fields = ['enrollment_number','dob','name']

admin.site.register(Student, StudentAdmin)
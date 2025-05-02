from django.contrib import admin
from . models import Student, Question, Result

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    model = Student 
    fields = ['enrollment_number','dob','name']


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    fields = [
    'text',
    'option_a', 
    'option_b',
    'option_c',
    'option_d', 
    'correct_answer']


class StudentResult(admin.ModelAdmin):
    model = Result
    fields = ['student', 'score']  
    readonly_fields = ['submitted_at']  
    
admin.site.register(Student, StudentAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Result, StudentResult)
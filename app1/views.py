from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "app1/index.html")


# views.py
from django.shortcuts import render, redirect
from .forms import LoginForm
from .models import Student

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            enrollment = form.cleaned_data['enrollment_number']
            dob = form.cleaned_data['dob']
            try:
                student = Student.objects.get(enrollment_number=enrollment, dob=dob)
                # Store student id in session
                request.session['student_id'] = student.id
                # Optional: Set session expiry to 1 hour
                request.session.set_expiry(3600)  # 1 hour
                return redirect('instructions')  # After successful login
            except Student.DoesNotExist:
                form.add_error(None, 'Invalid Enrollment Number or DOB')
    else:
        form = LoginForm()
    return render(request, 'app1/login.html', {'form': form})


def instructions_view(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')

    student = Student.objects.get(id=student_id)
    return render(request, 'app1/instructions.html', {'student_name': student.name})


def logout_view(request):
    # Logout user and flush the session data
    request.session.flush()  # Clears all session data
    return redirect('login')  # Redirect to login page


# views.py

from django.shortcuts import render, redirect
from .models import Student, Question, Answer, Result
from django.utils import timezone

def instructions_view(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    
    student = Student.objects.get(id=student_id)
    return render(request, 'app1/instructions.html', {'student_name': student.name})
'''
def start_exam_view(request):
    print("hello")
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')

    student = Student.objects.get(id=student_id)
    questions = Question.objects.all()

    if request.method == 'POST':
        for question in questions:
            qid = str(question.id)
            answer_value = request.POST.get(f'question_{qid}')
            if answer_value:
                Answer.objects.update_or_create(
                    student=student,
                    question=question,
                    defaults={'selected_answer': answer_value.upper()}
                )
        return redirect('submit_exam')

    return render(request, 'app1/start_exam.html', {'questions': questions})
'''
def start_exam_view(request):
    print("onstart exam")
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')

    student = Student.objects.get(id=student_id)

    # If this is the POST request from the instructions page, save the selected test
    if request.method == 'POST' and 'test' in request.POST:
        selected_test = request.POST.get('test')
        request.session['selected_test'] = selected_test
        print("Test selected and saved to session:", selected_test)
    else:
        selected_test = request.session.get('selected_test')

    print("Selected Test from session:", selected_test)

    questions = Question.objects.filter(subject=selected_test)
    print(f"Found {questions.count()} questions for subject: {selected_test}")

    # If POST (submitting answers), handle that
    if request.method == 'POST' and 'test' not in request.POST:
        for question in questions:
            qid = str(question.id)
            answer_value = request.POST.get(f'question_{qid}')
            if answer_value:
                Answer.objects.update_or_create(
                    student=student,
                    question=question,
                    defaults={'selected_answer': answer_value.upper()}
                )

    return render(request, 'app1/start_exam.html', {'questions': questions})



def submit_exam_view(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')

    student = Student.objects.get(id=student_id)
    answers = Answer.objects.filter(student=student)
    score = 0

    for answer in answers:
        if answer.selected_answer == answer.question.correct_answer:
            score += 1

    Result.objects.update_or_create(
        student=student,
        defaults={'score': score, 'submitted_at': timezone.now()}
    )

    return redirect('thank_you')

def thank_you_view(request):
    return render(request, 'app1/thank_you.html')



import csv
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Question

# @login_required
def upload_questions_view(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        subject = request.POST.get('subject')

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a CSV file.')
            return redirect('upload_questions')

        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:
            Question.objects.create(
                subject=subject,
                text=row['text'],
                option_a=row['option_a'],
                option_b=row['option_b'],
                option_c=row['option_c'],
                option_d=row['option_d'],
                correct_answer=row['correct_answer'].upper()
            )

        messages.success(request, 'Questions uploaded successfully!')
        return redirect('home')

    return render(request, 'app1/upload_questions.html')

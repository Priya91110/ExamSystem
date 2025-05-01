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

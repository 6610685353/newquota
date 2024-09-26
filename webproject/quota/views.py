from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student
from .models import Course
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import admin


def all_student(request):
    all_student = Student.objects.all()  # Fix to use 'objects'
    return render(request, "login.html", {"all_student": all_student})


def login_view(request):
    if request.method == "POST":  # Check if the method is POST
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.get_username() == 'admin':
                return redirect('admin/')
            else:
                login(request, user)
                messages.success(request, "Login successful!")  # Success message
                return redirect('index')  # Redirect to the next page or the default
        else:
            messages.error(request, "Invalid username or password.")  # Error message
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


@login_required
def index_view(request):
    all_courses = Course.objects.all()
    return render(request, "index.html", {"all_courses" : all_courses})  # Replace with your actual index template


@login_required
def academic_year(request):
    return render(request, "academic_year.html")


@login_required
def course_details(request):
    courses = Course.objects.all()  # Fetch all courses
    return render(request, "course_details.html", {"course": courses})


@login_required
def quota_status(request):
    return render(request, "quota_status.html")


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)

    return redirect("login")  # Redirect to login page after logging out


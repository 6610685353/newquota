from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse

from quota.models import Student
from .models import Course


def all_students(request):
    all_students = Student.objects.all()  # Correct to plural
    return render(request, "login.html", {"all_students": all_students})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.get_username() == "admin":
                return redirect(
                    reverse("admin:index")
                )  # Use reverse to redirect to admin
            else:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect("index")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


@login_required
def index_view(request):
    all_courses = Course.objects.all()
    try:
        enrolled_courses = request.user.student.courses.all()
    except Student.DoesNotExist:
        enrolled_courses = []
    return render(
        request,
        "index.html",
        {"all_courses": all_courses, "enrolled_courses": enrolled_courses},
    )


@login_required
def academic_year(request):
    return render(request, "academic_year.html")


@login_required
def course_details(request):
    all_courses = Course.objects.all()
    return render(
        request, "course_details.html", {"all_courses": all_courses}
    )  # Fixed key


@login_required
def quota_status(request):
    return render(request, "quota_status.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")


@login_required
def enroll_view(request, course_id):
    student = get_object_or_404(Student, user=request.user)
    course = get_object_or_404(Course, id=course_id)

    # Check if the course is already full or if the student is already enrolled
    if course.full:
        messages.error(request, "This course is full.")
        return redirect("course_index")

    if student in course.enrolled_students.all():  # Check if already enrolled
        messages.error(request, "You are already enrolled in this course.")
        return redirect("quota_status")

    # Enroll the student in the course
    course.enrolled_students.add(student)
    course.course_remain -= 1  # Decrease available seats
    if course.course_remain <= 0:
        course.full = True  # Mark course as full if no seats remain
    course.save()

    messages.success(request, f"Successfully enrolled in {course.course_name}!")
    return redirect("quota_status")


def withdraw_view(request, course_id):
    student = get_object_or_404(Student, user=request.user)
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        # Remove the student from the course
        course.enrolled_students.remove(student)
        course.course_remain += 1  # Increase available seats by 1
        if course.course_remain > 0:
            course.full = False  # Set course as not full
        course.save()

        messages.success(request, f"Successfully withdrawn from {course.course_name}.")
        return redirect("quota_status")

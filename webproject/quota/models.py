from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django import forms
from django.contrib.auth.models import User

# Create your models here.


class Student(models.Model):
    username = models.CharField(max_length=10, unique=True) 
    password = models.CharField(
        max_length=20
    )  
    name = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.password = make_password(self.password)
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} {self.name}"

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class Course(models.Model):
    course_code = models.CharField(max_length=6)
    course_name = models.CharField(max_length=80)
    course_detail = models.CharField(max_length=1000)
    course_credit = models.IntegerField()
    course_section = models.CharField(max_length=6)
    course_remain = models.IntegerField(default=0)
    full = models.BooleanField(default=False)
    students = models.ManyToManyField('Student', blank=True)

    SEMESTER_CHOICES = [("1", "1"), ("2", "2")]
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES)
    year = models.CharField(max_length=4, null=True) 


    class Meta:
        ordering = ["course_code"]

    def str(self):
        return f"{self.course_code} - {self.course_name}"
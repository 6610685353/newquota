from django.contrib import admin
from quota.models import Student, Course

class CourseAdmin(admin.ModelAdmin):
    list_display = [
        "course_code",
        "course_name",
        "course_section",
        "course_credit",
        "course_remain",
        "full",
    ]
    list_filter = ["full"]
    search_fields = [
        "course_code",
        "course_name",
    ]


admin.site.register(Course, CourseAdmin)
admin.site.register(Student)


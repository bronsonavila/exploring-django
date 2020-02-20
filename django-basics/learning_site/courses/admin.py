from django.contrib import admin

from .models import Course, Step


# Create an `inline` (the form within the form).
# Inlines may be either `stacked` or `tabular`.
class StepInline(admin.StackedInline):
    model = Step


# Create `admin` for customizing Courses.
class CourseAdmin(admin.ModelAdmin):
    inlines = [StepInline,]


admin.site.register(Course, CourseAdmin)
admin.site.register(Step) # Could be deleted.

from django.db import models


# The Course class inherits from `models.Model`.
class Course(models.Model):
    # Set value automatically to current time when a record is first created.
    # The current time is determined by the `TIME_ZONE` value in `settings.py`.
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()

    # "Dunder string" defines how an instance is turned into a string. This is
    # used when Django prints a reference to an instance (e.g., in the shell).
    # Can return something more informative than <Course: Course object (3)>.
    def __str__(self):
        return self.title


class Step(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    # `blank` refers to the form in the admin menu (i.e., allowed to be empty).
    content = models.TextField(blank=True, default='')
    order = models.IntegerField(default=0)
    # Establish a many-to-one relationship where many steps belong to one course.
    # If the Course class appeared after Step, then "Course" must be in quotes.
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE, # Delete child tables.
    )

    # Django models have the `Meta` class as an option to control
    # the model's behavior.
    class Meta:
        # Order all records by the `order` attribute, and then
        # fall back to using the `id` if the same `order` is used.
        ordering = ['order',]

    def __str__(self):
        return self.title

# Exploring Django

## Regular Expressions in Python

### Introduction to Regular Expressions

#### Reading Files

- Use the `open()` function to open a file by passing a file name as an argument. You can also specify an optional encoding value:

  ```python
  names_file = open('names.txt', encoding='utf-8')
  ```

  - The value of `names_file` variable will not be the contents of the file. Rather, it is a pointer to the file on the file system that can be interacted with in some way (e.g., read, close, etc.).

- Use the `read()` function to read the contents of a file:

  ```python
  data = names_file.read()
  ```

- Use the `close()` function after reading a file to free up system memory that had been pointing to the open file:

  ```python
  names_file.close()
  ```

- After fetching data from the file, you can use Python's `re` module to perform regular expression matching. Import the module at the top the Python file:

  ```python
  import re
  ```

- Use the `re.match()` method to find the first matching text at the ***beginning*** of a string:

  ```python
  print(re.match(r'Love', data))
  ```

  - The `r` in front of the first string argument indicates that it is a **raw string literal** (where, e.g., a `'\'` is just a *backslash* instead of an *escape character*).

- Use the `re.search()` method to find the first matching text ***anywhere*** in a string:

  ```python
  print(re.search(r'Kenneth', data))
  ```

#### Escape Hatches

- `\w` : Any Unicode **word character** (i.e., all letters, numbers, and the underscore).
- `\W` : Anything that is *not* a Unicode word character.
- `\s` : Any **whitespace character** (e.g., spaces, tabs, newlines, etc.).
- `\S` : Anything that is *not* a whitespace character.
- `\d` : Any **number** from 0 to 9.
  - **NOTE:** When working with phone numbers with an area code, be aware that **parentheses** have a special meaning in regex (as a grouping character), so they must be escaped by using a preceding backslash `'\'`.
- `\D` : Anything that is *not* a number.
- `\b` : A **word boundary**, which may be any of the following three positions (not necessarily just white space or the screen edge):
  - Before the first character in the string, if the first character is a word character.
  - After the last character in the string, if the last character is a word character.
  - Between two characters in the string, where one *is* a word character and the other is *not* a word character.
- `\B` : Anything that is *not* a word boundary.

#### Counts

+ Types:
  - `{`*`n`*`}` : Occurs *exactly* *n* times.
  - `{,`*`n`*`}` : Occurs *from 0* to *n* times.
  - `{`*`n`*`,}` : Occurs *n or more* times.
  - `{`*`n`*`,`*`p`*`}` : Occurs *from n to p* times.
  - `?` : Occurs *0 or 1* times.
  - `*` : Occurs *at least 0* times.
  - `+` : Occurs *at least once*.

- Use the `re.findall()` method to find ***all*** matching text anywhere in a string.

- **Examples**:

  ```python
  re.search(r'\w+, \w+', data) # Finds, e.g., "last name, first name" pair.
  re.findall(r'\(?\d{3}\)?-?\s?\d{3}-\d{4}', data) # Finds all phone numbers.
  ```

#### Sets

- Sets are defined with **square brackets**. They are used to combine explicit characters and escape patterns into pieces that can be repeated multiple times. They also are used to specify pieces that should be left out of any matches, e.g.:

  - `[aple]` : Matches "apple", "pale", "leap", etc.
  - `[a-z]` : Matches any lowercase letters from "a" to "z"
  - `[^2]` : Matches anything that is *not* "2"

+ **Example**:

  ```python
  # Finds all email addresses. Note that the '+' operator can be used with sets
  # to indicate that 1 or more characters in the set may appear in succession:

  print(re.findall(r'[-\w\d+.]+@[-\w\d.]+', data))

  # Also note that the '+' inside of the first set is a literal plus sign, and
  # not a count operator.
  ```

- Use the `re.IGNORECASE` (or `re.I`) flag to ignore **case sensitivity**:

  ```python
  print(re.findall(r'\b[trehous]{9}\b', data, re.I)) # Finds treehouse, Treehouse, etc.
  ```

#### Negation

- Use the `re.VERBOSE` (or `re.X`) flag to write regular expressions across multiple lines (ignoring white space and comments):

  ```python
  # Finds comma-separated pairs (e.g., "first name, last name"; "job title, company name"):

  print(re.findall(r'''
      \b[-\w]+, # Find a word boundary, 1+ hyphens or word characters, and a comma.
      \s        # Find a white space.
      [-\w ]+   # Find 1+ hyphens, word characters, or explicit space characters.
      [^\t\n]   # Ignore tabs and newlines.
  ''', data, re.X))
  ```

  - **NOTE:** The **pipe character** (`|`) can be used to combine multiple flags; e.g., `re.I|re.X`.

#### Groups

- Use **parentheses** to identify groups.
- Each group can be given a **name** that can be used for dictionary-like access by using the following syntax at the start of the group: `?P<name>`.
  - **NOTE:** Use the `groupdict()` method to view the match in a dictionary format.
- Use the `^` character (not as a first character in a character set) to specify the *beginning* of a matching input, and use the `$` character to specify the *end*.
  - **NOTE:** Use the `re.MULTILINE` (or `re.M`) flag to indicate that each newline in a single string input should be treated as a separate string.

+ **Example**:
  ```python
  line = re.search(r'''
      ^(?P<name>[-\w ]*,\s[-\w ]+)\t            # Last & first names (last name optional)
      (?P<email>[-\w\d.+]+@[-\w\d.]+)\t         # Email
      (?P<phone>\(?\d{3}\)?-?\s?\d{3}-\d{4})?\t # Phone (optional)
      (?P<job>[\w\s]+,\s[\w\s.]+)\t?            # Job & company (optional)
      (?P<twitter>@[\w\d]+)?$                   # Twitter
  ''', data, re.X|re.M)

  print(line.groupdict()) # Prints key-value pairs for "name", "email", etc.
  ```

#### Compiling and Loops

- Use the `compile()` method to compile a regex pattern into a regex object that can be reused.
- Use the `finditer()` method in a loop upon a compiled `re.search()` object to retrieve an **iterable** of each non-overlapping match in a string. The result is similar to using `findall()`, but you receive a **match object** (instead of tuples), which is what you receive when using `re.match()` or `re.search()`.

+ **Example:**
  ```python
  line = re.compile(r'''
      ^(?P<name>(?P<last>[-\w ]*),\s(?P<first>[-\w ]+))\t # Name (with subgroups)
      (?P<email>[-\w\d.+]+@[-\w\d.]+)\t                   # Email
      (?P<phone>\(?\d{3}\)?-?\s?\d{3}-\d{4})?\t           # Phone
      (?P<job>[\w\s]+,\s[\w\s.]+)\t?                      # Job and company
      (?P<twitter>@[\w\d]+)?$                             # Twitter
  ''', re.X|re.M)

  # Prints the first result:
  print(re.search(line, data).groupdict())

  # Also prints the first result (alternate syntax):
  print(line.search(data).groupdict())

  # Prints all "last name, first name" pairs as match objects:
  for match in line.finditer(data):
      print(match.group('name'))

  # Prints a formatted list of names and emails according to the
  # dictionary values; e.g., "Ryan Carson <ryan@teamtreehouse.com>":
  for match in line.finditer(data):
      print('{first} {last} <{email}>'.format(**match.groupdict()))
  ```

## Using Databases in Python

### Meet Peewee

#### Meet Peewee, Our ORM

- **Installation**

  - Run `pip3 install peewee` to install the [Peewee](https://peewee.readthedocs.io/en/latest/) ORM.
  - To use PeeWee with a MySQL database, run `pip3 install pymysql` to install the required driver.

- **Example** (MySQL):

  ```python
  from peewee import *

  # Configure MySQL database connection.
  db = MySQLDatabase('students', user='root', password='root', host='localhost')


  # Create a base model (using PeeWee's "Model" class) upon which all other models will
  # be based. This convention ensures all models know what database they belong to.
  class BaseModel(Model):
      class Meta:
          database = db


  # Define a model.
  class Student(BaseModel):
      username = CharField(max_length=255, unique=True)  # varchar(255) UNIQUE
      points = IntegerField(default=0)                   # int DEFAULT 0


  students = [
      {'username': 'alpha',
      'points': 40},
      {'username': 'beta',
      'points': 50},
      {'username': 'gamma',
      'points': 60}
  ]


  def add_students():
      for student in students:
          try:
              Student.create(
                  username=student['username'], points=student['points'])
          # An "integrity error" will occur if you attempt to create a Student with
          # an already existing username. If this error occurs, then pull the existing
          # Student from the database, update the Student's points, and save the record.
          except IntegrityError:
              Student.update(points=student['points']).where(
                  Student.username == student['username']).execute()


  def top_student():
      # The get() method returns only the first matching record.
      student = Student.select().order_by(Student.points.desc()).get()
      return student


  # If the file is run directly (not imported), then connect to the database.
  if __name__ == '__main__':
      db.connect()
      # Use the "safe" flag to prevent an error if the table already exists.
      db.create_tables([Student], safe=True)

      add_students()
      # The 0 represents the first index of the output of top_student().
      print('Top student: {0.username}'.format(top_student()))

      db.close()

  ```

## Django Basics

### Say Hello to Django

#### Installing Django

- Run `pip install django` to install Django.

#### Starting the Project

- Use `django-admin` to access admin commands to perform tasks such as creating a new project, e.g.:

  ```
  $ django-admin startproject learning_site

  Yields the following file output:

  .
  +-- learning_site     // "Stub" directory
  |   +-- __init__.py   // Marks a directory as a Python module
  |   +-- asgi.py
  |   +-- settings.py   // Core settings
  |   +-- urls.py       // Base URLs for project
  |   +-- wsgi.py       // Web server entry point
  +-- manage.py         // Admin commands entry point
  ```

  - **NOTE:** Always use underscores for Python packages.

  - **NOTE:** Refere to [the documentation](https://docs.djangoproject.com/en/3.0/ref/django-admin/) for a full list of `django-admin` and `manage.py` commands.

### What a View!

#### Running the Server

- Use the `manage.py` file to tell the server what port it should listen to for receiving requests:

  ```
  python manage.py runserver 0.0.0.0:8000
  ```

- When running the server, you may receive a notice about "unapplied migrations" if Django's migrations have not been run. **Migrations** are a way of moving a database from one design, a specific set of tables and columns, to a new one. Migrations are reversible, too (e.g., removing a column). Run the following commands to apply migrations to the Django database:

  ```
  python manage.py migrate
  ```

  This will add a new file called `db.sqlite3`, which is the default Django database.

#### Hello Django

- Django is an MVC framework, but it does not call templates "views", nor does it call the functions that render templates "controllers". Rather, Django calls templates "templates" and controllers "views" (MTV):

  ```
  M - Model       =>  M - Model
  V - View        =>  T - Template
  C - Controller  =>  V - View
  ```

- Create a `views.py` file in your project's stub directory to manage views:

  ```python
  # ./learning_site/views.py

  from django.http import HttpResponse


  # All views must have a `request` parameter, even if not actually used.
  def hello_world(request):
      return HttpResponse('Hello World')
  ```

- A view must be assigned to a route in order to be rendered.

#### What Are URLs?

- Django URLs are added via the `urls.py` file, e.g.:

  ```python
  from django.contrib import admin
  from django.urls import path

  from . import views

  # The newer `path()` method uses a simpler syntax than the old `url()` method.
  # See: https://docs.djangoproject.com/en/3.0/ref/urls/
  urlpatterns = [
      path('admin/', admin.site.urls),
      path('', views.hello_world),
  ]
  ```

#### Our First App

- Django **Projects** are composed of pluggable **Apps**, with each app encompassing a specific area of functionality. While you use `django-admin startproject` to create a new project, you would use `django-admin startapp` to create an app within the project, e.g.:

  ```
  $ django-admin manage.py startapp courses

  Creates a new directory in your project root named "courses".
  ```

  - **NOTE:** App names are usually the **plural** form of the main model that your app is going to be about.

- Once the app is created, you can include it in `settings.py` within the project's stub directory. Add the app name to the `INSTALLED_APPS` list.

  - **NOTE:** The `settings.py` file is also where you can modify the server's `TIME_ZONE`.

### Model Administration

#### What are Models?

- In Django, models are classes that represent database tables. Each model is its own table, and each attribute on the class is a column in the table. When we add new instances of a class to the database, Django's ORM creates a new row in the table.
- Models belong to an app and live in the app's `models.py` file. Model names should be **singular** by convention, and most models will extend from the `models.Model` base class, e.g.:

  ```python
  from django.db import models

  # The Course class inherits from `models.Model`.
  class Course(models.Model):
      title = models.CharField(max_length=255)
      description = models.TextField()
      # Set value automatically to current time when a record is first created.
      # The current time is determined by the `TIME_ZONE` value in `settings.py`.
      created_at = models.DateTimeField(auto_now_add=True)

      # "Dunder string" defines how an instance is turned into a string. This is
      # used when Django prints a reference to an instance (e.g., in the shell).
      # Can return something more informative than <Course: Course object (3)>.
      def __str__(self):
          return self.title
  ```

  - **NOTE:** The `id` field will automatically be created by Django.

  - **NOTE:** See the [Model Field Reference](https://docs.djangoproject.com/en/3.0/ref/models/fields/) for a complete list of model field types.

- Whenever your model design has changed (e.g., adding a new table or new columns), you need to migrate your database again by **making migrations** with a `manage.py` command:

  ```
  $ python manage.py makemigrations courses

  Migrations for 'courses':
    courses/migrations/0001_initial.py
      - Create model Course
  ```

- After making the migration, you next need to **run the migration**:

  ```
  $ python manage.py migrate courses

  Operations to perform:
    Apply all migrations: courses
  Running migrations:
    Applying courses.0001_initial... OK
  ```

#### Adding Instances

- You can quickly explore the ORM and create new records by opening Python's shell with Django's configuration already loaded:

  ```
  $ python manage.py shell

  # Import the model:
  >>> from courses.models import Course

  # Query existing courses (currently empty) via the model's `objects` attribute:
  >>> Course.objects.all()
  <QuerySet []>

  # Create a course:
  >>> c = Course()
  >>> c.title = "Basics"
  >>> c.description = "Learn the basics"

  # Call the `save()` method to insert the course into the database:
  >>> c.save()

  >>> Course.objects.all()
  <QuerySet [<Course: Course object (1)>]>

  # Alternative way to create a new record:
  >>> Course(title="Collections", description="Learn about collections").save()

  # As another option, use the `create()` method, which will return an object:
  >>> Course.objects.create(title="OOP", description="Learn about OOP")
  <Course: Course object(3)>

  # If a dunder string method has been set, the output should be more informative:
  >>> Course.objects.all()
  <QuerySet [<Course: Python Basics>, <Course: Collections>, <Course: OOP>]>

  # Filter results with the `filter()` method:
  >>> Course.objects.filter(title="OOP")
  <QuerySet [<Course: OOP>]>
  ```

  - **NOTE:** The `objects` attributes points to a **model manager**, which is a class that controls access to the model's instances (among other things).

#### First App View

- You can include views from apps into the main project as follows:

  ```python
  # ./courses/views.py

  from django.http import HttpResponse

  # Reference the `models` module in the current app.
  from .models import Course


  def course_list(request):
      courses = Course.objects.all()
      # Transform the Course objects into a stringified list of course titles.
      output = ', '.join([str(course) for course in courses])
      return HttpResponse(output)
  ```

  ```python
  # ./courses/urls.py

  from django.urls import path

  from . import views

  urlpatterns = [
      path('', views.course_list),
  ]
  ```

  ```python
  # ./learning_site/urls.py

  from django.contrib import admin
  from django.urls import include, path

  from . import views

  urlpatterns = [
      path('courses/', include('courses.urls')),
      path('admin/', admin.site.urls),
      path('', views.hello_world),
  ]
  ```

#### Python Comprehensions

##### List Comprehensions

- **NOTE:** This is not a core section of "Exploring Django". Rather, it is a separate workshop covering the topic of **comprehensions**, which were raised in the "First App View" section above.

- If you wanted to create a list representing half the values of another list, you would normally do so as follows:

  ```python
  nums = range(5, 101)
  halves = []
  for num in nums:
      halves.append(num/2)
  ```

- However, this process can be simplified by using a list comprehension:

  ```python
  halves = [num/2 for num in nums]
  ```

- You do not have to include every iterable value in the list output:

  ```python
  # Only include numbers divisible by 3:
  divisble_by_three = [num for num in nums if num % 3 == 0]
  ```

- You can use double comprehensions when working with two lists:

  ```python
  [(letter, number) for number in range(1, 3) for letter in 'ABC']
  # [('A', 1), ('B', 1), ('C', 1), ('A', 2), ('B', 2), ('C', 2)]
  ```

##### Dict Comprehensions

- Example where a numberic key is tied to a letter of the alphabet:

  ```python
  {number: letter for letter, number in zip('ABCD', range(1, 5))}
  # {1: 'A', 2: 'B', 3: 'C', 4: 'D'}
  ```

##### Set Comprehensions

- Example:

  ```python
  {num * 2 for num in [5, 2, 18, 2, 42, 2, 2]}
  # {84, 10, 4, 36}
  ```

#### Django's Admin

- Create a **super user** to access the admin view:

  ```
  $ python manage.py createsuperuser
  ```

- After logging in, you will see two models created by Django: Groups and Users. These belong to Django's `auth` app. To add (or **register**) your own models, use the `admin.py` file within the model's app, e.g.:

  ```python
  # ./courses/admin.py

  from django.contrib import admin

  from .models import Course

  admin.site.register(Course)
  ```

- From this view, you can create, read, update, and delete records.

### Django Templates

#### Templates

- In Django, templates can be in any language that you want (e.g., HTML, JSON, XML). Django ships built-in backends for its own template system, called the Django template language (DTL), and for [Jinja2](http://jinja.pocoo.org/).

  - **NOTE:** This course only covers the DTL, not Jinja2.

- When inside of an **app** directory, Django looks for templates within a `/templates` directory by default. Django also expects that `/templates` directory to include another directory that shares the same name as the app (serving as a namespaced directory for all app-specific templates within). It is within this directory (e.g., `./courses/templates/courses/`) that your template files will appear, e.g.:

  ```html
  # ./courses/templates/courses/course_list.html

  {% for course in courses %}
    <h2>{{ course.title }}</h2>
    <p>{{ course.description }}</p>
  {% endfor %}
  ```

  ```python
  # ./courses/views.py

  from django.shortcuts import render

  from .models import Course


  def course_list(request):
      courses = Course.objects.all()
      # This `render()` has three arguments: (1) request, (2) template path, and
      # (3) context dictionary. The first two are always required.
      return render(request, 'courses/course_list.html', {'courses': courses})
  ```

- For templates within the **project** itself (as opposed to one of the project's app directories), (1) create a `/templates` directory at the project root level, and (2) modify the `DIRS` list under the `TEMPLATES` variable within `settings.py` to include the directory containing project templates, i.e., `'DIRS': ['templates',]`.

#### Template Inheritance

- Example:

  ```html
  # ./templates/layout.html

  <!DOCTYPE html>
  <html lang="en">
    <head>
      <title>{% block title %}{% endblock %}</title>
    </head>
    <body>{% block content %}{% endblock %}</body>
  </html>
  ```

  ```html
  # ./templates/home.html

  {% extends "layout.html" %}

  {% block title %}Home{% endblock %}

  {% block content %}
    <h1>Welcome</h1>
  {% endblock %}
  ```

#### Static Assets

- The location of [static assets](https://docs.djangoproject.com/en/3.0/howto/static-files/) (e.g., CSS, JS, images) must be referenced in `settings.py` by adding a setting named `STATICFILES_DIRS` (which is a tuple):

  ```python
  STATICFILES_DIRS = (
      os.path.join(BASE_DIR, 'assets'),
  )
  ```

- Once the configuration above has been set up, you can use static assets as follows, e.g.:

  ```html
  # ./templates/layout.html

  # Do not use pre-Django 2.0 `load static from staticfiles`.
  # Modern Django knows where to find the `static` method.

  {% load static %}

  <!DOCTYPE html>
  <html lang="en">
    <head>
      <title>{% block title %}{% endblock %}</title>
      <link rel="stylesheet" href="{% static 'css/layout.css' %}">
    </head>
    <body>{% block content %}{% endblock %}</body>
  </html>
  ```

  - The `{% static 'path' %}` template tag tells Django's template engine to prefix the path with `STATIC_URL`. On a development server, `STATIC_URL` will be the related path in the project's default static directory. On a production server, `STATIC_URL` will be a URL path that conforms to the rules of the running server.

  - **NOTE:** You may see instances where someone's code uses `STATIC_URL` rather than `static`. This may be fine when the static URL never changes. However, if static assets are deployed to something like S3 or CloudFront, then you do not want to have a URL that never changes. The `static` tag can figure out what the dynamic URL may be.

  - **NOTE:** Prior to Django 2.0, the following lines would have been required in `urls.py`, but it is no longer necessary:

    ```python
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns = [ ... ]

    # This checks to see if we're in DEBUG mode and, if so, a `static/` path
    # will be added which points to all files in your static folders.
    urlpatterns += staticfiles_urlpatterns()
    ```

#### Step by Step

- You may have a situation where one model has a relationship to another, and you want to be able to configure the model and its related counterpart in the same admin menu. For example, you may have a collection of "Courses", and each course has a number of instructional "Steps" to follow:

  ```python
  # ./courses/models.py

  from django.db import models


  class Course(models.Model):
      # ...


  class Step(models.Model):
      title = models.CharField(max_length=255)
      description = models.TextField()
      order = models.IntegerField(default=0)
      # Establish a many-to-one relationship where many steps belong to one course.
      course = models.ForeignKey(
          Course,
          on_delete=models.CASCADE, # Delete child tables.
      )

      def __str__(self):
          return self.title
  ```

  - **NOTE:** When adding a new model, remember to (1) register your model, (2) make a new migration, and (3) run the migration.

- You can now add an admin form for editing/creating Steps (i.e., an [inline](https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#inlinemodeladmin-objects)) within the admin form for editing/creating Courses by modifying `admin.py` as follows:

  ```python
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
  ```

#### Add a Detail View

- Example:

  ```html
  # ./courses/templates/courses/course_detail.html

  {% extends "layout.html" %}

  {% block title %}{{ course.title }}{% endblock %}

  {% block content %}
    <article>
      <h2>{{ course.title }}</h2>
      {{ course.description|linebreaks }}

      <section>
        <!-- `step_set` is a query set that can be queried against
          for `all` Step records belonging to the Course -->
        {% for step in course.step_set.all %}
          <h3>{{ step.title }}</h3>
          {{ step.description|linebreaks }}
        {% endfor %}
      </section>
    </article>
  {% endblock %}
  ```

  ```python
  # ./courses/views.py

  from django.shortcuts import render

  from .models import Course


  def course_list(request):
      # ...


  # Django automatically provides `request`, and we provide the
  # primary key (the ID, by default) through the URL.
  def course_detail(request, pk):
      # Django provides a `pk` lookup shortcut.
      course = Course.objects.get(pk=pk)
      return render(request, 'courses/course_detail.html', {'course': course})
  ```

  ```python
  # ./courses/urls.py

  from django.urls import path

  from . import views

  urlpatterns = [
      path('<int:pk>/', views.course_detail),
      path('', views.course_list),
  ]
  ```

  - **NOTE:** [`prefetch_related`](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#django.db.models.query.QuerySet.prefetch_related) and [`select_related`](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#django.db.models.query.QuerySet.select_related) may also be useful in making queries.

#### Ordering and 404s

- Modify the order of records as follows:

  ```python
  # ./courses/models.py

  from django.db import models


  class Course(models.Model):
      # ...


  class Step(models.Model):
      title = models.CharField(max_length=255)
      description = models.TextField()
      order = models.IntegerField(default=0)
      course = models.ForeignKey(
          Course,
          on_delete=models.CASCADE,
      )

      # Django models have an optional `Meta` class to control their behavior.
      class Meta:
          # Order records by the `order` attribute, and then fall back
          # to using the `id` if the same `order` is used.
          ordering = ['order',]

      def __str__(self):
          return self.title
  ```

- Use the following shortcut to yield 404 errors:

  ```python
  # ./courses/views.py

  from django.shortcuts import get_object_or_404, render

  from .models import Course


  def course_detail(request, pk):
      # Show 404 if the Course object is not found.
      course = get_object_or_404(Course, pk=pk)
      return render(request, 'courses/course_detail.html', {'course': course})
  ```

  - **NOTE:** You can customize error views by following the instructions [here](https://docs.djangoproject.com/en/3.0/topics/http/views/#customizing-error-views).

### Final Details

#### url Tag

- Example:

  ```python
  # ./learning_site/urls.py

  # ...

  urlpatterns = [
      # Add `namespace` for easier configuration of URL tags.
      path('courses/', include('courses.urls', namespace='courses')),
      path('admin/', admin.site.urls),
      path('', views.home, name='home'), # Assign a name for tagging.
  ]
  ```

  ```html
  # ./templates/layout.html

  <!-- Snippet -->
  <nav>
    <a href="{% url 'home' %}">Home</a>
    <a href="{% url 'courses:list' %}">Courses</a>
  </nav>
  ```

  ```python
  # ./courses/urls.py

  # ...

  # Must include an app name for namespacing to work.
  app_name = 'courses'

  urlpatterns = [
      path('', views.course_list, name='list'),
      path('<int:course_pk>/<int:step_pk>/', views.step_detail, name='step'),
      path('<int:pk>/', views.course_detail, name='detail'),
  ]
  ```

  ```html
  # ./courses/templates/courses/course_list.html

  <!-- Snippet -->
  <div class="cards">
    {% for course in courses %}
    <div class="card">
      <header>
        <a href="{% url 'courses:detail' pk=course.pk %}">{{ course.title }}</a>
      </header>
      <div class="card-copy">
        {{ course.description|linebreaks }}
      </div>
    </div>
    {% endfor %}
  </div>
  ```

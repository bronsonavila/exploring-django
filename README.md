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

  - Run `pip install peewee` to install the [**Peewee**](https://peewee.readthedocs.io/en/latest/) ORM.
  - To use PeeWee with a MySQL database, run `pip install pymysql` to install the required driver.

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

## Python Testing

### First Steps With Testing

#### Writing and Running Doctests

- **Doctests** are written in plain text in the **docstring** of a function or class. Examples:

  ```python
  # .python-testing/dungeon/dd_game.py

  # Python will run a statement that starts with 3 chevrons.

  def build_cells(width, height):
      """Create and return a `width` x `height` grid of two tuples

      >>> cells = build_cells(2, 2)
      >>> len(cells)
      4

      """
      cells = []
      for y in range(height):
          for x in range(width):
              cells.append((x, y))
      return cells


    def get_locations(cells) :
        """Randomly pick starting locations for the monster, the door,
        and the player

        >>> cells = build_cells(2, 2)
        >>> m, d, p = get_locations(cells)
        >>> m != d and d != p
        True
        >>> d in cells
        True

        """
        monster = random.choice(cells)
        door = random.choice(cells)
        player = random.choice(cells)

        if monster == door or monster == player or door == player:
            monster, door, player = get_locations(cells)

        return monster, door, player


    def get_moves(player):
        """Based on the tuple of the player's position, return the list
        of acceptable moves

        >>> GAME_DIMENSIONS = (2, 2)
        >>> get_moves((0, 2))
        ['RIGHT', 'UP', 'DOWN']

        """
        x, y = player
        moves = ['LEFT', 'RIGHT', 'UP', 'DOWN']
        if x == 0:
            moves.remove('LEFT')
        if x == GAME_DIMENSIONS[0] - 1:
            moves.remove('RIGHT')
        if y == 0:
            moves.remove('UP')
        if y == GAME_DIMENSIONS[1] - 1:
            moves.remove('DOWN')
        return moves
  ```

- To run the tests in the examples above, run:

  ```
  $ python -m doctest dd_game.py
  ```

  - **NOTE:** The `-m` flag tells Python to load the `doctest` module. The `doctest` module reviews the file for doctests and runs them. If no messages are printed to the console, then all of the tests passed successfully.

#### Your First unittest Test Case

- A **test case** is a class that contains multiple methods (some of which are tests, and others simply being methods that you need). There are two special methods--**Set Up** and **Tear Down**--that are run before and after each test.

- Example:

  ```python
  # ./python-testing/rps/tests.py

  import unittest


  # Test case:
  class MathTests(unittest.TestCase):
      # Tests must always begin with the word `test`.
      def test_five_plus_five(self):
          assert 5 + 5 == 10

      def test_one_plus_one(self):
          assert not 1 + 1 == 3

  # Allow tests to be run directly via `$ python tests.py`.
  if __name__ == '__main__':
      unittest.main()
  ```

  - **NOTE:** If do you not include the last 2 lines, you will have to run the tests via:

    ```python
    $ python -m unittest tests.py
    ```

### Be Assertive

#### Quantitative Assertions

- **Assertions** test a condition in your code that must be met. Examples:

  ```python
  # ./python-testing/rps/tests.py

  import unittest

  import moves


  class MoveTests(unittest.TestCase):
      # The `setUp` method predates PEP8, hence the camelCase.
      # This method is called before each test.
      def setUp(self):
          self.rock = moves.Rock()
          self.paper = moves.Paper()
          self.scissors = moves.Scissors()

      def test_equal(self):
          self.assertEqual(self.rock, moves.Rock())

      def test_not_equal(self):
          self.assertNotEqual(self.rock, self.paper)

      def test_rock_better_than_scissors(self):
          self.assertGreater(self.rock, self.scissors)

      def test_paper_worse_than_scissors(self):
          self.assertLess(self.paper, self.scissors)

  if __name__ == '__main__':
      unittest.main()
  ```

#### Exceptions

- Example of testing for exceptions:

  ```python
  def test_bad_description(self):
      # This test will pass only if a `ValueError` exception is raised.
      # `with` is a "context manager".
      with self.assertRaises(ValueError):
          dice.Roll('2b6')
  ```

### Covering Your Bases

#### Using Coverage

- Run `pip install coverage` to install Coverage.

- To use Coverage, ensure the script to be scripted includes the `if __name__` block noted above, and run the following command:

  ```
  $ coverage run tests.py
  ```

- To view details regarding your percentage of code coverage and any lines which are missing coverage, run the following command:

  ```
  $ coverage report -m
  ```

  - **NOTE:** The `-m` flag stands for "missing".

- Ideally, aim for code coverage of 90% or better.

#### HTML Reports

- Instead of generating a Coverage report in the terminal, you can run the following command to prepare an HTML report that can be viewed in your browser:

  ```
  $ coverage html
  ```

- After creating your `htmlcov/` directory, run a Python server to view the page in your browser:

  ```
  $ python -m http.server
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
  # ./django-basics/learning_site/views.py

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

  - **NOTE:** See the [**Model Field Reference**](https://docs.djangoproject.com/en/3.0/ref/models/fields/) for a complete list of model field types.

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
  # ./django-basics/learning_site/courses/views.py

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
  # ./django-basics/learning_site/courses/urls.py

  from django.urls import path

  from . import views

  urlpatterns = [
      path('', views.course_list),
  ]
  ```

  ```python
  # ./django-basics/learning_site/urls.py

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
  # ./django-basics/learning_site/courses/admin.py

  from django.contrib import admin

  from .models import Course

  admin.site.register(Course)
  ```

- From this view, you can create, read, update, and delete records.

### Django Templates

#### Templates

- In Django, templates can be in any language that you want (e.g., HTML, JSON, XML). Django ships built-in backends for its own template system, called the Django template language (DTL), and for [**Jinja2**](http://jinja.pocoo.org/).

  - **NOTE:** This course only covers the DTL, not Jinja2.

- When inside of an **app** directory, Django looks for templates within a `/templates` directory by default. Django also expects that `/templates` directory to include another directory that shares the same name as the app (serving as a namespaced directory for all app-specific templates within). It is within this directory (e.g., `/.django-basics/learning_site/courses/templates/courses/`) that your template files will appear, e.g.:

  ```html
  # ./django-basics/learning_site/courses/templates/courses/course_list.html

  {% for course in courses %}
    <h2>{{ course.title }}</h2>
    <p>{{ course.description }}</p>
  {% endfor %}
  ```

  ```python
  # ./django-basics/learning_site/courses/views.py

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

  <!-- The given path should be relative to `templates/ -->
  {% extends "layout.html" %}

  {% block title %}Home{% endblock %}

  {% block content %}
    <h1>Welcome</h1>
  {% endblock %}
  ```

#### Static Assets

- The location of [**static assets**](https://docs.djangoproject.com/en/3.0/howto/static-files/) (e.g., CSS, JS, images) must be referenced in `settings.py` by adding a setting named `STATICFILES_DIRS` (which is a tuple):

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
  # ./django-basics/learning_site/courses/models.py

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

- You can now add an admin form for editing/creating Steps (i.e., an [**inline**](https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#inlinemodeladmin-objects)) within the admin form for editing/creating Courses by modifying `admin.py` as follows:

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
  # ./django-basics/learning_site/courses/templates/courses/course_detail.html

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

    - **NOTE:** If you only want to know the number of items in a query set, consider using `step_set.count` instead (as calling `.all` will perform a full database query, while `.count` just query the number of relevant items).

  ```python
  # ./django-basics/learning_site/courses/views.py

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
  # ./django-basics/learning_site/courses/urls.py

  from django.urls import path

  from . import views

  urlpatterns = [
      path('<int:pk>/', views.course_detail),
      path('', views.course_list),
  ]
  ```

  - **NOTE:** [**prefetch_related**](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#django.db.models.query.QuerySet.prefetch_related) and [**select_related**](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#django.db.models.query.QuerySet.select_related) may also be useful in making queries.

#### Ordering and 404s

- Modify the order of records as follows:

  ```python
  # ./django-basics/learning_site/courses/models.py

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
  # ./django-basics/learning_site/courses/views.py

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
  # ./django-basics/learning_site/urls.py

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
  # ./django-basics/learning_site/courses/urls.py

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
  # ./django-basics/learning_site/courses/templates/courses/course_list.html

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

### Test Time

#### Model Tests

- Testing models is usually the first step in thoroughly testing a Django app. All apps will include a `tests.py` file when they are created. Once you have written your tests, run them using the `test` command of your project's `manage.py` utility:

  ```
  $ python manage.py test
  ```

#### View Tests

- Example:

  ```python
  # ./django-basics/learning_site/courses/tests.py

  from django.urls import reverse
  from django.test import TestCase

  from .models import Course


  class CourseViewsTests(TestCase):
      def setUp(self):
          self.course = Course.objects.create(
              title="Python Testing",
              description="Learn to write tests in Python"
          )
          self.course2 = Course.objects.create(
              title="New Course",
              description="A new course"
          )

      # Test course list view to ensure it shows both courses above.
      def test_course_list_view(self):
          # When testing views, you can use `self.client`, which allows you to
          # make HTTP requests to a URL and fetch the status code and HTML that
          # come from that URL.
          resp = self.client.get(reverse('courses:list'))
          self.assertEqual(resp.status_code, 200)
          # `resp` (response) object has an attributed named `context` which is
          # a dictionary of all values passed into the template upon render.
          self.assertIn(self.course, resp.context['courses'])
          self.assertIn(self.course2, resp.context['courses'])

      def test_course_detail_view(self):
          resp = self.client.get(
              reverse('courses:detail', kwargs={'pk': self.course.pk}))
          self.assertEqual(resp.status_code, 200)
          self.assertEqual(self.course, resp.context['course'])

      def test_step_detail_view(self):
          resp = self.client.get(reverse('courses:step', kwargs={
                                'course_pk': self.course.pk, 'step_pk': self.step.pk}))
          self.assertEqual(resp.status_code, 200)
          self.assertEqual(self.step, resp.context['step'])
  ```

#### Template Tests

- Example:

  ```python
  # ./django-basics/learning_site/courses/tests.py

  # ...

  def test_course_list_view(self):
      resp = self.client.get(reverse('courses:list'))
      # Verify that the correct template is used.
      self.assertTemplateUsed(resp, 'courses/course_list.html')
      # Ensure that the course title appears somewhere on the page.
      self.assertContains(resp, self.course.title)
  ```

## Customizing Django Templates

### CSS in Django

- To add app-specific (rather than site-wide) CSS and other static assets, you need to add a directory called `static/` within the app directory. You must then **namespace** your static files by creating another directory within your `static/` directory which has the same name as your app directory. For example, if your app is contained within the `./learning_site/courses/` directory, then the static files should be contained within: `./learning_site/courses/static/courses/css/courses.css`

- To apply your app-specific styles, add a `static` block in the `<head>` of your base HTML layout, and then use the `static` block within your app-specific HTML template in which the styles should be applied, e.g.:

  ```html
  # ./django-basics/learning_site/templates/layout.html

  <head>
    <title>{% block title %}{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'css/layout.css' %}">
    {% block static %}{% endblock %}
  </head>
  ```

  ```html
  # ./django-basics/learning_site/courses/templates/courses/course_list.html

  {% extends "layout.html" %}

  <!-- Load app-specific static files -->
  {% load static %}

  {% block static %}
    <link rel="stylesheet" href="{% static 'courses/css/courses.css' %}">
  {% endblock %}

  # ...
  ```

### Handy Dandy Filters

- Example of how to use `pluralize` and `join` filters:

  ```html
  # Will say "There is 1 step in this course" or "There are 2 steps in this course", depending on the number of steps assigned to the given course. Each step will be separated by a comma and a space.

  <p>
    There {{ course.step_set.count|pluralize:'is,are' }} {{ course.step_set.count }} step{{ course.step_set.count|pluralize }} in this course: {{ course.step_set.all|join:', ' }}
  </p>
  ```

### Using Template Libraries

- Consider using the [**Humanize `contrib` package**](https://docs.djangoproject.com/en/3.0/ref/contrib/humanize/) for additional filters that are helpful for displaying data values in a more human-readable format. To use this package, add `django.contrib.humanize` to your `INSTALLED_APPS` in `settings.py`. Once installed, load the package into the template file, e.g.:

  ```python
  {% load humanize %}

  # Displays 1-9 as numbers, and 10+ as words (e.g., "ten").
  {{ course.step_set.count|apnumber }}
  ```

- If you know that you may chaining multiple filters on one particular variable, consider using the `with` statement to make the variable name shorter, e.g.:

  ```python
  {% with content=step.content %}
    {{ content|linebreaks }} Content: {{ content|wordcount }} words
  {% endwith %}
  ```

## Building Custom Tags

### Built-in Tags and Filters

- Examples of `wordcount`, `truncatewords`, `urlize`, and Django's custom [**date filter**](https://docs.djangoproject.com/en/3.0/ref/templates/builtins/#date):

  ```html
  <!-- Add an ellipsis and "Read More" link for descriptions longer than 5 words. -->
  <div class="card-copy">
    {% with description=course.description %}
      {% if description|wordcount <= 5 %}
        {{ description|linebreaks }}
      {% else %}
        {{ description|linebreaks|truncatewords:5 }}
        <a href="{% url 'courses:detail' pk=course.pk %}">Read More</a>
      {% endif %}
      <!-- Format date as: December 9, 2019 -->
      <div>Created on: {{ course.created_at|date:'F j, Y' }}</div>
    {% endwith %}
  </div>

  <!-- `urlize` automatically creates a `mailto` link if text is a valid email. -->
  <div>Have questions? Contact us: {{ email|urlize }}</div>
  ```

### DIY Custom Tags

- [**Custom template tags**](https://docs.djangoproject.com/en/3.0/howto/custom-template-tags/#simple-tags) must be located in an app's `templatetags/` directory.

  - **IMPORTANT:** Be sure to place an empty `__init__.py` file in the directory; otherwise, the directory will not be recognized as a Python package.

- Example:

  ```python
  # ./django-basics/learning_site/courses/templatetags/course_extras.py

  # The `template` module contains the function required to register
  # templates. When you register a template tag, you are making the
  # tag available to Django's template language for future use.
  from django import template

  from courses.models import Course


  register = template.Library()

  # Teacher's Notes: Simple tags don't include new templates, don't have
  # an end tag, and don't assign values to context variables.
  @register.simple_tag
  def newest_course():
      """Gets the most recent course that was added to the library."""
      return Course.objects.latest('created_at')

  # If you do not include the `@register` decorator, this line would
  # be required to register the template tag:
  # register.simple_tag(newest_course)
  ```

### Complex Template Tags

- Use an `inclusion_tag` if your template tag needs to return data as another template, not just a string, e.g.:

  ```python
  # ./django-basics/learning_site/courses/templatetags/course_extras.py

  @register.inclusion_tag('courses/course_nav.html')
  def nav_courses_list():
      """Returns dictionary of courses to display as navigation pane."""
      courses = Course.objects.all()
      return {'courses': courses}
  ```

  ```html
  # ./django-basics/learning_site/courses/templates/courses/course_nav.html

  {% for course in courses %}
    <div>
      <a href="{% url 'courses:detail' pk=course.pk %}">{{ course.title }}</a>
    </div>
  {% endfor %}
  ```

  ```html
  # ./django-basics/learning_site/templates/layout.html

  <div>{% nav_courses_list %}</div>
  ```

## Building Custom Filters

### Custom Time Estimate Filter

- Custom filters are located in the same directory as custom template tags: `templatetags/`

- Example:

  ```python
  # ./django-basics/learning_site/courses/templatetags/course_extras.py

  @register.filter
  def time_estimate(word_count):
      minutes = round(word_count/20)
      return minutes
  ```

  ```html
  # ./django-basics/learning_site/courses/templates/courses/step_detail.html

  <!-- Displays "Content: 26 words. Estimated time to complete: 1 minute." -->
  {% with content=step.content %}
    Content: {{ content|wordcount }} words.
    Estimated time to complete: {{ content|wordcount|time_estimate }} minute{{ content|wordcount|time_estimate|pluralize }}.
  {% endwith %}
  ```

### Custom Tags

- You can use a Python library called [**markdown2**](https://github.com/trentm/python-markdown2) to transform Markdown text into HTML. Run `pip install markdown2` to install the library.

- Example:

  ```python
  # ./django-basics/learning_site/courses/templatetags/course_extras.py

  # ...

  from django.utils.safestring import mark_safe
  import markdown2

  # ...

  @register.filter
  def markdown_to_html(markdown_text):
      """Converts Markdown text to HTML."""
      html_body = markdown2.markdown(markdown_text)
      return mark_safe(html_body)
  ```

  ```html
  # ./django-basics/learning_site/courses/templates/courses/course_detail.html

  {% load course_extras %}

  {{ course.description|markdown_to_html }}
  ```

## Django Forms

### Forms

#### Creating a Form

- If you want to make a [**form**](https://docs.djangoproject.com/en/3.0/topics/forms/) for your general site (e.g., a contact form), first create a file named `forms.py` in your project's stub directory (e.g., `./learning_site/learning_site/forms.py`). Each form should exist as a class within `forms.py`, e.g.:

  ```python
  # ./django-basics/learning_site/learning_site/forms.py

  from django import forms


  class SuggestionForm(forms.Form):
      name = forms.CharField()
      email = forms.EmailField()
      # Specify the `TextArea` widget; otherwise, it will be an input field.
      suggestion = forms.CharField(widget=forms.Textarea)
  ```

#### Showing a Form in a View

- Example:

  ```python
  # ./django-basics/learning_site/learning_site/views.py

  from . import forms

  # ...

  def suggestion_view(request):
    form = forms.SuggestionForm()
    return render(request, 'suggestion_form.html', {'form': form})
  ```

  ```python
  # ./django-basics/learning_site/learning_site/urls.py

  from . import views

  # ...

  urlpatterns = [
    # ...
    path('suggest/', views.suggestion_view, name='suggestion'),
    # ...
  ]
  ```

  ```html
  # ./django-basics/learning_site/templates/suggestion_form.html

  {% extends "layout.html" %}

  {% block title %}Suggest an idea!{% endblock %}

  {% block content %}
    <form action="" method="POST">
      <!-- Place each form element within a set of `<p>` tags. -->
      {{ form.as_p }}
      {% csrf_token %}
      <input type="submit">
    </form>
  {% endblock %}
  ```

  - **IMPORTANT:** The `csrf_token` is used to protect against [**Cross Site Request Forgeries**](https://docs.djangoproject.com/en/3.0/ref/csrf/).

#### Handling a Form in a View

- Example of how to process a submitted form (simulates the form being received as an email, but merely stores the email within a `suggestions/` directory instead):

  ```python
  # ./django-basics/learning_site/learning_site/settings.py

  # ...

  EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
  EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'suggestions')
  ```

  - **NOTE:** Refer to the [**documentation**](https://docs.djangoproject.com/en/3.0/topics/email/) for more information on sending a real email.

  ```python
  # ./django-basics/learning_site/learning_site/views.py

  from django.contrib import messages
  from django.core.mail import send_mail
  from django.urls import reverse
  from django.http import HttpResponseRedirect
  from django.shortcuts import render

  from . import forms

  # ...

  def suggestion_view(request):
      form = forms.SuggestionForm()

      if request.method == 'POST':
          # Pass in the form data via the `request.POST` dictionary,
          # and then validate the form's inputs in relation to the class.
          # This is a "time-tested" approach to handling form validation.
          form = forms.SuggestionForm(request.POST)
          if form.is_valid():
              # After being run through the `is_valid()` method, each field
              # will be added to the `cleaned_data` object.
              send_mail(
                  'Suggestion from {}'.format(form.cleaned_data['name']),
                  form.cleaned_data['suggestion'],
                  '{name} <{email}>'.format(**form.cleaned_data),
                  ['name@email.com']
              )
              # Display flash message on the screen after submission.
              messages.add_message(request, messages.SUCCESS,
                                  'Thanks for your suggestion!')
              # Redirect to the same page (acts as a way to clear the form).
              return HttpResponseRedirect(reverse('suggestion'))

      return render(request, 'suggestion_form.html', {'form': form})
  ```

  ```html
  # ./django-basics/learning_site/templates/suggestion_form.html

  # ...

  {% block content %}
    {% if messages %}
      <ul>
        {% for message in messages %}
          <li>{{ message }}</li>
        {% endfor %}
      </ul>
    {% endif %}
    <form action="" method="POST">
      {{ form.as_p }}
      {% csrf_token %}
      <input type="submit">
    </form>
  {% endblock %}
  ```

#### Custom Field Validation

- Example of a "honeypot" custom field validation:

  ```python
  # ./django-basics/learning_site/learning_site/forms.py

  # ...

  class SuggestionForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    suggestion = forms.CharField(widget=forms.Textarea)
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

    # When Django runs the `is_valid()` method, it applies its own built-in
    # validations to each field. Adding your own `clean_` method allows you
    # to perform validations beyond the default cleaning behavior for a specific
    # field (e.g., `clean_name` will handle validating the `name` field).
    def clean_honeypot(self):
        honeypot = self.cleaned_data['honeypot']
        if len(honeypot):
            raise forms.ValidationError('Bad bot!')
        return honeypot
  ```

#### Using and Creating Validators

- Rather than using a custom field validation, you may also be able to rely upon Django's [**validators**](https://docs.djangoproject.com/en/3.0/ref/validators/), e.g.:

  ```python
  # ./django-basics/learning_site/learning_site/forms.py

  # ...

  class SuggestionForm(forms.Form):
      name = forms.CharField()
      email = forms.EmailField()
      suggestion = forms.CharField(widget=forms.Textarea)
      honeypot = forms.CharField(
          required=False,
          widget=forms.HiddenInput,
          # The value is only valid if it has a max length of 0.
          validators=[validators.MaxLengthValidator(0)]
      )
  ```

- Alternatively, you can create your own custom validators, e.g.:

  ```python
  # ./django-basics/learning_site/learning_site/forms.py

  # ...

  def must_be_empty(value):
      if value:
          raise forms.ValidationError('is not empty')


  class SuggestionForm(forms.Form):
      name = forms.CharField()
      email = forms.EmailField()
      # Specify the `TextArea` widget; otherwise, it will be an input field.
      suggestion = forms.CharField(widget=forms.Textarea)
      honeypot = forms.CharField(
          required=False,
          widget=forms.HiddenInput,
          validators=[must_be_empty]
    )
  ```

#### Cleaning a Whole Form

- Example:

  ```python
  # ./django-basics/learning_site/learning_site/forms.py

  # ...

  # If a method is named `clean`, then it will clean the entire form.
  # Django will first go through each field and make sure they satisfy
  # their own requirements. Then Django will look a the form as a whole
  # to make sure the form follows the `clean` method's requirements.
  def clean(self):
      # `super().clean()` preserves validation logic in parent classes.
      # See: https://docs.djangoproject.com/en/3.0/ref/forms/validation/
      cleaned_data = super().clean()
      email = cleaned_data.get('email')
      verify = cleaned_data.get('verify_email')

      if email != verify:
          raise forms.ValidationError('Email fields must match.')
  ```

  - **NOTE:** Unlike cleaning a single field, the form `clean` method does not need to return a "clean" value if an error is not raised.

### More on Models

#### Abstract Inheritance

- [**Abstract inheritance**](https://docs.djangoproject.com/en/3.0/topics/db/models/#abstract-base-classes) allows for models to inherit from other models which are not inserted in the database, e.g.:

  ```python
  class User(models.Model):
      """Cannot be queried."""
      name = models.CharField()

      class Meta:
          abstract = True

  class Student(User):
      """Will include a `name` field. Can be queried via `Student.objects.all()`."""

  class Staff(User):
      """Will include a `name` field. Can be queried via `Staff.objects.all()`."""
  ```

  - **NOTE:** If you turn an already existing model into an abstract model, you will need to make and apply a new migration (and will likely need to remove registration references to the modified model in `admin.py` in the process, as you will essentially be renaming the model that currently exists in the database).

#### Multiple Choice and True/False Questions

- The second type of model inheritance used by Django is [**multi-table inheritance**](https://docs.djangoproject.com/en/3.0/topics/db/models/#multi-table-inheritance), which occurs when each model in the heirarcy corresponds to its own database table and can be queried and created individually. (You will probably want to avoid using MTI most of the time.)

- Example:

  ```python
  # ./django-basics/learning_site/courses/models.py

  # ...

  class Question(models.Model):
      quiz = models.ForeignKey(
          Quiz,
          on_delete=models.CASCADE
      )
      order = models.IntegerField(default=0)
      prompt = models.TextField()

      class Meta:
          ordering = ['order', ]

      # Makes it easier to get to specific model instances, and can also
      # be useful in the admin view (for creating a "View on Site" button).
      def get_absolute_url(self):
          return self.quiz.get_absolute_url()

      def __str__(self):
          return self.prompt


  class MultipleChoiceQuestion(Question):
      shuffle_answers = models.BooleanField(default=False)


  class TrueFalseQuestion(Question):
      pass
  ```

  - **NOTE:** With the above configuration, it would only be necessary to register the `MultipleChoiceQuestion` and `TrueFalseQuestion` models (not the `Question` model

### Model Forms

#### What are Model Forms?

- When you create a model in an app, Django automatically creates a form for creating/editing instances of registered models via the admin view. However, if you want to create/edit models from outside of the admin view (e.g., to allow logged-in users to modify their own data), Django provides [**model forms**](https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/).

- To create a model form, go to your app directory and create a file named `forms.py`. Example:

  ```python
  # ./django-basics/learning_site/courses/forms.py

  from django import forms

  from . import models


  class QuizForm(forms.ModelForm):
      class Meta:
          model = models.Quiz
          # Specify the fields you want to include.
          fields = [
              'title',
              'description',
              'order',
              'total_questions',
          ]
  ```

- Teacher's Notes: One of the areas of model forms that frustrates people is the requirement to use either `fields` or `exclude`. Many people find `excludes` to be faster because you do not have to update it every time you change your form or your model. But that is a dangerous decision to make because now any new fields will be automatically added to your displayed form. Instead, use `fields` to be explicit and control your fields directly.

#### Using a Model Form

- Create a new view for your model form:

  ```python
  # ./django-basics/learning_site/courses/views.py

  from django.contrib import messages
  # Marks a view as requiring a logged-in user.
  from django.contrib.auth.decorators import login_required
  from django.http import HttpResponseRedirect
  from django.shortcuts import get_object_or_404, render

  from . import forms
  from . import models

  # ...

  @login_required
  def quiz_create(request, course_pk):
      course = get_object_or_404(models.Course, pk=course_pk)
      form = forms.QuizForm()

      if request.method == 'POST':
          form = forms.QuizForm(request.POST)
          if form.is_valid():
              # `commit=False` means "don't actually put this in the database,
              # just make the model instance and hold it in memory."
              # This allows you to modify the form data before saving.
              quiz = form.save(commit=False)
              # The form will not allow the user to modify the
              # course associated with the quiz, but the course
              # must be included as a field from the `Step` model
              # (which is the `Quiz` parent model).
              quiz.course = course
              quiz.save()
              messages.add_message(request, messages.SUCCESS, 'Quiz added!')
              return HttpResponseRedirect(quiz.get_absolute_url())

      return render(request, 'courses/quiz_form.html', {'form': form, 'course': course})
  ```

- Create a URL to access the model form view:

  ```python
  # ./django-basics/learning_site/courses/urls.py

  # ...

  urlpatterns = [
      # ...
      path('<int:course_pk>/create_quiz/', views.quiz_create, name='create_quiz'),
      # ...
  ]
  ```

- Create an HTML template for your model form:

  ```html
  # ./django-basics/learning_site/courses/templates/courses/quiz_form.html

  {% extends "layout.html" %}

  {% block title %}New Quiz | {{ course.title }}{% endblock %}

  {% block content %}
    <a href="{% url 'courses:detail' pk=course.pk %}">Back to {{ course.title }}</a>

    <h1>Make a new quiz</h1>

    <form method="POST">
      {% csrf_token %}
      {{ form.as_p }}
      <input type="submit" value="Save">
    </form>
  {% endblock %}
  ```

- Create a link elsewhere on the site to access your model form:

  ```html
  # ./django-basics/learning_site/courses/templates/courses/course_detail.html

  # ...

  <!-- Only allow logged-in users to view this link. -->
  {% if user.is_authenticated %}
    <a href="{% url 'courses:create_quiz' course_pk=course.id %}">New Quiz</a>
  {% endif %}
  ```

#### Edit an Instance

- Create a view for editing a model form:

  ```python
  # ./django-basics/learning_site/courses/views.py

  # ...

  @login_required
  def quiz_edit(request, course_pk, quiz_pk):
      quiz = get_object_or_404(models.Quiz, pk=quiz_pk, course_id=course_pk)
      form = forms.QuizForm(instance=quiz)

      if request.method == 'POST':
          form = forms.QuizForm(instance=quiz, data=request.POST)
          if form.is_valid():
              form.save()
              messages.success(request, "Updated {}".format(
                  form.cleaned_data['title']))
              return HttpResponseRedirect(quiz.get_absolute_url())

      return render(request, 'courses/quiz_form.html', {'form': form, 'course': quiz.course})
  ```

- Create a URL:

  ```python
  # ./django-basics/learning_site/courses/urls.py

  urlpatterns = [
      # ...
      path('<int:course_pk>/edit_quiz/<int:quiz_pk>/', views.quiz_edit, name='edit_quiz'),
      # ...
  ]
  ```

- Modify your form template to accommodate edit functionality:

  ```html
  # ./django-basics/learning_site/courses/templates/courses/quiz_form.html

  {% extends "layout.html" %}

  <!-- If a form to edit already exists, then Django will pull in
    the title of the form instance. Otherwise, if the form does
    not exist, then Django will display "New Quiz" by default. -->
  {% block title %}
    {{ form.instance.title|default:"New Quiz" }} | {{ course.title }}
  {% endblock %}

  {% block content %}
    <a href="{% url 'courses:detail' pk=course.pk %}">Back to {{ course.title }}</a>

    <h1>{{ form.instance.title|default:"Make a new quiz" }}</h1>

    <form method="POST">
      {% csrf_token %}
      {{ form.as_p }}
      <input type="submit" value="Save">
    </form>
  {% endblock %}
  ```

### Inlines and Media

#### Formsets

- [**Formsets**](https://docs.djangoproject.com/en/3.0/topics/forms/formsets/) allow you to create/edit multiple instances of a model at once. Example:

  ```python
  # ./django-basics/learning_site/courses/forms.py

  # ...

  AnswerFormset = forms.modelformset_factory(
      models.Answer,
      form=AnswerForm,
      extra=2, # Show 2 extra blank sets of form inputs (default=1)
  )
  ```

  ```python
  # ./django-basics/learning_site/courses/views.py

  # ...

  @login_required
  def answer_form(request, question_pk):
      question = get_object_or_404(models.Question, pk=question_pk)
      formset = forms.AnswerFormset(queryset=question.answer_set.all())

      if request.method == 'POST':
          formset = forms.AnswerFormset(
              request.POST, queryset=question.answer_set.all())
          if formset.is_valid():
              answers = formset.save(commit=False)
              for answer in answers:
                  answer.question = question
                  answer.save()
              messages.success(request, 'Added answers')
              return HttpResponseRedirect(question.quiz.get_absolute_url())

      return render(request, 'courses/answer_form.html', {
          'formset': formset,
          'question': question,
      })
  ```

  ```html
  # ./django-basics/learning_site/courses/templates/courses/answer_form.html

  <form action="" method="POST">
    {% csrf_token %}
    <section>
      {{ formset }}
    </section>
    <input type="submit" value="Save">
  </form>
  ```

#### Inline Model Formset

- [**Inline formsets**](https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/#inline-formsets) appear in the model form of another model.

- Example (allows a user to modify a question's answers directly from the "Question" form, rather than needing to access a separate "Answers" form):

  ```python
  # ./django-basics/learning_site/courses/forms.py

  # ...

  AnswerInlineFormset = forms.inlineformset_factory(
      models.Question,  # The model that will contain the inline form.
      models.Answer,  # The model to be editted in the inline form.
      extra=2,
      fields=('order', 'text', 'correct'),
      formset=AnswerFormset,  # Per lecturer: "Not required."
      min_num=1,
  )
  ```

  ```python
  # ./django-basics/learning_site/courses/views.py

  # ...

  @login_required
  def create_question(request, quiz_pk, question_type):
      quiz = get_object_or_404(models.Quiz, pk=quiz_pk)
          form_class = forms.TrueFalseQuestionForm
      else:
          form_class = forms.MultipleChoiceQuestionForm

      form = form_class()
      answer_forms = forms.AnswerInlineFormset(
          # The question has no answers since it's just being created,
          # so you must pull in a blank queryset.
          queryset=models.Answer.objects.none()
      )

      if request.method == 'POST':
          form = form_class(request.POST)
          answer_forms = forms.AnswerInlineFormset(
              request.POST,
              queryset=models.Answer.objects.none(),
          )

          if form.is_valid() and answer_forms.is_valid():
              question = form.save(commit=False)
              question.quiz = quiz
              question.save()
              answers = answer_forms.save(commit=False)
              for answer in answers:
                  answer.question = question
                  answer.save()
              messages.success(request, 'Added question')
              return HttpResponseRedirect(quiz.get_absolute_url())

      return render(request, 'courses/question_form.html', {
          'quiz': quiz,
          'form': form,
          'formset': answer_forms,
      })


  @login_required
  def edit_question(request, quiz_pk, question_pk):
      question = get_object_or_404(
          models.Question, pk=question_pk, quiz_id=quiz_pk)

      if hasattr(question, 'truefalsequestion'):
          form_class = forms.TrueFalseQuestionForm
          question = question.truefalsequestion
      else:
          form_class = forms.MultipleChoiceQuestionForm
          question = question.multiplechoicequestion

      form = form_class(instance=question)
      answer_forms = forms.AnswerInlineFormset(
          queryset=form.instance.answer_set.all()
      )

      if request.method == 'POST':
          form = form_class(request.POST, instance=question)
          answer_forms = forms.AnswerInlineFormset(
              request.POST,
              queryset=form.instance.answer_set.all()
          )

          if form.is_valid() and answer_forms.is_valid():
              form.save()
              answers = answer_forms.save(commit=False)
              for answer in answers:
                  answer.question = question
                  answer.save()
              # If you use `commit=False`, objects will not be deleted
              # automatically. You must call `delete()` on each object.
              for answer in answer_forms.deleted_objects:
                  answer.delete()
              messages.success(request, 'Updated question')
              return HttpResponseRedirect(question.quiz.get_absolute_url())

      return render(request, 'courses/question_form.html', {
          'quiz': question.quiz,
          'form': form,
          'formset': answer_forms,
      })
  ```

  ```html
  # ./django-basics/learning_site/courses/templates/courses/question_form.html

  # ...

  <form action="" method="POST">
    {% csrf_token %}
    {{ form.as_p }}

    <!-- `formset.management_form` is a special set of fields that controls how many items are represented, how many forms there are, etc. Must be included when parsing `formset` internals. -->
    {{ formset.management_form }}

    <table>
      <thead>
        <tr>
          <th>Order</th>
          <th>Text</th>
          <th>Correct?</th>
          <th>Delete?</th>
        </tr>
      </thead>
      <!-- Class required for ordering script (see 'Custom Form Media'). -->
      <tbody class="order">
        {% for form in formset %}
          <!-- Class required for dynamic jQuery formset (see 'Custom Form Media'). -->
            <tr class="answer-form {% if form.instance.pk %}item{% else %}new{% endif %}">
            <td>{{ form.id }}{{ form.order }}</td>
            <td>{{ form.text }}</td>
            <td>{{ form.correct }}</td>
            {% if form.instance.pk %}
              <td>{{ form.DELETE }}</td>
            {% else %}
              <td></td>
            {% endif %}
          </tr>
        {% endfor %}
      </tbody>
    </table>

    <input type="submit" value="Save">
  </form>
  ```

- Course Notes:
  - Recommended [**tutorial**](https://whoisnicoleharris.com/2015/01/06/implementing-django-formsets.html) by Nicole Harris.

  - Consider using a [**form wizard**](https://django-formtools.readthedocs.io/en/latest/wizard.html#) for more advanced forms.

#### Custom Form Media

- You may sometimes need to use special static files (e.g., CSS, JS, or images) to make forms work as desired. Example of how to make an inline formset orderable via drag-and-drop:

  ```python
  # ./django-basics/learning_site/courses/forms.py

  # ...

  class QuestionForm(forms.ModelForm):
      class Media:
          css = {'all': ('courses/css/order.css',)}
          js = (
              'courses/js/vendor/jquery.fn.sortable.min.js',
              'courses/js/order.js',
          )


  class TrueFalseQuestionForm(QuestionForm):
      # ...


  class MultipleChoiceQuestionForm(QuestionForm):
      # ...
  ```

  ```html
  # ./django-basics/learning_site/courses/templates/courses/question_form.html

  # ...

  {% block css %}
    {{ form.media.css }}
  {% endblock %}

  {% block javascript %}
    {% load static %}
    {{ form.media.js }}
    <script src="{% static 'js/vendor/jquery.formset.js' %}"></script>
    <script>
      $('.answer-form').formset({
        addText: 'Add Answer',
        deleteText: 'Remove'
      });
    </script>
  {% endblock %}
  ```

  - **NOTE:** This example relies upon the jQuery library being imported as a dependency in the main `layout.html` file.

## Django ORM

### Sale Old ORM

#### Let's Review

- Working with a `Course` model:

  - Get all courses: `Course.objects.all()`
  - Get none of the courses: `Course.objects.none()`
  - Get a single couse: `Course.objects.get(**kwargs)`
  - Make a new course: `Course.objects.create(**kwargs)`
  - Save changes to a course: `Course.objects.save(**kwargs)`

#### Model Upgrades

- You can use [fixtures](https://docs.djangoproject.com/en/3.0/howto/initial-data/) to provide initial data for models. You can create fixture data with `python manage.py dumpdata` and then optionally provide an app or model name. You can load that data with `python manage.py loaddata` and then provide the name of the fixture file, e.g.:

  ```
  $ python manage.py loaddata fixtures.json
  ```

#### Django Debug Toolbar

- Install the [**Django Debug Toolbar**](https://django-debug-toolbar.readthedocs.io/en/1.4/index.html) (DjDT) by running the following command:

  ```
  $ pip install django-debug-toolbar
  ```

- DjDT requires that the environment's `DEBUG` variable be set to `True`, and that the environment be running as `localhost`. To activate DjDT in your application:
  1. Go to your app's `settings.py` file.
  2. Add `'debug_toolbar'` to the `INSTALLED_APPS` variable anywhere after `django.contrib.staticfiles` (as DjDT relies upon some static files).
  3. Add `'debug_toolbar.middleware.DebugToolbarMiddleware'` to the `MIDDLEWARE` variable.

      - **NOTE:** You should include the Debug Toolbar middleware as early as possible in the list. However, it must come after any other middleware that encodes the response’s content, such as `GZipMiddleware`.

  4. Set the `INTERNAL_IPS` variable to `['127.0.0.1', '::1', '0.0.0.0']`.
  5. Set the `DEBUG_TOOLBAR_PATCH_SETTINGS` variable to `False`.
  6. Go to your app's `urls.py` file and add the following:

      ```python
      from django.urls import include, path, re_path
      from django.conf import settings

      # ...

      if settings.DEBUG:
          import debug_toolbar
          urlpatterns += [
              re_path(r'^__debug__/', include(debug_toolbar.urls)),
          ]
      ```

### Basic ORM Usage

#### Restricting Results

- You can refine a queryset by adding [**filter() conditions**](https://docs.djangoproject.com/en/3.0/topics/db/queries/#retrieving-specific-objects-with-filters).

- Example of filtering database results:

  ```python
  # ./django-basics/learning_site/courses/urls.py

  # ...

  urlpatterns = [
    # ...
    path('by/<slug:teacher>/', views.courses_by_teacher, name='by_teacher'),
    path('search/', views.search, name='search'),
    # ...
  ]
  ```

  ```python
  # ./django-basics/learning_site/courses/views.py

  # ...

  def courses_by_teacher(request, teacher):
      # teacher = models.User.objects.get(username=teacher)
      # courses = teacher.course_set.all()

      # Simpler way to query courses by teacher, rather than using the
      # commented out code above. This method is also preferred because
      # it will just produce an empty queryset rather than a 404 error
      # if the given teacher name does not exist in the database.
      courses = models.Course.objects.filter(teacher__username=teacher)

      return render(request, 'courses/course_list.html', {'courses': courses})


  def search(request):
      term = request.GET.get('q')
      # Get courses where the title contains the term (case insensitive).
      courses = models.Course.objects.filter(title__icontains=term)
      return render(request, 'courses/course_list.html', {'courses': courses})
  ```

  ```html
  # ./django-basics/learning_site/templates/layout.html

  # ...

  <form action="{% url 'courses:search' %}" method="GET">
    <ul>
      <li><input type="search" name="q"></li>
      <li><button type="button">Search</button></li>
    </ul>
  </form>
  ```

#### Exclusivity

- You can use the `exclude()` method as an inverse corollary of the `filter()` method. Example:

  ```
  (InteractiveConsole)

  >>> from courses.models import Course

  >>> Course.objects.exclude(subject__in=['Python', 'Java'])

  <QuerySet [<Course: Collections>, <Course: OOP>, <Course: Testing>, <Course: Build a Simple Android App>, <Course: Android Activity Lifecycle>, <Course: SQL Basics>, <Course: Modifying Data with SQL>, <Course: jQuery Basics>, <Course: Build a Simple Dynamic Site with Node.js>, <Course: Build a Basic PHP Website>]>
  ```

#### Updates and Deletes

- Example of how to update a field in all records at once in the Python shell:

  ```
  (InteractiveConsole)

  >>> from courses.models import Course

  >>> Course.objects.update(published=True)

  15
  ```

- The `update()` and `delete()` methods target all records for a given model. If you want to avoid updating all records, you can include a `filter()` or `exclude()` statement, e.g.:

  ```
  >>> sql_courses = Course.objects.filter(subject__icontains='sql')

  >>> sql_courses

  <QuerySet [<Course: SQL Basics>, <Course: Modifying Data with SQL>]>

  >>> sql_courses.delete()

  (15, {'courses.Text': 0, 'courses.Answer': 7, 'courses.MultipleChoiceQuestion': 2, 'courses.Question': 2, 'courses.Quiz': 2, 'courses.Course': 2})

  >>> sql_courses

  <QuerySet []>
  ```

#### The Miracle of Creation

- Examples of how to create model instances outside of a model form using `create()` and `bulk_create()`:

  ```
  >>> from django.contrib.auth.models import User

  >>> teacher = User.objects.get(username='bavila')

  >>> course = Course.objects.create(teacher=teacher, subject='Python', title='Django Basics')

  >>> course.id

  22

  >>> Course.objects.bulk_create([
  ...     Course(teacher=teacher, title='Django Forms', subject='Python'),
  ...     Course(teacher=teacher, title='Django ORM', subject='Python')
  ... ])

  [<Course: Django Forms>, <Course: Django ORM>]

  >>> Course.objects.filter(title__icontains='django')

  <QuerySet [<Course: Customizing Django Templates>, <Course: Django Basics>, <Course: Django Forms>, <Course: Django ORM>]>
  ```

- Similar to the `get_object_or_404()` method, Django offers the `get_or_create()` method that checks to see if a record exists using all of the attributes passed to it. If the record does exist, it will be returned. If not, the record will be created and returned. The method also returns a boolean value indicating whether or not a new record was created, e.g.:

  ```
  >>> Course.objects.get_or_create(teacher=teacher, title='Django Forms', subject='Python')

  (<Course: Django Forms>, False)

  >>> Course.objects.get_or_create(teacher=teacher, title='Django REST Framework', subject='Python')

  (<Course: Django REST Framework>, True)
  ```

#### Take Control

- Example of how to use the `values()` method:

  ```python

  # ./django-basics/learning_site/courses/templatetags/course_extras.py

  @register.inclusion_tag('courses/course_nav.html')
  def nav_courses_list():
      """Returns dictionary of the 5 most recent courses to display in navigation pane."""
      # The `-` before `created_at` indicates items will be sorted in descending order.
      # `values()` returns a list of dictionaries (one for each selected instance).
      # Each dict's keys are the model's attributes. If you pass specific
      # attributes as arguments, then only those attributes will be included.
      courses = Course.objects.filter(published=True).order_by(
          '-created_at').values('id', 'title')[:5]
      return {'courses': courses}
  ```

  - **NOTE:** Alternatively, you could use [values_list](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#values-list), which returns a list of tuples, rather than a list of dictionaries. `values_list()` is most useful when you need to produce an ordered, structured representation of model instances.

- Example of `datetimes()`:

  ```
  >>> from courses.models import Course

  >>> dates = Course.objects.datetimes('created_at', 'year')

  >>> dates

  <QuerySet [datetime.datetime(2016, 1, 1, 0, 0, tzinfo=<DstTzInfo 'Pacific/Honolulu' HST-1 day, 14:00:00 STD>), datetime.datetime(2019, 1, 1, 0, 0, tzinfo=<DstTzInfo 'Pacific/Honolulu' HST-1 day, 14:00:00 STD>), datetime.datetime(2020, 1, 1, 0, 0, tzinfo=<DstTzInfo 'Pacific/Honolulu' HST-1 day, 14:00:00 STD>)]>
  ```

### Total Control

#### Brought to You by the Letter F

- [**F() objects**](https://docs.djangoproject.com/en/3.0/ref/models/expressions/#f-expressions) are useful when you need to access database values in real-time. These objects let you refer to a value of a field as it currently is in the database, instead of how it is in an instance that may be outdated (helps to avoid race conditions), e.g.:

  ```
  # Example assumes `quiz.times_taken` starts at 0.

  >>> from courses.models import Quiz

  >>> from django.db.models import F

  >>> quiz = Quiz.objects.latest('id')

  >>> quiz.times_taken = F('times_taken') + 1

  >>> quiz.save()

  >>> quiz.times_taken

  <CombinedExpression: F(times_taken) + Value(1)>

  >>> quiz.refresh_from_db()

  >>> quiz.times_taken

  1

  >>> Quiz.objects.all().update(times_taken=F('times_taken')+1)

  >>> quiz.refresh_from_db()

  >>> quiz.times_taken

  2
  ```

#### Mind your Ps and Qs

- You can perform complex lookups with [**Q objects**](https://docs.djangoproject.com/en/3.0/topics/db/queries/#complex-lookups-with-q-objects), e.g.:

  ```python
  # ./django-basics/learning_site/courses/views.py

  from django.db.models import Q

  # ...

  def search(request):
      term = request.GET.get('q')
      # Get courses where the title contains the term (case insensitive).
      courses = models.Course.objects.filter(
          # Q objects are independent queries. The pipe character acts as an
          # "OR" operator (i.e., a UNION query). If you separate the two
          # queries with a comma, that acts as an "AND" operator.
          Q(title__icontains=term)|Q(description__icontains=term),
          # Note that `published=True` is a keyword argument, while the Q
          # objects are non-keywords arguments. Keyword arguments must ALWAYS
          # go after non-keyword arguments.
          published=True
      )
      return render(request, 'courses/course_list.html', {'courses': courses})
  ```

- **NOTE:** It may often be better to use a dedicated search engine like Elasticsearch rather than building a solution with Q objects.

#### Aggregate and Annotate

- [**Annotations**](https://docs.djangoproject.com/en/3.0/topics/db/aggregation/) let you run SQL operations on each item in a queryset and then append the result as a new attribute. While **annotations** are run on each individual item in a queryset, **aggregates** are run on the entire queryset (and they return a dictionary rather than a queryset)

- Example:

  ```python
  # ./django-basics/learning_site/courses/views.py

  from django.db.models import Q, Count, Sum

  # ...

  def course_list(request):
      courses = models.Course.objects.filter(
          published=True
      ).annotate(
          # `total_steps` will be added as a new attribute on each queryset.
          # Add `distinct=True` so each text and quiz are only counted once.
          total_steps=Count('text', distinct=True)+Count('quiz', distinct=True)
      )
      total = courses.aggregate(total=Sum('total_steps'))
      email = 'questions@learning_site.com'
      return render(request, 'courses/course_list.html', {
          'courses': courses,
          'total': total,
          'email': email,
      })
  ```

- **NOTE:** Aggregates can add a significant amount to your query time, so you should always monitor them with DjDT.

#### Related Records

- You can use certain ORM functions to help reduce the number of superfluous queries made against the database, e.g.:

  ```python
  # ./django-basics/learning_site/courses/views.py

  from django.http import HttpResponseRedirect, Http404

  # ...

  def course_detail(request, pk):
      try:
          # `prefetch_related` will fetch everything in the `quiz_set` and the
          # `text_set` and assign them to the items in the resulting queryset.
          # Generates 4 SQL queries (courses, quiz sets, text sets, question sets).
          course = models.Course.objects.prefetch_related(
              'quiz_set', 'text_set', 'quiz_set__question_set'
          ).get(pk=pk, published=True)
      except models.Course.DoesNotExist:
          raise Http404
      else:
          steps = sorted(chain(
              course.text_set.all(),
              course.quiz_set.all()
          ), key=lambda step: step.order)
      return render(request, 'courses/course_detail.html', {
          'course': course,
          'steps': steps,
      })


  def quiz_detail(request, course_pk, step_pk):
      try:
          # `select_related` gets foreign key related records.
          step = models.Quiz.objects.select_related(
              'course'
          ).prefetch_related(
              'question_set', 'question_set__answer_set'
          ).get(
              course_id=course_pk, pk=step_pk, course__published=True
          )
      except models.Quiz.DoesNotExist:
          raise Http404
      else:
          return render(request, 'courses/step_detail.html', {'step': step})
  ```

- Teacher's Notes:

  `.select_related()` and `.prefetch_related()`.

  Remember the direction each of these goes. `select_related` is used on the model when you have the `ForeignKey` field. `prefetch_related` is used on the model that's related ***to*** by the `ForeignKey` field.

  `prefetch_related` won't always reduce the number of queries. It helps to prevent extra queries being run in your templates, though, by fetching and attaching the data before the template is ever rendered.

  `select_related`, when used correctly, can drastically reduce the number of queries you run.

- Two additional guidelines from the lecturer:

  1. `prefetch_related` is for getting lots of other items. This is the method you want if you're following a "reverse relationship", like "quiz questions".

  2. `select_related` is for getting smaller amounts of items, usually just one. Usually this will relate to a foreign key field on the model you're originally selecting, like going from question to quiz.

## Customizing the Django Admin

### Using the Django Admin

#### Your First Admin Customization

- To begin customizing the admin view, (1) create a directory named `admin/` under the `templates/` directory at the project level, and (2) create a file named `base_site.html` and insert the following code that can be modified as needed (obtained from the Django source code, available [here](https://github.com/django/django/blob/master/django/contrib/admin/templates/admin/base_site.html)):

  ```html
  {% extends "admin/base.html" %}

  {% block title %}{{ title }} | {{ site_title|default:_('Django site admin') }}{% endblock %}

  {% block branding %}
  <h1 id="site-name"><a href="{% url 'admin:index' %}">{{ site_header|default:_('Django administration') }}</a></h1>
  {% endblock %}

  {% block nav-global %}{% endblock %}
  ```

  - **NOTE:** Refer to [this page](https://github.com/django/django/tree/master/django/contrib/admin/templates/admin) of the source code to see all admin templates.

#### Changing Field Order

- By default, Django's admin displays all fields for each model in the order they appear in the class. You can specify which fields appear in the admin view and their order as follows:

  ```python
  # ./django-basics/learning_site/courses/admin.py

  from django.contrib import admin

  from . import models


  class QuizAdmin(admin.ModelAdmin):
      fields = ['course', 'title', 'description', 'order', 'total_questions']


  admin.site.register(models.Quiz, QuizAdmin)
  ```

### Customizing the List View

#### Adding Search and Filters

- You can add a **search field** and **filter** to any admin list view (e.g., Home > Courses > Courses):

  ```python
  # ./django-basics/learning_site/courses/admin.py

  class CourseAdmin(admin.ModelAdmin):
      inlines = [TextInline, QuizInline]
      # Insert the name of attributes that will be made searchable.
      search_fields = ['title', 'description']
      # Filter courses by creation date and "live" status.
      list_filter = ['created_at', 'published']
  ```

#### Building Custom Filters

- You can create your own classes that act as custom filters, e.g.:

  ```python
  # ./django-basics/learning_site/courses/admin.py

  class YearListFilter(admin.SimpleListFilter):
      # `title` appears after the word "By" in the filter sidebar.
      title = 'year created'
      # `parameter_name` is used in the URL whenever the filter is selected.
      parameter_name = 'year'

      # Creates the clickable links for the filter. Returns a tuple of tuples.
      def lookups(self, request, model_admin):
          return (
              # First value appears in the URL, the second in the sidebar.
              ('2016', '2016'),
              ('2019', '2019'),
              ('2020', '2020'),
          )

      # Returns the objects that fit the parameters of the filter.
      def queryset(self, request, queryset):
          if self.value():
              return queryset.filter(
                  created_at__gte=date(int(self.value()), 1, 1),
                  created_at__lte=date(int(self.value()), 12, 31)
              )


  class CourseAdmin(admin.ModelAdmin):
      inlines = [TextInline, QuizInline]
      search_fields = ['title', 'description']
      list_filter = ['created_at', 'published', YearListFilter]
  ```

#### Customizing What You See

- You can customize a list view to show more than just the main piece of information (i.e., whatever is returned by the `__str__` method of your model) about an object:

  ```python
  # ./django-basics/learning_site/courses/admin.py

  class CourseAdmin(admin.ModelAdmin):
      inlines = [TextInline, QuizInline]
      search_fields = ['title', 'description']
      list_filter = ['created_at', 'published', YearListFilter]
      # Show creation date and published status with title in list view.
      list_display = ['title', 'created_at', 'published']
  ```

#### Customizing Attributes

- You can use methods as custom attributes on your models, which can then be displayed in the list view of the admin site, e.g.:

  ```python
  # ./django-basics/learning_site/courses/models.py

  class Course(models.Model):
      created_at = models.DateTimeField(auto_now_add=True)
      title = models.CharField(max_length=255)
      description = models.TextField()
      teacher = models.ForeignKey(
          User,
          on_delete=models.CASCADE,
      )
      subject = models.CharField(default='', max_length=100)
      published = models.BooleanField(default=False)

      def __str__(self):
          return self.title

      def time_to_complete(self):
          # Must import `course_extras` within this method rather than at the top
          # of the file because `course_extras` imports the `Course` model as a
          # dependency. Importing `course_extras` at the top of this file (before
          # the `Course` model is declared) will lead to a recursive import error.
          from courses.templatetags.course_extras import time_estimate
          return '{} min'.format(time_estimate(len(self.description.split())))
  ```

  ```python
  # ./django-basics/learning_site/courses/admin.py

  class CourseAdmin(admin.ModelAdmin):
      inlines = [TextInline, QuizInline]
      search_fields = ['title', 'description']
      list_filter = ['created_at', 'published', YearListFilter]
      # `time_to_complete` will show, e.g.: "2 min"
      list_display = ['title', 'created_at', 'published', 'time_to_complete']
  ```

#### Editing the List View

- You can use `list_editable` to edit items in your database directly from the list view without entering a detail view, e.g.:

  ```python
  # ./django-basics/learning_site/courses/admin.py

  class QuestionAdmin(admin.ModelAdmin):
      inlines = [AnswerInline]
      search_fields = ['prompt']
      list_display = ['prompt', 'quiz', 'order']
      list_editable = ['quiz', 'order']
  ```

### Customizing the Detail View

#### Customize the Look of the Detail View

- You can use [**fieldsets**](https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fieldsets) to customize how the detail view looks, including grouping related fields together, adding horizontal select options, and showing choices in tabular format; e.g.:

  ```python
  # ./django-basics/learning_site/courses/admin.py

  class TextAdmin(admin.ModelAdmin):
      # NOTE: Do not use `fields` when using `fieldsets`.

      # `fieldsets` is a list of two-tuples. Each two-tuple represents a
      # separate section of the form.
      fieldsets = (
          # The first element is the heading that will be displayed above the
          # fieldset; the second element consists of the field options.
          (None, {
              'fields': ('course', 'title', 'order', 'description')
          }),
          ('Add content', {
              # Trailing comma indicates this is a tuple.
              'fields': ('content',),
              'classes': ('collapse',)  # Makes the section collapsible.
          })
      )
  ```

#### Horizontal Select and TabularInline

- You can replace a dropdown menu with a selection of radio buttons, and change fields from stacking on top of each other to being in a tabular format; e.g.:

  ```python
  # ./django-basics/learning_site/courses/admin.py

  class AnswerInline(admin.TabularInline):
      model = models.Answer

  # ...

  class QuestionAdmin(admin.ModelAdmin):
      inlines = [AnswerInline]
      search_fields = ['prompt']
      list_display = ['prompt', 'quiz', 'order']
      list_editable = ['quiz', 'order']
      # Displays the quiz options as a set of horizontal radio buttons.
      radio_fields = {'quiz': admin.HORIZONTAL}
  ```

#### Making a Text Preview

- You can add a WYSIWYG editor preview by modifying the default `change_form` and `fieldset` HTML templates. Make duplicates of each file within your project's `templates/admin/{APP}/{MODEL}/` directory. See the following files for details:

  - `django-basics/learning_site/templates/admin/courses/course/change_form.html`

  - `django-basics/learning_site/templates/admin/courses/course/includes/fieldset.html`

- **NOTE:** Rather than copying the original template from the GitHub repo, you can always use DjDT's "Templates" tab to determine (1) which admin templates are being used, and (2) the filepath to the template in the source code on your local machine. It is best to copy from these local templates, as the version of the template from the `master` branch of the [Django source code](https://github.com/django/django/blob/master/django/contrib/admin/templates/admin/) may not be compatible with that installed on your local machine.

#### Finishing the Markdown Preview

- Refer to the following files to see how a Markdown preview box was created:

  - `django-basics/learning_site/assets/js/vendor/markdown.js`
  - `django-basics/learning_site/assets/js/preview.js`
  - `django-basics/learning_site/assets/css/preview.css`

  ```python
  # ./django-basics/learning_site/courses/admin.py

  class CourseAdmin(admin.ModelAdmin):
      inlines = [TextInline, QuizInline]
      search_fields = ['title', 'description']
      list_filter = ['created_at', 'published', YearListFilter]
      list_display = ['title', 'created_at', 'published', 'time_to_complete']
      list_editable = ['published']

      class Media:
          js = ('js/vendor/markdown.js', 'js/preview.js')
          css = {
              'all': ('css/preview.css',),
          }
  ```

  - **NOTE:** The implementation is rather crude (as the Markdown preview only updates when the form is saved, rather than in real time). It should not likely ever be implemented as is, and it is only included here for reference.

#### Adding Custom Admin Actions

- You can add custom admin actions to perform bulk operations (e.g., setting multiple courses to "Published" from the list view):

  ```python
  # ./django-basics/learning_site/courses/models.py

  STATUS_CHOICES = (
      ('i', 'In Progress'),
      ('r', 'In Review'),
      ('p', 'Published'),
  )

  class Course(models.Model):
      created_at = models.DateTimeField(auto_now_add=True)
      title = models.CharField(max_length=255)
      description = models.TextField()
      teacher = models.ForeignKey(
          User,
          on_delete=models.CASCADE,
      )
      subject = models.CharField(default='', max_length=100)
      published = models.BooleanField(default=False)
      status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='i')
  ```

  ```python
  # ./django-basics/learning_site/courses/admin.py

  def make_published(modeladmin, request, queryset):
      queryset.update(status='p', published=True)

  # This is the message users will see when using the "Action" dropdown menu
  # to change the published status of their courses.
  make_published.short_description = 'Mark selected courses as Published'

  class CourseAdmin(admin.ModelAdmin):
      inlines = [TextInline, QuizInline]
      search_fields = ['title', 'description']
      list_filter = ['created_at', 'published', YearListFilter]
      list_display = ['title',
                      'created_at',
                      'time_to_complete',
                      'published',
                      'status']
      list_editable = ['status']
      # Add the `make_published()` function to the "Action" dropdown menu.
      actions = [make_published]
  ```

## Django Class-based Views

### Classy Views

#### What are Class-based Views?

- Django's [**class-based views**](https://docs.djangoproject.com/en/3.0/topics/class-based-views/) allow you to structure your views and reuse code by harnessing inheritance and mixins. The generic views provided by Django can provide most of the functionality needed by a view.

- See also: [**Classy Class-Based Views**](https://ccbv.co.uk/) for detailed descriptions about each of Django's class-based generic views.

#### The View Class

- The most basic class for creating views is [**View**](http://ccbv.co.uk/projects/Django/3.0/django.views.generic.base/View/). Example:

  ```python
  # ./django-basics/django_cbvs/djangoal/djangoal/views.py

  from django.http import HttpResponse
  from django.views.generic import View


  class HelloWorldView(View):
      # Each view based on the `View` class accepts the `get()` method.
      def get(self, request):
          return HttpResponse('Hello World')
  ```

  ```python
  # ./django-basics/django_cbvs/djangoal/djangoal/urls.py

  urlpatterns = [
      path('admin/', admin.site.urls),
      path('', views.home, name='home'),
      path('teams/', include('teams.urls', namespace='teams')),
      # The `HelloWorldView` must call the `as_view()` method because it is based
      # on the `View` class. The `as_view()` method creates an instance of the
      # class, configures the request object, and runs the class's dispatch
      # method. The dispatch method runs the correct class method based on the
      # incoming HTTP request (i.e., if the HTTP request is a `GET` request,
      # then the dispatch method with call the class's `get()` method).
      path('hello/', views.HelloWorldView.as_view(), name='hello')
  ]
  ```

- **NOTE:** The `View` class is generally only useful when you need to control _everything_ about how a view is managed. However, for most cases, you will most likely use Django's generic views that are aimed at solving specific problems.

#### Template View

- The [**TemplateView**](https://docs.djangoproject.com/en/3.0/ref/class-based-views/base/#templateview) renders a given template, with the context containing parameters captured in the URL. Example:

  ```python
  # ./django-basics/django_cbvs/djangoal/djangoal/views.py

  from django.views.generic import View, TemplateView

  class HomeView(TemplateView):
      template_name = 'home.html'

      # Gets/generates context dictionary that's used for rendering template.
      def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          # Add hardcoded value that's accessible to the template.
          context['games_today'] = 6
          return context
  ```

  ```html
  # ./django-basics/django_cbvs/djangoal/templates/home.html

  <p>
		There {{ games_today|pluralize:"is,are" }} {{ games_today }} game{{ games_today|pluralize }} today!
	</p>
  ```

#### ListView and DetailView

- Examples:

  ```python
  # ./django-basics/django_cbvs/djangoal/teams/views.py

  from django.views.generic import ListView, DetailView

  class TeamListView(ListView):
      model = models.Team
      # By default, Django sets the context name of the list to be generated
      # as both `object_list` and the lower-cased version of the model class's
      # name followed by `_list` (in this case, `team_list`). However, it you
      # want to change that name to something else, use `context_object_name`.
      context_object_name = 'teams'


  class TeamDetailView(DetailView):
      model = models.Team
  ```

  ```python
  # ./django-basics/django_cbvs/djangoal/teams/urls.py

  from django.urls import path

  from . import views

  app_name = 'teams'

  urlpatterns = [
      path('', views.TeamListView.as_view(), name='list'),
      path('<int:pk>/', views.TeamDetailView.as_view(), name='detail'),
  ]
  ```

#### CRUD View

- Basic example of `CreateView`, `UpdateView`, and `DeleteView`:

  ```python
  # ./django-basics/django_cbvs/djangoal/teams/models.py

  from django.db import models
  from django.urls import reverse


  class Team(models.Model):
      name = models.CharField(max_length=255)
      coach = models.ForeignKey(
          User,
          related_name='teams',
          on_delete=models.CASCADE,
      )
      practice_location = models.CharField(max_length=255)

      def __str__(self):
          return self.name

      def get_absolute_url(self):
          return reverse('teams:detail', kwargs={'pk': self.pk})
  ```

  ```python
  # ./django-basics/django_cbvs/djangoal/teams/views.py

  from django.urls import reverse_lazy
  from django.views.generic import (
      ListView, DetailView,
      CreateView, UpdateView, DeleteView
  )


  class TeamCreateView(CreateView):
      model = models.Team
      fields = ('name', 'practice_location', 'coach')


  class TeamUpdateView(UpdateView):
      model = models.Team
      fields = ('name', 'practice_location', 'coach')


  class TeamDeleteView(DeleteView):
      model = models.Team
      # `reverse_lazy` is evaluated when the view is instantiated (as opposed to
      # `reverse`, which is evaluated when this file is read & parsed by Python).
      # So it won't matter if the URL for the list view doesn't exist yet when
      # the file is read.
      success_url = reverse_lazy('teams:list')
  ```

  ```python
  # ./django-basics/django_cbvs/djangoal/teams/urls.py

  urlpatterns = [
      path('', views.TeamListView.as_view(), name='list'),
      path('<int:pk>/', views.TeamDetailView.as_view(), name='detail'),
      path('create/', views.TeamCreateView.as_view(), name='create'),
      path('edit/<int:pk>/', views.TeamUpdateView.as_view(), name='update'),
      path('delete/<int:pk>/', views.TeamDeleteView.as_view(), name='delete'),
  ]
  ```

  ```html
  # ./django-basics/django_cbvs/djangoal/teams/templates/teams/team_form.html

  <!-- Used whenever a team is created or updated. The name follows a Django
      convention in which CreateView/UpdateView templates use the lowercased
      model name followed by `_form`. -->

  {% extends "teams/_layout.html" %}

  {% block body_content %}
  <h1>{% if not form.instance.pk %}Create Team{% else %}Edit {{ form.instance.name }}{% endif %}</h1>

  <form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" class="btn btn-primary" value="Save">
  </form>
  {% endblock %}
  ```

  ```html
  # ./django-basics/django_cbvs/djangoal/teams/templates/teams/team_confirm_delete.html

  <!-- Used whenever a team is deleted. The name follows a Django convention
      in which DeleteView confirmation templates use the lowercased model
      name followed by `_confirm_delete`. -->
  {% extends "teams/_layout.html" %}

  {% block body_content %}
  <h1>Delete {{ team.name }}?</h1>

  <form method="POST">
    {% csrf_token %}
    <input type="submit" class="btn btn-danger" value="Delete">
    <a href="{% url 'teams:detail' pk=team.pk %}">Cancel</a>
  </form>
  {% endblock %}
  ```

### Customizing Class-based Views

#### Overriding Methods

- Example of overriding `get_initial` and `get_queryset` methods:

  ```python
  # ./django-basics/django_cbvs/djangoal/teams/views.py

  class TeamCreateView(CreateView):
      model = models.Team
      fields = ('name', 'practice_location', 'coach')

      # `get_initial` populates a form with starter data. Here, the form
      # will begin with the logged-in user assigned as the coach.
      def get_initial(self):
          initial = super().get_initial()
          initial['coach'] = self.request.user.pk
          return initial


  class TeamDeleteView(DeleteView):
      model = models.Team
      success_url = reverse_lazy('teams:list')

      # Override the default `get_queryset` method to say that only a superuser
      # can delete any team. Otherwise, a user can only delete teams for which
      # the user is a coach.
      def get_queryset(self):
          # All class-based views have a `request` attribute.
          if not self.request.user.is_superuser:
              return self.model.objects.filter(coach=self.request.user)
          return self.model.objects.all()
  ```

#### Franken-Views

- It is possible to combine multiple views (although it is likely better to use mixins, which are described below). Example of combining a Create form on a list view page:

  ```python
  # ./django-basics/django_cbvs/djangoal/teams/views.py

  # The order of arguments matters when combining views. In this case, you
  # want `CreateView` to come before `ListView`, because the `CreateView`
  # build process looks for an `object` attribute, but the `ListView` output
  # does not produce an `object` attribute.
  class TeamListView(CreateView, ListView):
      model = models.Team
      context_object_name = 'teams'
      fields = ('name', 'practice_location', 'coach')
      template_name = 'teams/team_list.html'
  ```

  ```html
  # ./django-basics/django_cbvs/djangoal/teams/templates/teams/team_list.html

  {% block body_content %}
  <h1 class="page-header">Dashboard</h1>
  <div class="row placeholders">
    {% for team in teams %}
      {% team_avatar team %}
    {% endfor %}
  </div>

  {% if user.is_authenticated %}
  <hr>

  <form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" class="btn btn-primary" value="Save">
  </form>
  {% endif %}
  {% endblock %}
  ```

#### Mixins

- [**Mixins**](https://docs.djangoproject.com/en/3.0/topics/class-based-views/mixins/) are small classes that add or augment a single feature on a larger class (in order to customize and modify a view).

- Four major built-in mixins:
  - [AccessMixin](https://ccbv.co.uk/projects/Django/3.0/django.contrib.auth.mixins/AccessMixin/)
  - [LoginRequiredMixin](https://ccbv.co.uk/projects/Django/3.0/django.contrib.auth.mixins/LoginRequiredMixin/)
  - [PermissionRequiredMixin](https://ccbv.co.uk/projects/Django/3.0/django.contrib.auth.mixins/PermissionRequiredMixin/)
  - [UserPassesTestMixin](https://ccbv.co.uk/projects/Django/3.0/django.contrib.auth.mixins/UserPassesTestMixin/)

- See additional mixins on [**Django Braces**](https://django-braces.readthedocs.io/en/latest/).

- You can create your own mixins by adding a `mixins.py` file to your app directory. Example of a custom mixin for dynamically setting a page title:

  ```python
  # ./django-basics/django_cbvs/djangoal/teams/mixins.py

  class PageTitleMixin:
      page_title = ''

      # Allows page title to be set dynamically.
      def get_page_title(self):
          return self.page_title

      def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context['page_title'] = self.get_page_title()
          return context
  ```

  ```python
  from django.contrib.auth.mixins import LoginRequiredMixin
  from . import mixins

  # `LoginRequiredMixin` comes first, because you want to ensure that the
  # user is logged in before creating the view.
  class TeamCreateView(LoginRequiredMixin, mixins.PageTitleMixin, CreateView):
      model = models.Team
      fields = ('name', 'practice_location', 'coach')
      page_title = 'Create a new team'

      # `get_initial` populates a form with starter data. Here, the form
      # will begin with the logged-in user assigned as the coach.
      def get_initial(self):
          initial = super().get_initial()
          initial['coach'] = self.request.user.pk
          return initial


  class TeamUpdateView(LoginRequiredMixin, mixins.PageTitleMixin, UpdateView):
      model = models.Team
      fields = ('name', 'practice_location', 'coach')

      def get_page_title(self):
          # `get_object()` gets the object currently being editted.
          obj = self.get_object()
          return 'Update {}'.format(obj.name)
  ```

  ```html
  # ./django-basics/django_cbvs/djangoal/teams/templates/teams/team_form.html

  <h1>{{ page_title }}</h1>
  ```

## Django REST Framework

### Installation

- Install the [Django REST framework](https://www.django-rest-framework.org/) using `pip`:

  ```
  $ pip install djangorestframework
  ```

- Add `rest_framework` to your `INSTALLED_APPS` in `settings.py`.

- Configure `REST_FRAMEWORK` settings (such as authentication and permissions) in `settings.py`; e.g.:

  ```python
  # ./django-basics/django_rest_framework/ed_reviews/ed_reviews/settings.py

  # REST Framework - contains all DRF settings
  REST_FRAMEWORK = {
      'DEFAULT_AUTHENTICATION_CLASSES': (
          'rest_framework.authentication.SessionAuthentication',
      ),
      'DEFAULT_PERMISSION_CLASSES': (
          # Unauthenticated users can only read data.
          'rest_framework.permissions.IsAuthenticatedOrReadOnly',
      ),
  }
  ```

- Set up URLs for authentication; e.g.:

  ```python
  # ./django-basics/django_rest_framework/ed_reviews/ed_reviews/urls.py

  urlpatterns = [
      path('admin/', admin.site.urls),
      path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
  ]
  ```

- Log in via `/api-auth/login/`.

  - **NOTE:** You will be redirected to the default route of `/accounts/profile/`, which would require another URL pattern of its own.

#### Model Serializers

- The [**ModelSerializer**](https://www.django-rest-framework.org/api-guide/serializers/#modelserializer) class can be used to turn model instances into JSON and vice versa. The `ModelSerializer` is similar to Django's model forms, and it can automatically generate fields from your models. The class includes automatically generated validators, and has the ability to create and update database objects.

- To begin using model serializers, create a new file named `serializers.py` in your app directory. Example:

  ```python
  # ./django-basics/django_rest_framework/ed_reviews/courses/serializers.py

  from rest_framework import serializers

  from . import models


  class ReviewSerializer(serializers.ModelSerializer):
      class Meta:
          model = models.Review
          fields = (
              'id',
              'course',
              'name',
              'email',
              'comment',
              'rating',
              'created_at',
          )
          # Sepcify that the `email` field can be supplied by the user,
          # but it will not be sent back out upon serialization.
          extra_kwargs = {
              'email': {'write_only': True}
          }


  class CourseSerializer(serializers.ModelSerializer):
      class Meta:
          model = models.Course
          fields = (
              'id',
              'title',
              'url',
          )
  ```

  ```
  (InteractiveConsole)

  >>> from rest_framework.renderers import JSONRenderer

  >>> from courses.models import Course

  >>> from courses.serializers import CourseSerializer

  >>> course = Course.objects.latest('id')

  >>> course.title

  'Python Collections'

  >>> serializer = CourseSerializer(course)

  >>> serializer

  CourseSerializer(<Course: Python Collections>):
      id = IntegerField(label='ID', read_only=True)
      title = CharField(max_length=255)
      url = URLField(max_length=200, validators=[<UniqueValidator(queryset=Course.objects.all())>])

  >>> serializer.data

  {'id': 2, 'title': 'Python Collections', 'url': 'https://teamtreehouse.com/library/python-collections'}

  >>> JSONRenderer().render(serializer.data)

  b'{"id":2,"title":"Python Collections","url":"https://teamtreehouse.com/library/python-collections"}'
  ```

  - **NOTE:** The final output provided by `JSONRenderer()` is a [**bytes literal**](https://docs.python.org/3/library/stdtypes.html#bytes) that needs to be converted to a string before it can be used.

#### GET Requests with APIView

- [**APIView**](https://www.django-rest-framework.org/api-guide/views/) is a subclass of Django's `View` class. The main difference is that the requests that are passed to the handler methods in `APIView` will be DRF request objects, instead of Django's HTTP request objects. DRF request objects are an extension of Django's standard HTTP request, but with additional support for flexible request parsing and request authentication. By using the DRF request object, you can treat JSON data/requests the same way that you would deal with form data.

- Example:

  ```python
  # ./django-basics/django_rest_framework/ed_reviews/courses/views.py

  from rest_framework.views import APIView
  from rest_framework.response import Response

  from . import models
  from . import serializers


  class ListCourse(APIView):
      # `format` controls the format of the output.
      def get(self, request, format=None):
          courses = models.Course.objects.all()
          # Use `many=True` when serializing multipe objects.
          serializer = serializers.CourseSerializer(courses, many=True)
          return Response(serializer.data)
  ```

  ```python
  # ./django-basics/django_rest_framework/ed_reviews/courses/urls.py

  from django.urls import path, include

  from . import views

  app_name = 'courses'

  urlpatterns = [
      path('', views.ListCourse.as_view(), name='course_list'),
  ]
  ```

  ```python
  # ./django-basics/django_rest_framework/ed_reviews/ed_reviews/urls.py

  urlpatterns = [
      # ...
      # Include API version number.
      path('api/v1/courses/', include('courses.urls', namespace='courses')),
  ]
  ```

#### POSTing to an APIView

- Example of how to handle a POST request:

  ```python
  # ./django-basics/django_rest_framework/ed_reviews/courses/views.py

  from rest_framework import status
  from rest_framework.views import APIView
  from rest_framework.response import Response

  from . import models
  from . import serializers


  class ListCreateCourse(APIView):
      def get(self, request, format=None):
          courses = models.Course.objects.all()
          serializer = serializers.CourseSerializer(courses, many=True)
          return Response(serializer.data)

      def post(self, request, format=None):
          serializer = serializers.CourseSerializer(data=request.data)
          # Returns a 400 Bad Request error if the data is not valid.
          serializer.is_valid(raise_exception=True)
          # `save()` both saves the data to the database and updates
          #  `serializer.data` to include all fields entered into the
          # database, such as the primary key and `created_at` values.
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
  ```

  ```python
  # ./django-basics/django_rest_framework/ed_reviews/courses/urls.py

  from django.urls import path, include

  from . import views

  app_name = 'courses'

  urlpatterns = [
      path('', views.ListCreateCourse.as_view(), name='course_list'),
  ]
  ```

### Make the REST Framework Work for You

#### Generic CRUD

- DRF includes [**generic views**](https://www.django-rest-framework.org/api-guide/generic-views/) that allow you to quickly build API views that map closely to your database models. Example:

  ```python
  # ./django-basics/django_rest_framework/ed_reviews/courses/views.py

  from rest_framework import generics

  from . import models
  from . import serializers


  # Extends a generic API view rather than the standard `APIView`.
  class ListCreateCourse(generics.ListCreateAPIView):
      queryset = models.Course.objects.all()
      # Specifies which serializer will be used on the queryset.
      serializer_class = serializers.CourseSerializer


  class RetrieveUpdateDestroyCourse(generics.RetrieveUpdateDestroyAPIView):
      queryset = models.Course.objects.all()
      serializer_class = serializers.CourseSerializer
  ```

  ```python
  # ./django-basics/django_rest_framework/ed_reviews/courses/urls.py

  from django.urls import path, include

  from . import views

  app_name = 'courses'

  urlpatterns = [
      path('', views.ListCreateCourse.as_view(), name='course_list'),
      # `RetrieveUpdateDestroyAPIView` expects a query parameter called `pk`.
      path('<pk>/', views.RetrieveUpdateDestroyCourse.as_view(), name='course_detail')
  ]
  ```

  - **NOTE:** This method of making a List/Create view replaces that shown in "POSTing to an APIView" above. It provides for a more succinct way to create such views. The form for submitting a POST request to the database is also configured to use HTML inputs in addition to raw JSON.

#### Overriding Generic View Methods

- Example of how to override generic view methods for filtering:

  ```python
  #. /django-basics/django_rest_framework/ed_reviews/courses/views.py

  # ...

  class ListCreateReview(generics.ListCreateAPIView):
      queryset = models.Review.objects.all()
      serializer_class = serializers.ReviewSerializer

      # Override the default `get_queryset` method to have it use `course_pk`.
      def get_queryset(self):
          return self.queryset.filter(course_id=self.kwargs.get('course_pk'))

      # This method is run when an object is created by the view.
      def perform_create(self, serializer):
          # Prevent the user from assigning a `course_pk` which differs from the
          # primary key of the course in which the review is being submitted.
          course = get_object_or_404(
              models.Course, pk=self.kwargs.get('course_pk')
          )
          serializer.save(course=course)


  class RetrieveUpdateDestroyReview(generics.RetrieveUpdateDestroyAPIView):
      queryset = models.Review.objects.all()
      serializer_class = serializers.ReviewSerializer

      # `get_object` is similar to `get_queryset`, but instead gets a
      # single item rather than multiple items.
      def get_object(self):
          # Get a single object from the queryset that has the specified
          # `course_id` and `pk`. Ensures that an object can only be
          # updated or destroyed based on the query parameters provided.
          return get_object_or_404(
              self.get_queryset(),
              course_id=self.kwargs.get('course_pk'),
              pk=self.kwargs.get('pk')
          )
  ```

  ```python
  # ./django-basics/django_rest_framework/ed_reviews/courses/urls.py

  # ...

  urlpatterns = [
      # ...
      path('<course_pk>/reviews/', views.ListCreateReview.as_view(), name='review_list'),
      path('<course_pk>/reviews/<pk>/', views.RetrieveUpdateDestroyReview.as_view(), name='review_detail'),
  ]
  ```

#### Viewsets and Routers

- [**Routers**](https://www.django-rest-framework.org/api-guide/routers/) are DRF's way of automating URL creation for API views. Routers are designed to work seamlessly with [**viewsets**](https://www.django-rest-framework.org/api-guide/viewsets/), which allow you to combine all of the logic for a set of related views into a single class. Instead of creating a `ListCreateAPIView` and `RetrieveUpdateDestroyAPIView` for every resources, you can do this all in one class.

- If you have ad hoc methods that should be routable, you can mark them as such with the [**@action decorator**](https://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions).

- Example:

  ```python
  # ./django-basics/django_rest_framework/ed_reviews/courses/views.py

  from rest_framework import viewsets
  from rest_framework.decorators import action
  from rest_framework.response import Response

  from . import models
  from . import serializers

  # ...

  class CourseViewSet(viewsets.ModelViewSet):
      queryset = models.Course.objects.all()
      serializer_class = serializers.CourseSerializer

      # This viewset only applies to the detail view (rather than the list
      # view), and it will only work for GET requests.
      @action(detail=True, methods=['get'])
      def reviews(self, request, pk=None):
          course = self.get_object()
          serializer = serializers.ReviewSerializer(
              course.reviews.all(), many=True
          )
          return Response(serializer.data)


  class ReviewViewSet(viewsets.ModelViewSet):
      queryset = models.Review.objects.all()
      serializer_class = serializers.ReviewSerializer
  ```

  ```python
  # ./django-basics/django_rest_framework/ed_reviews/ed_reviews/urls.py

  # ...

  from rest_framework import routers

  from courses import views

  router = routers.SimpleRouter()
  # Register viewsets with the router, and assign a prefix.
  router.register(r'courses', views.CourseViewSet)
  router.register(r'reviews', views.ReviewViewSet)

  urlpatterns = [
      # ...
      # Create URLs automatically for each viewset registered with the router.
      path('api/v2/', include((router.urls, 'ed_reviews'), namespace='apiv2')),
  ]
  ```

#### Customizing Viewsets

- You can customize viewsets to control exactly which HTTP methods your viewsets will respond to. Example:

  ```python
  # ./django-basics/django_rest_framework/ed_reviews/courses/views.py

  from rest_framework import mixins

  # ...

  """
  `ModelViewSet` essentially inherits from each of the following:
      - `mixins.CreateModelMixin`
      - `mixins.RetrieveModelMixin`
      - `mixins.UpdateModelMixin`
      - `mixins.DestroyModelMixin`
      - `mixins.ListModelMixin`
      - `viewsets.GenericViewSet`

  So if you want to customize a viewset that will not display a list view,
  then simply create a new model that inherits from `GenericViewSet` and
  all of the mixins execpt for `ListModelMixin`. The end result is that users
  can retrieve individual reviews (e.g., `/api/v2/courses/1/reviews/2/`), but
  they cannot retrieve a list of all reviews (e.g., `/api/v2/reviews/).
  Attempting to go to the latter will yield: "Method 'GET' not allowed."
  """
  # Mixins must be evaluated before the class they are modifying.
  class ReviewViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
      queryset = models.Review.objects.all()
      serializer_class = serializers.ReviewSerializer
  ```

- **NOTE:** It is also possible to create [**function-based views**](https://www.django-rest-framework.org/api-guide/views/#function-based-views) rather than class-based views, if desired.

#### Relations

- Use [**relations**](https://www.django-rest-framework.org/api-guide/relations/) to display foreign key relationships. Example:

  ```python
  # ./django-basics/django_rest_framework/ed_reviews/courses/serializers.py

  class CourseSerializer(serializers.ModelSerializer):
      """
      Automatically include any reviews related to a course instance.
      NOTE: This will bring in EVERY review related to the course, so
      this method is best when only working with limited amounts of data
      (ideally situations where there's just a one-to-one relationship).
      """
      # reviews = ReviewSerializer(many=True, read_only=True)

      """
      Alternative to the above, in which you only fetch the hyperlink(s)
      of related field(s), rather than all the data from the related object.
      `review-detail` is the automatically-generated view name for the
      viewset in the API v2 router. NOTE: This will still return ALL items.
      See: https://www.django-rest-framework.org/api-guide/routers/#simplerouter
      """
      # reviews = serializers.HyperlinkedRelatedField(many=True,
      #                                               read_only=True,
      #                                               view_name='apiv2:review-detail')

      """
      Another option in which you only fetch the primary key(s) of related
      field(s). This is generally the fastest option.
      """
      reviews = serializers.PrimaryKeyRelatedField(many=True,
                                                  read_only=True)

      class Meta:
          model = models.Course
          fields = (
              'id',
              'title',
              'url',
              # Should correspond to the `related_name` in `models.py`:
              'reviews',
          )
  ```

#### Pagination

- Use [**pagination**](https://www.django-rest-framework.org/api-guide/pagination/) to prevent situations in which thousands of related objects are included in a single API request.

- Set up the default pagination in the `REST_FRAMEWORK` dictionary in your project's `settings.py` file:

  ```python
  # ./django-basics/django_rest_framework/ed_reviews/ed_reviews/settings.py

  REST_FRAMEWORK = {
      # ...
      'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
      'PAGE_SIZE': 5,
  }
  ```

- **IMPORTANT:** The default pagination will be applied to all generic views, but it will not automatically work on your ad hoc views (i.e., those using the `@action` decorator). You will need to make your own calls to the paginator to handle the latter. Example:

  ```python
  # ./django-basics/django_rest_framework/ed_reviews/courses/views.py

  class CourseViewSet(viewsets.ModelViewSet):
      queryset = models.Course.objects.all()
      serializer_class = serializers.CourseSerializer

      # This viewset method only applies to the detail view (rather than
      # the list view), and it will only work for GET requests.
      @action(detail=True, methods=['get'])
      def reviews(self, request, pk=None):
          # Calls the `pagination_class` set in `settings.py` with the
          # specified page size.
          self.pagination_class.page_size = 1
          reviews = models.Review.objects.filter(course_id=pk)

          page = self.paginate_queryset(reviews)

          if page is not None:
              serializer = serializers.ReviewSerializer(page, many=True)
              return self.get_paginated_response(serializer.data)

          serializer = serializers.ReviewSerializer(reviews, many=True)
          return Response(serializer.data)
  ```

### Security and Customization

#### Token Authentication

- Token-based [**authentication**](https://www.django-rest-framework.org/api-guide/authentication/) takes advantage of a simple HTTP authentication method. Instead of making a user log in and keep a [**session**](https://docs.djangoproject.com/en/3.0/topics/http/sessions/#module-django.contrib.sessions) around (which will not be an option available on non-browser mobile applications), a user is assigned a token which is usually a randomly-generated string that the user provides to the server to prove their identity. Tokens

- To begin using tokens:
  1. Add `'rest_framework.authtoken'` to `INSTALLED_APPS` in your `settings.py` file, and
  2. Change the `REST_FRAMEWORK.DEFAULT_AUTHENTICATION_CLASSES` to use `TokenAuthentication`.

- Example of how to manually generate a token in the Python shell (normally you would set something up to automatically generate a token whenever a user signs up):

  ```
  (InteractiveConsole)

  >>> from rest_framework.authtoken.models import Token

  >>> from django.contrib.auth.models import User

  >>> user = User.objects.get(id=1)

  >>> user

  <User: kennethlove>

  >>> token = Token.objects.create(user=user)

  >>> token.key

  'b1cfa1c350e39202b68b87db80c2290d50ad932e'
  ```

  - **NOTE:** Tokens can be viewed in `/admin/authtoken/token`.

- The token generated above can now be used to submit POST requests that require authentication. The request's `Headers` must include a key of `Authorization` which has a value of `Token b1cfa1c350e39202b68b87db80c2290d50ad932e` (note the space between "Token" and the key).

#### Permissions

- [**Permissions**](https://www.django-rest-framework.org/api-guide/permissions/) decide whether a request should be granted or denied access. In addition to setting the `DEFAULT_PERMISSION_CLASSES` globally via `settings.py`, you can use permissions to protect a single, specific view. Example:

  ```python
  # ./django-basics/django_rest_framework/ed_reviews/courses/views.py

  # Only allow superusers to delete objects. All other users can peform
  # any other request.
  class SuperUserCanDelete(permissions.BasePermission):
      def has_permission(self, request, view):
          if request.method != 'DELETE' or request.user.is_superuser:
              return True
          return False


  class CourseViewSet(viewsets.ModelViewSet):
      # This will override the default permissions in `settings.py`.
      # The permission checks will run in the order they are listed.
      # Here, a non-superuser will not be able to delete a course,
      # even if they have that ability via Django permissions.
      permission_classes = (
          SuperUserCanDelete,
          permissions.DjangoModelPermissions
      )
  ```

- Also see [**Django Guardian**](https://django-guardian.readthedocs.io/en/stable/overview.html), which is an implementation of object permissions for Django and provides an extra authentication backend.

#### Enhancing Your Calm with Throttling

- [**Throttling**](https://www.django-rest-framework.org/api-guide/throttling/) controls the rate of requests that a client can make to an API.

- You can set global throttling rules via the `REST_FRAMEWORK` dictionary in `settings.py`, e.g.:

  ```python
  # ./django-basics/django_rest_framework/ed_reviews/ed_reviews/settings.py

  REST_FRAMEWORK = {
      # ...
      'DEFAULT_THROTTLE_CLASSES': (
          'rest_framework.throttling.AnonRateThrottle', # Non-authenticated users.
          'rest_framework.throttling.UserRateThrottle', # Authenticated users.
      ),
      'DEFAULT_THROTTLE_RATES': {
          'anon': '500/day',
          'user': '100/hour',
      }
  }
  ```

- DRF tracks the requests made in a given time limit via Django's cache backend settings. Django defaults to the local memory cache backend (which is primarily meant for local development and is not very efficient). Django provides other cache backend choices, and there are other third-party packages that can extend your options. In production, you may likely use the [**Memcached**](https://docs.djangoproject.com/en/3.0/topics/cache/#memcached) backend.

#### Customizing Validation

- Example of a custom serializer validation:

  ```python
  # ./django-basics/django_rest_framework/ed_reviews/courses/serializers.py

  class ReviewSerializer(serializers.ModelSerializer):
      class Meta:
          model = models.Review
          fields = (
              'id',
              'course',
              'name',
              'email',
              'comment',
              'rating',
              'created_at',
          )
          extra_kwargs = {
              'email': {'write_only': True}
          }

      # Just as with field-level validations for forms (e.g., `clean_field`),
      # custom serializer validation methods must be `validate_field`.
      def validate_rating(self, value):
          if value in range(1, 6):
              return value
          raise serializers.ValidationError(
              'Rating must be an integer between 1 and 5'
          )
  ```

- It is also possible to perform object-level validation across multiple fields, and for validators to be included on individual fields on a serializer. See the examples in the [official documentation](https://www.django-rest-framework.org/api-guide/serializers/#validation).

#### Customizing Serialization

- You can add custom data to your serializer output by using the [**SerializerMethodField**](https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield). Example:

  ```python
  # ./django-basics/django_rest_framework/ed_reviews/courses/serializers.py

  from django.db.models import Avg

  # ...

  class CourseSerializer(serializers.ModelSerializer):
      reviews = serializers.PrimaryKeyRelatedField(
          many=True,
          read_only=True,
      )
      average_rating = serializers.SerializerMethodField()

      class Meta:
          model = models.Course
          fields = (
              'id',
              'title',
              'url',
              'reviews',
              'average_rating',
          )

      # When working with `SerializerMethodField` to add custom data to the
      # serialized output, the method needs to follow a `get_field` pattern.
      # `obj` is the object that is being serialized.
      def get_average_rating(self, obj):
          # NOTE: This is probably not the best way to get average ratings,
          # as it will be taxing on your query time as the database continues
          # to grow. It would be best to add an `average_rating` field to the
          # model itself and store a value that is calculated and updated
          # each time a review is submitted using Django's `signals`.
          average = obj.reviews.aggregate(Avg('rating')).get('rating__avg')

          if average is None:
              return 0
          # Ensure you're always dealing 0.5 increments (e.g., 1.0, 2.5, etc.).
          return round(average * 2) / 2
  ```

## Django Authentication

### Authentication

#### Requiring Logins

- Django provides the [**LoginRequiredMixin**](https://docs.djangoproject.com/en/3.0/topics/auth/default/#django.contrib.auth.mixins.LoginRequiredMixin) for generic views that requires a user to be logged in to gain access to the view. According to the teacher: "Django provides decorators for marking a view as requiring a login, but decorators are 'iffy' with class-based views. So Django also provides mixins to use with your class-based views."

- Example:

  ```python
  # ./django-basics/django_auth/msg/posts/views.py

  from django.contrib.auth.mixins import LoginRequiredMixin
  from braces.views import SelectRelatedMixin

  # ...

  # `SelectedRelatedMixin` is from `django-braces`. It lets you perform
  # "select related" queries without having to change the queryset yourself.
  # You just need to use the `select_related` attribute.
  class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
      model = models.Post
      select_related = ("user", "community")
      success_url = reverse_lazy("posts:all")

      # ...
  ```

#### LoginView

- One method of using [**LoginView**](https://docs.djangoproject.com/en/3.0/topics/auth/default/#django.contrib.auth.views.LoginView) to authenticate and log in users via a form located on `/accounts/login/`:

  ```python
  # ./django-basics/django_auth/msg/accounts/views.py

  from django.contrib.auth import login
  from django.contrib.auth.forms import AuthenticationForm
  from django.urls import reverse_lazy
  from django.views import generic


  class LoginView(generic.FormView):
      # Ensure the user is authenticated before attemping a log in.
      form_class = AuthenticationForm
      # Redirect when the form view is complete.
      success_url = reverse_lazy('posts:all')
      template_name = 'accounts/login.html'

      def get_form(self, form_class=None):
          if form_class is None:
              form_class = self.get_form_class()
          # The default `form_class` just takes the second argument,
          # but the first argument in an `AuthenticationForm` must
          # be the request.
          return form_class(self.request, **self.get_form_kwargs())

      # Only login if the `AuthenticationForm` is valid.
      def form_valid(self, form):
          # `self.request` is used in creating the session and validating
          # that a request is coming from the user. The `form.get_user()`
          # method is a method provided by the `AuthenticationForm` which
          # returns the authenticated user object.
          login(self.request, form.get_user())
          return super().form_valid(form)
  ```

  ```python
  # ./django-basics/django_auth/msg/msg/urls.py

  # ...

  urlpatterns = [
      # ...
      path('accounts/', include('accounts.urls', namespace='accounts')),
      # ...
  ]
  ```

  ```python
  # ./django-basics/django_auth/msg/accounts/urls.py

  # ...

  urlpatterns = [
      path('login/', views.LoginView.as_view(), name='login')
  ]
  ```

  ```html
  # ./django-basics/django_auth/msg/accounts/templates/accounts/login.html

  {% extends "layout.html" %}
  {% load bootstrap3 %}

  {% block title_tag %}Login | {{ block.super }}{% endblock %}

  {% block body_content %}
  <div class="container">
    <h1>Login</h1>
    <form method="POST">
      {% csrf_token %}
      {% bootstrap_form form %}
      <input class="btn btn-default" type="submit" value="Login">
    </form>
  </div>
  {% endblock %}
  ```

- **HOWEVER:** There is a simpler way to perform the same login by relying upon `django.contrib.auth.urls` rather than `LoginView`:

  ```python
  # ./django-basics/django_auth/msg/msg/urls.py

  urlpatterns = [
      # ...
      # This first `accounts/` path should only contain URLs that
      # go beyond those provided by `django.contrib.auth.urls`. This
      # means `account.urls` should not contain a `login/` path, because
      # `django.contrib.auth.urls` already contains such a path.
      path('accounts/', include('accounts.urls', namespace='accounts')),
      # This path will only be executed if there are no matches
      # for any URLs in the `accounts` path above.
      path('accounts/', include('django.contrib.auth.urls')),
      # ...
  ]
  ```

  ```python
  # ./django-basics/django_auth/msg/msg/settings.py

  #...

  # By default, login forms using `django.contrib.auth.urls` redirect to
  # `accounts/profile/`. Use this variable to change the redirect URL.
  LOGIN_REDIRECT_URL = 'posts:all'
  ```

  ```html
  # ./django-basics/django_auth/msg/templates/registration/login.html

  <!-- This specific `registration/login.html` template on the project level must be used
    for the login form if you are using `django.contrib.auth.urls` to handle log ins. -->

  {% extends "layout.html" %}
  {% load bootstrap3 %}

  {% block title_tag %}Login | {{ block.super }}{% endblock %}

  {% block body_content %}
  <div class="container">
    <h1>Login</h1>
    <form method="POST">
      {% csrf_token %}
      {% bootstrap_form form %}
      <input class="btn btn-default" type="submit" value="Login">
    </form>
  </div>
  {% endblock %}
  ```

#### LogoutView and SignUpView

- Django's authentication views include a [**LogoutView**](https://docs.djangoproject.com/en/3.0/topics/auth/default/#django.contrib.auth.views.LogoutView), which renders as an admin "Logged out" template by default when a request is made to `accounts/logout/`. You can change this behavior to redirect to another view instead (e.g., the home page). Example:

  ```python
  # ./django-basics/django_auth/msg/accounts/views.py

  from django.contrib.auth import login, logout

  # ...

  class LogoutView(generic.RedirectView):
      # `RedirectView` requires a `url` attribute indicating the
      # URL that will be used for the redirect.
      url = reverse_lazy('home')

      def get(self, request, *args, **kwargs):
          logout(request)
          # Ensure the normal return proceeds after the log out.
          return super().get(request, *args, **kwargs)
  ```

  ```python
  # ./django-basics/django_auth/msg/accounts/urls.py

  # ...

  urlpatterns = [
      path('logout/', views.LogoutView.as_view(), name='logout')
  ]
  ```

- Creating a **Sign Up** view is often very customized to each site, so Django does not include a ready-made view for registering new users. You can use the [**UserCreationForm**](https://docs.djangoproject.com/en/3.0/topics/auth/default/#django.contrib.auth.forms.UserCreationForm) as one option for creating a new user. Example:

  ```python
  # ./django-basics/django_auth/msg/accounts/forms.py

  from django.contrib.auth.forms import UserCreationForm
  from django.contrib.auth.models import User


  class UserCreateForm(UserCreationForm):
      class Meta:
          fields = (
              'username',
              'email',
              'password1',
              'password2',
          )
          model = User

      # Override the default form labels.
      def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields['username'].label = 'Display name'
          # NOTE: The `email` field of Django's `User` model is optional.
          # If you need it to be required, this class will need
          # to be customized further.
          # Google: django usercreationform email
          self.fields['email'].label = 'Email address'
  ```

  ```python
  # ./django-basics/django_auth/msg/accounts/views.py

  from . import forms

  # ...

  class SignUpView(generic.CreateView):
      form_class = forms.UserCreateForm
      success_url = reverse_lazy('login')
      template_name = 'accounts/signup.html'
  ```

  ```html
  # ./django-basics/django_auth/msg/accounts/templates/accounts/signup.html

  {% extends "layout.html" %}
  {% load bootstrap3 %}

  {% block title_tag %}Sign Up | {{ block.super }}{% endblock %}

  {% block body_content %}
  <div class="container">
    <h1>Sign Up</h1>
    <form method="POST">
      {% csrf_token %}
      {% bootstrap_form form %}
      <input class="btn btn-default" type="submit" value="Sign Up">
    </form>
  </div>
  {% endblock %}

  ```

- You can enhance your user registration process with the [**django-registration**](https://django-registration.readthedocs.io/en/3.1/) package, which allows for user validation on sign up (i.e., the user must click a link that is sent to their email address in order to complete the registration process).

- Consider using [**django-allauth**](https://readthedocs.org/projects/django-allauth/) as an option for allowing third-party (social) account authentication.

- To automatically log a user in after completing the sign up process, consider the steps taken in [this thread](https://teamtreehouse.com/community/django-authentication-signupview-challenge-task-2-of-2-not-sure-if-i-am-on-the-right-path).

#### Resetting Passwords

- Django's default password reset process sends a link to the email address of a registered user. Once the user clicks that link, they will be presented with a form to enter a new password. While in development, you may use the [**file backend**](https://docs.djangoproject.com/en/3.0/topics/email/#email-backends) to write emails to a file rather than actually sending a real email:

  ```python
  # ./django-basics/django_auth/msg/msg/settings.py

  # Use the file-based email backend in development to simulate
  # an email being sent.
  EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
  EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')
  ```

- All of the registration templates use the admin template by default. However, the following templates can be customized by creating their respective HTML files under `${PROJECT}/templates/registration/`:
  - Initiate the reset process: `password_reset_form.html`
  - "Password reset sent" template: `password_reset_done.html`
  - Password reset form: `password_reset_confirm.html`
  - "Password reset complete" template: `password_reset_complete.html`

### Users and Authorization

#### User Diversity

- Read the [**documentation**](https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#extending-the-existing-user-model) regarding creating **custom user models**.

#### Custom User Manager

- Example of a custom user manager:

  ```python
  # ./django-basics/django_auth/msg/accounts/models.py

  from django.contrib.auth.models import (
      AbstractBaseUser, # All user models should be based on `AbstractBaseUser`.
      BaseUserManager, # Model manager that all user models use.
      PermissionsMixin, # Provides for user group permissions, etc.
  )
  from django.db import models
  from django.utils import timezone


  class UserManager(BaseUserManager):
      def create_user(self, email, username, display_name=None, password=None):
          if not email:
              raise ValueError('Users must have an email address')
          if not display_name:
              display_name = username

          # `self.model()` is whatever model the manager is attached to.
          user = self.model(
              # Ensure all emails throughout the app are formatted the same.
              email=self.normalize_email(email),
              username=username,
              display_name=display_name,
          )
          # Handle password encryption and validation checks.
          user.set_password(password)
          user.save()
          return user

      # This is the method that is called when you run:
      # $ python manage.py createsuperuser
      def create_superuser(self, email, username, display_name, password):
          user = self.create_user(
              email,
              username,
              display_name=display_name,
              password=password,
          )
          user.is_staff = True
          user.is_superuser = True
          user.save()
          return user
  ```

  - **SEE ALSO:** A [**full example**](https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#a-full-example) of an admin-compliant custom user app, and the documentation regarding [**managers**](https://docs.djangoproject.com/en/3.0/topics/db/managers/).

#### Custom User Model

- Example:

  ```python
  # ./django-basics/django_auth/msg/accounts/models.py

  # ...

  # NOTE: The teacher's reasoning for placing `PermissionsMixin` after
  # `AbstractBaseUser` (rather than vice versa) is because that's how he'd
  # always seen this example used in the documentation. The course was
  # originally created when Python was in version 1.9, so this pattern
  # may be obsolete.
  class User(AbstractBaseUser, PermissionsMixin):
      email = models.EmailField(unique=True)
      username = models.CharField(max_length=40, unique=True)
      display_name = models.CharField(max_length=140)
      bio = models.CharField(max_length=140, blank=True, default='')
      avatar = models.ImageField(blank=True, null=True)
      date_joined = models.DateTimeField(default=timezone.now)
      is_active = models.BooleanField(default=True)
      is_staff = models.BooleanField(default=False)

      # `objects` is the same attribute referenced in `User.objects.all()`
      objects = UserManager()

      # Specify what field will be used as the unique identifier for looking
      # someone up in the database.
      USERNAME_FIELD = 'email'
      # List of fields that will be prompted for when creating a user via
      # the `createsuperuser` management command.
      REQUIRED_FIELDS = ['display_name', 'username']

      def __str__(self):
          return '@{}'.format(self.username)

      def get_short_name(self):
          return self.display_name

      def get_long_name(self):
          return '{} (@{})'.format(self.display_name, self.username)
  ```

  ```python
  # ./django-basics/django_auth/msg/msg/settings.py

  # ...

  # Specify which model to use as the "active" user model for this project.
  AUTH_USER_MODEL = 'accounts.User'
  ```

  ```python
  # ./django-basics/django_auth/msg/accounts/forms.py

  # NOTE: You cannot use `django.conf import settings` for the `Meta` model.
  # `settings.AUTH_USER_MODEL` only returns a string, but you need an actual
  # model object. The `get_user_model` method makes that happen here, as it
  # always returns the "active" user model (which, in this case, will be the
  # `AUTH_USER_MODEL` defined in `settings.py`).
  from django.contrib.auth import get_user_model
  from django.contrib.auth.forms import UserCreationForm


  class UserCreateForm(UserCreationForm):
      class Meta:
          fields = ('username', 'email', 'password1', 'password2')
          model = get_user_model()

      def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields['username'].label = 'Display name'
          self.fields['email'].label = 'Email address'
  ```

  - **NOTE:** Throughout the project, ensure that you always include `from django.conf import settings` and use `settings.AUTH_USER_MODEL` when necessary to reference your custom model as a string (rather than importing `from django.contrib.auth.models import User` and using `User`). This applies when, e.g., setting a `ManyToManyField` relationship, setting a `ForeignKey`, etc. **HOWEVER**, this would not apply when, e.g., executing a `.objects.create()` query (in which case, you should use `get_user_model()`).

  - **WARNING:** Changing to a custom user model mid-project can lead to significant difficulties. Refer to the [documentation](https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#changing-to-a-custom-user-model-mid-project) and [this thread on Stack Overflow](https://stackoverflow.com/questions/44651760/django-db-migrations-exceptions-inconsistentmigrationhistory/49911140#49911140) for more details.

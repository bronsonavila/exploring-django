import os
from peewee import *

# Configure MySQL database connection.
db = MySQLDatabase('students',
                   user=os.environ['USER'],
                   password=os.environ['PASSWORD'], host='localhost')


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

# Generated by Django 3.0 on 2020-03-07 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_course_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='times_taken',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]

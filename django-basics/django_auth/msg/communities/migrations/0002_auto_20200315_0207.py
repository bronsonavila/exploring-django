# Generated by Django 3.0 on 2020-03-15 02:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='communitymember',
            options={'permissions': (('ban member', 'Can ban members'),)},
        ),
    ]
# Generated by Django 3.2.9 on 2021-11-08 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('levelupapi', '0003_auto_20211108_1919'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='',
            new_name='attendee',
        ),
    ]

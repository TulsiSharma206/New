# Generated by Django 3.1.1 on 2020-11-02 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0010_auto_20201102_1040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignmentstest',
            name='chapter',
        ),
    ]

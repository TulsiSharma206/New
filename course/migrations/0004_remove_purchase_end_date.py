# Generated by Django 3.1.1 on 2020-10-15 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_auto_20201012_1106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='end_date',
        ),
    ]

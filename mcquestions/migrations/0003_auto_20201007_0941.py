# Generated by Django 3.1.1 on 2020-10-07 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcquestions', '0002_studentpercentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentpercentage',
            name='percentag',
            field=models.CharField(max_length=255, verbose_name='percentage'),
        ),
    ]

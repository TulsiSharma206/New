# Generated by Django 3.1.1 on 2020-10-22 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_count_vtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='price',
            field=models.CharField(blank=True, max_length=127, null=True),
        ),
    ]

# Generated by Django 3.1.1 on 2020-10-15 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_remove_purchase_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='count',
            name='vtime',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

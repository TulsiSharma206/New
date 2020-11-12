# Generated by Django 3.1.1 on 2020-11-02 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0011_remove_assignmentstest_chapter'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mocktestpercentage',
            options={'verbose_name': 'MockTestPercentage', 'verbose_name_plural': 'MockTestPercentage'},
        ),
        migrations.AddField(
            model_name='assignmentspercentage',
            name='cours',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Assignmentchapter', to='course.course'),
        ),
        migrations.AddField(
            model_name='assignmentsprogress',
            name='cours',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Assignmentcourse', to='course.course'),
        ),
        migrations.AddField(
            model_name='mocktestpercentage',
            name='chapter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Mockchapter', to='course.chapter'),
        ),
        migrations.AddField(
            model_name='mocktestpercentage',
            name='cours',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='MockTest', to='course.course'),
        ),
        migrations.AddField(
            model_name='mocktestprogress',
            name='chapter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='MockTestsChapter', to='course.chapter'),
        ),
        migrations.AddField(
            model_name='mocktestprogress',
            name='cours',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='MockTestsCourse', to='course.course'),
        ),
    ]
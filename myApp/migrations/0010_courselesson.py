# Generated by Django 5.0.7 on 2024-08-29 16:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0009_course_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseLesson',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField(blank=True, null=True)),
                ('resource', models.FileField(blank=True, null=True, upload_to='lessons/videos/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='myApp.course')),
            ],
        ),
    ]

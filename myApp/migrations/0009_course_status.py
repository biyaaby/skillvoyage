# Generated by Django 5.0.7 on 2024-08-29 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0008_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('archived', 'Archived'), ('pending approval', 'Pending Approval'), ('rejected', 'Rejected')], default='draft', max_length=20),
        ),
    ]

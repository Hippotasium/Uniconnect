# Generated by Django 5.1.7 on 2025-04-14 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_job_poster'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

# Generated by Django 5.1.7 on 2025-04-16 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_delete_chatmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='student_approved',
            field=models.BooleanField(default=False),
        ),
    ]

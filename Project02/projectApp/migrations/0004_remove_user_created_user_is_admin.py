# Generated by Django 5.1.2 on 2024-10-08 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectApp', '0003_remove_user_confirm_password_alter_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='created',
        ),
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]

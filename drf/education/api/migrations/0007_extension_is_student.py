# Generated by Django 3.2.16 on 2023-04-19 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_extension_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='extension',
            name='is_student',
            field=models.BooleanField(default=False),
        ),
    ]

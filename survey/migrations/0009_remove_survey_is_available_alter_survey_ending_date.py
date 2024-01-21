# Generated by Django 5.0.1 on 2024-01-21 17:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0008_alter_survey_ending_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='is_available',
        ),
        migrations.AlterField(
            model_name='survey',
            name='ending_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 18, 17, 58, 52, 625135, tzinfo=datetime.timezone.utc)),
        ),
    ]

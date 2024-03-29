# Generated by Django 5.0.1 on 2024-01-22 18:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0009_remove_survey_is_available_alter_survey_ending_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='ending_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 19, 18, 5, 49, 295427, tzinfo=datetime.timezone.utc)),
        ),
    ]

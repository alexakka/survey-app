# Generated by Django 5.0.1 on 2024-01-21 17:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_survey_number_of_respondent_alter_survey_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 18, 17, 27, 39, 415138, tzinfo=datetime.timezone.utc)),
        ),
    ]
# Generated by Django 5.0.1 on 2024-01-27 17:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0013_delete_respondent_rename_name_survey_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='ending_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 24, 17, 22, 34, 607799, tzinfo=datetime.timezone.utc)),
        ),
    ]
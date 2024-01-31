import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from survey.models import Survey, Question, Answer, Response, SpentTime
from datetime import timedelta
from faker import Faker
from random import randint




User = get_user_model()
fake = Faker()


def create_user():
    email = fake.email()
    password = fake.password()
    first_name = fake.first_name()
    last_name = fake.last_name()
    sex = fake.random_element(elements=('M', 'F'))  # Randomly choose 'M' or 'F'

    # Generate a random birthday between 18 and 65 years ago
    birthday_start = timezone.now() - timedelta(days=65*365)  # 65 years ago
    birthday_end = timezone.now() - timedelta(days=18*365)  # 18 years ago
    birthday = fake.date_time_between_dates(birthday_start, birthday_end).date()

    user = User.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        sex=sex,  # Assigning the sex field
        birthday=birthday  # Assigning the birthday field
    )
    return user


def get_survey(survey_id):
    try:
        survey = Survey.objects.get(id=survey_id)
        return survey
    except Survey.DoesNotExist:
        print(f"Survey with ID {survey_id} does not exist.")
        return None


def complete_survey(user, survey):
    questions = survey.question_set.all()
    spent_time_seconds = randint(30, 180)  # Random time between 30 seconds and 3 minutes
    start_time = timezone.now()  # Record the start time
    end_time = start_time + timedelta(seconds=spent_time_seconds)

    for question in questions:
        answers = question.answer_set.all()
        chosen_answer = fake.random_element(answers)

        Response.objects.create(
            survey=survey,
            question=question,
            answer=chosen_answer,
            respondent=user
        )

    spent_time = SpentTime.objects.create(
        survey=survey,
        start_time=start_time.time(),
        end_time=end_time.time(),
        respondent=user
    )


def main():
    print('SCRIPT STARTED')
    survey_id = 16
    survey = get_survey(survey_id)

    if survey:
        for _ in range(50):
            user = create_user()
            complete_survey(user, survey)
    else:
        print("Survey could not be found.")

    print('SCRIPT COMPLETED')


if __name__ == "__main__":
    main()

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from survey.models import Survey, Question, Answer, Response
from faker import Faker



User = get_user_model()
fake = Faker()


def create_user():
    email = fake.email()
    password = fake.password()
    first_name = fake.first_name()
    last_name = fake.last_name()

    user = User.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
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

    for question in questions:
        answers = question.answer_set.all()
        chosen_answer = fake.random_element(answers)

        Response.objects.create(
                survey=survey,
                question=question,
                answer=chosen_answer,
                respondent=user
            )


def main():
    print('SCRIPT STARTED')
    survey_id = 16
    survey = get_survey(survey_id)

    if survey:
        for _ in range(5):
            user = create_user()
            complete_survey(user, survey)
    else:
        print("Survey could not be found. Exiting.")

    print('SCRIPT COMPLETED')


if __name__ == "__main__":
    main()
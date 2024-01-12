from django.db import models
from django.utils import timezone

from user.models import User


class Survey(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=1024)
    creating_date = models.DateTimeField(default=timezone.now)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=28))
    is_available = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        verbose_name = 'Survey'
        verbose_name_plural = 'Surveys'


    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.CharField(max_length=255)
    is_mandatory = models.BooleanField(default=True)

    survey = models.ForeignKey('Survey', on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Answer(models.Model):
    value = models.CharField(max_length=255)

    question = models.ForeignKey('Question', on_delete=models.CASCADE)

    def __str__(self):
        return self.value


class Respondent(models.Model):
    SEXES = {
        "M": "Male",
        "F": "Female",
    }

    age = models.IntegerField(blank=False)
    sex = models.CharField(max_length=1, choices=SEXES)


class Response(models.Model):
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    respondent = models.ForeignKey('Respondent', on_delete=models.CASCADE)


# class SurveyResponse(models.Model):
#     pass



# class QuestionOrder(models.Model):
#     pass

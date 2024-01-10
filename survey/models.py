from django.db import models
from django.utils import timezone

from user.models import User


class Survey(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=1024)
    creating_date = models.DateTimeField(default=timezone.now)
    starting_at = models.DateTimeField(default=timezone.now)
    ending_at = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=28))
    is_available = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        verbose_name = 'Survey'
        verbose_name_plural = 'Surveys'


    def __str__(self):
        return self.name



# class Question(models.Model):
#     text = models.CharField(max_length=255)
#     survey = models.ForeignKey('Survey', on_delete=models.CASCADE)


# class Answer(models.Model):
#     text = models.CharField(max_length=255)
#     question = models.ForeignKey('Question', on_delete=models.CASCADE)


# class Response(models.Model):
#     pass


# class QuestionOrder(models.Model):
#     pass


# class Respondent(models.Model):
#     pass


# class SurveyResponse(models.Model):
#     pass

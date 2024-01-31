from django.db import models
from django.utils import timezone
from django.utils.text import slugify
import datetime

from user.models import User


class Survey(models.Model):
    title = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=1024)
    slug = models.SlugField(unique=True, blank=True)
    number_of_responses = models.IntegerField(default=0)
    creating_date = models.DateTimeField(auto_now_add=True)
    starting_date = models.DateTimeField(default=timezone.now)
    ending_date = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=28))
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Survey'
        verbose_name_plural = 'Surveys'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def is_available(self):
        if timezone.now > self.ending_date:
            return False
        return True

    def __str__(self):
        return self.title


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


class Response(models.Model):
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    respondent = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer.value


class SpentTime(models.Model):
    start_time = models.TimeField(default=datetime.time)
    end_time = models.TimeField(default=datetime.time)  # Change this line
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE)
    respondent = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'SpentTime'
        verbose_name_plural = 'SpentTime'

    def get_spent_time(self):
        start_datetime = datetime.datetime.combine(datetime.date.today(), self.start_time)
        end_datetime = datetime.datetime.combine(datetime.date.today(), self.end_time)

        return end_datetime - start_datetime

    def __str__(self):
        return f"{self.start_time} | {self.survey.title} | {self.get_spent_time()} | {self.respondent.get_full_name()}"


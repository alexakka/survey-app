from django.shortcuts import render
from django.utils import timezone
from survey.models import Survey


def index(request):
    surveys = Survey.objects.all().filter(ending_date__gt=timezone.now())

    return render(request, 'index.html', {'surveys': surveys})

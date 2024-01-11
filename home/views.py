from django.shortcuts import render
from survey.models import Survey


def index(request):
    surveys = Survey.objects.all()

    # You can add additional logic here if needed

    # Render the survey details using a template
    return render(request, 'index.html', {'surveys': surveys})

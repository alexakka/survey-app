from django.views.generic import ListView
from django.utils import timezone
from survey.models import Survey


class IndexView(ListView):
    model = Survey
    template_name = 'index.html'
    context_object_name = 'surveys'

    def get_queryset(self):
        return Survey.objects.filter(ending_date__gt=timezone.now())

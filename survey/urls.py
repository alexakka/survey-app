from django.urls import path
from .views import survey_detail

urlpatterns = [
    # Other URL patterns
    path('survey/<int:survey_id>/', survey_detail, name='survey_detail'),
]

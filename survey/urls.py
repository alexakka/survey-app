from django.urls import path
from . import views


urlpatterns = [
    path('survey/<int:survey_id>/', views.survey_detail, name='survey_detail'),
    path('create_survey/', views.create_survey, name='create_survey'),
]

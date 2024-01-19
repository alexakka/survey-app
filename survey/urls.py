from django.urls import path
from . import views


urlpatterns = [
    path('survey/<int:survey_id>/', views.survey_detail, name='survey_detail'),
    path('create_survey/', views.create_survey, name='create_survey'),
    path('submit_response/<int:survey_id>/', views.submit_response, name='submit_response'),
    path('responses/<int:survey_id>', views.show_all_responses, name="responses")
]

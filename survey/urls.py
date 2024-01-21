from django.urls import path
from . import views


urlpatterns = [
    path('<int:survey_id>/', views.survey_detail, name='survey_detail'),
    path('create_survey/', views.create_survey, name='create_survey'),
    path('submit_response/<int:survey_id>/', views.submit_response, name='submit_response'),
    path('<int:survey_id>/complete_survey/', views.complete_survey, name='complete_survey'),
    path('responses/<int:survey_id>', views.show_all_responses, name="responses"),
    path('profile', views.profile, name='profile'),
    path('responses/<int:survey_id>/<int:respondent_id>/', views.respondent_response, name='respondent_response')
]

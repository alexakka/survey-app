from django.urls import path
from . import views


urlpatterns = [
    # surveys
    path('create_survey/', views.create_survey, name='create_survey'),
    path('edit_survey/<slug:survey_slug>/', views.edit_survey, name='edit_survey'),
    path('<slug:survey_slug>/', views.survey_detail, name='survey_detail'),

    # completing survey
    path('<slug:survey_slug>/complete_survey/', views.complete_survey, name='complete_survey'),
    path('submit_response/<slug:survey_slug>/', views.submit_response, name='submit_response'),

    # responses
    path('responses/<slug:survey_slug>/', views.show_all_responses, name="responses"),
    path('responses/<slug:survey_slug>/<int:respondent_id>/', views.respondent_response, name='respondent_response'),

    # export results
    path('<slug:survey_slug>/export-responses-csv/', views.export_responses_csv, name='export_responses_csv'),
]

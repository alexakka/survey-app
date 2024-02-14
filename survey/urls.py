from django.urls import path
from . import views


urlpatterns = [
    # surveys
    path('create_survey/', views.CreateSurveyView.as_view(), name='create_survey'),
    path('edit_survey/<slug:survey_slug>/', views.EditSurveView.as_view(), name='edit_survey'),
    path('<slug:survey_slug>/', views.SurveyDetailView.as_view(), name='survey_detail'),


    # completing survey
    path('<slug:survey_slug>/pass_survey/', views.PassSurveyView.as_view(), name='pass_survey'),
    path('submit_response/<slug:survey_slug>/', views.SubmitSurveyView.as_view(), name='submit_response'),

    # responses
    path('responses/<slug:survey_slug>/', views.ShowAllResponsesView.as_view(), name="responses"),
    path('responses/<slug:survey_slug>/<int:respondent_id>/', views.respondent_response, name='respondent_response'),

    # export results
    path('<slug:survey_slug>/export-responses-csv/', views.export_responses_csv, name='export_responses_csv'),

    path('chart_data/<slug:survey_slug>', views.chart_data, name='chart_data'),
]

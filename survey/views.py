import csv
import datetime
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView

from .models import Survey, Question, Answer, Response, SpentTime


class CreateSurveyView(View):
    def get(self, request):
        return render(request, 'survey/create_survey.html')

    def post(self, request):
        survey = Survey.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            author=request.user
        )

        question_texts = request.POST.getlist('question_text[]')
        answer_texts = request.POST.getlist('answer_text[]')

        j = 0
        for i in range(len(question_texts)):
                question = Question.objects.create(text=question_texts[i], survey=survey)

                # Assuming each question has the same number of answers
                for answer_text in answer_texts[j:j + len(answer_texts) // len(question_texts)]:
                    Answer.objects.create(value=answer_text, question=question)

                j = j + len(answer_texts) // len(question_texts)


        return redirect('index')

class EditSurveView(View):
    def get(self, request, survey_slug):
        survey = get_object_or_404(Survey, slug=survey_slug)
        return render(request, 'survey/edit_survey.html', {'survey': survey})

    def post(self, request, survey_slug):
        survey = get_object_or_404(Survey, slug=survey_slug)

        survey.title = request.POST['title']
        survey.description = request.POST['description']

        question_texts = request.POST.getlist('question_text[]')
        answer_texts = request.POST.getlist('answer_text[]')
        print(question_texts)
        j = 0
        for question, text in zip(survey.question_set.all(), question_texts):
            question.text = text

            for answer, value in zip(question.answer_set.all(), answer_texts[j:j + len(answer_texts) // len(question_texts)]):
                answer.value = value
                answer.save()

            question.save()
            j = j + len(answer_texts) // len(question_texts)

        survey.save()
        return redirect('profile')

class SurveyDetailView(View):
    def get(self, request, survey_slug):
        survey = get_object_or_404(Survey, slug=survey_slug)
        is_author = request.user == survey.author
        return render(request, 'survey/survey_detail.html', {'survey': survey, 'is_author': is_author})

class PassSurveyView(View):
    def get(self, request, survey_slug):
        survey = get_object_or_404(Survey, slug=survey_slug)

        respondent = Response.objects.filter(survey=survey, respondent=request.user)

        # check if user already complete a survey
        if respondent.exists():
            # re-initialising the storage to clear it
            request._messages = messages.storage.default_storage(request)

            messages.error(request, "You have already completed the survey!")
            return redirect(reverse('survey_detail', args=[survey_slug]))

        request.session['start_time'] = datetime.datetime.now().strftime('%H:%M:%S')
        return render(request, 'survey/complete_survey.html', {'survey': survey})

class SubmitSurveyView(View):
    def get(self, request, survey_slug):
        return redirect('pass_survey', survey_slug=survey_slug)

    def post(self, request, survey_slug):
        survey = get_object_or_404(Survey, slug=survey_slug)

        # adding one respondent to field
        survey.number_of_responses += 1
        survey.save()

        SpentTime.objects.create(
            start_time=request.session.get('start_time'),
            end_time=datetime.datetime.now().strftime('%H:%M:%S'),
            survey=Survey.objects.get(slug=survey_slug),
            respondent=request.user
        )

        for question in survey.question_set.all():
            answer_id = request.POST.get(f'question_{question.id}')
            answer = get_object_or_404(Answer, pk=answer_id)

        Response.objects.create(
                survey=survey,
                question=question,
                answer=answer,
                respondent=request.user
                )

        return redirect('index')

class ShowAllResponsesView(ListView):
    model = Response
    template_name = "survey/responses.html"
    context_object_name = "responses"

    def get_queryset(self):
        survey_slug = self.kwargs.get('survey_slug')
        survey = get_object_or_404(Survey, slug=survey_slug)
        responses = Response.objects.filter(survey=survey).distinct("respondent")
        return responses



def respondent_response(request, survey_slug, respondent_id):
    survey = get_object_or_404(Survey, slug=survey_slug)

    responses = Response.objects.all().filter(survey=survey, respondent=respondent_id)
    return render(request, "survey/respondent_response.html", {"responses": responses})





@login_required
def export_responses_csv(request, survey_slug):
    responses = Response.objects.filter(survey__slug=survey_slug).order_by('answer')

    # Check the survey author
    if request.user == responses[0].survey.author:
        filename = f"{survey_slug}-responses.csv"

        # Create the HttpResponse object with CSV content.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Create CSV writer
        writer = csv.writer(response)
        questions = Question.objects.filter(survey__slug=survey_slug)

        writer.writerow(write_columns(len(questions)))

        respondents = Response.objects.values_list('respondent', flat=True).distinct()

        for respondent in respondents:
            resp = Response.objects.filter(respondent=respondent)

            spent_time = get_object_or_404(SpentTime, survey__slug=survey_slug, respondent=respondent)
            row = [
                resp[0].respondent.first_name + ' ' + resp[0].respondent.last_name,
                resp[0].respondent.get_age(),
                resp[0].respondent.birthday,
                resp[0].respondent.sex,
                spent_time.start_time,
                spent_time.end_time,
                spent_time.get_spent_time(),
                ]
            for r in resp:
                row.append(r.question)
                row.append(r.answer)

            writer.writerow(row)

        return response

    return HttpResponse('You not the owner of the survey')


def write_columns(num_of_questions):
    columns = ['Respondent', 'Age', 'Birthday', 'Sex', 'Start_time', 'End time', 'Spent_time']

    for i in range(num_of_questions):
        columns.append(f'Question{i + 1}')
        columns.append(f'Answer{i + 1}')
        i += 1

    return columns


def chart_data(request, survey_slug):
    try:
        survey = Survey.objects.get(slug=survey_slug)
        questions = survey.question_set.all()
        chart_data = []

        for question in questions:
            total_responses = Response.objects.filter(question=question).count()
            answers = question.answer_set.all()
            answer_data = {}

            for answer in answers:
                response_count = Response.objects.filter(question=question, answer=answer).count()
                if total_responses > 0:
                    answer_percentage = (response_count / total_responses) * 100
                else:
                    answer_percentage = 0
                answer_data[answer.value] = round(answer_percentage, 2)

            chart_data.append({
                'question': question.text,
                'answers': answer_data
            })

        return JsonResponse(chart_data, safe=False)

    except Survey.DoesNotExist:
        return JsonResponse({'error': 'Survey does not exist'}, status=404)


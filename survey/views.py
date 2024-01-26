import csv
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from .models import Survey, Question, Answer, Response


@login_required
def create_survey(request):
    if request.method == 'POST':

        survey = Survey.objects.create(
            name=request.POST['name'],
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

    return render(request, 'survey/create_survey.html')


@login_required
def edit_survey(request, survey_slug):
    survey = get_object_or_404(Survey, slug=survey_slug)

    if request.method != 'POST':
        return render(request, 'survey/edit_survey.html', {'survey': survey})
    else:
        survey.name = request.POST['name']
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


def survey_detail(request, survey_slug):
    survey = get_object_or_404(Survey, slug=survey_slug)
    is_author = request.user == survey.author
    return render(request, 'survey/survey_detail.html', {'survey': survey, 'is_author': is_author})


def complete_survey(request, survey_slug):
    survey = get_object_or_404(Survey, slug=survey_slug)

    respondent = Response.objects.filter(survey=survey, respondent=request.user)

    # check if user already complete a survey
    if respondent.exists():
        # re-initialising the storage to clear it
        request._messages = messages.storage.default_storage(request)

        messages.error(request, "You already complete the survey!")
        return redirect(reverse('survey_detail', args=[survey_slug]))

    return render(request, 'survey/complete_survey.html', {'survey': survey})



def show_all_responses(request, survey_slug):
    survey = get_object_or_404(Survey, slug=survey_slug)

    all_responses = Response.objects.filter(survey=survey).distinct("respondent")
    return render(request, "survey/responses.html", {"responses": all_responses})


def respondent_response(request, survey_slug, respondent_id):
    survey = get_object_or_404(Survey, slug=survey_slug)

    responses = Response.objects.all().filter(survey=survey, respondent=respondent_id)
    return render(request, "survey/respondent_response.html", {"responses": responses})



def submit_response(request, survey_slug):
    if request.method == 'POST':

        survey = get_object_or_404(Survey, slug=survey_slug)
        # adding one respondent to field
        survey.number_of_responses += 1
        survey.save()

        for question in survey.question_set.all():
            answer_id = request.POST.get(f'question_{question.id}')
            answer = get_object_or_404(Answer, pk=answer_id)

            response = Response(
                survey=survey,
                question=question,
                answer=answer,
                respondent=request.user
                )
            response.save()

        return redirect('index')

    return redirect('complete_survey', survey_slug=survey_slug)


@login_required
def export_responses_csv(request, survey_slug):
    responses = Response.objects.filter(survey__slug=survey_slug).order_by('answer')

    # Check the survey author
    if request.user == responses[0].survey.author:
        filename = f"{survey_slug}_responses.csv"

        # Create the HttpResponse object with CSV content.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Create CSV writer
        writer = csv.writer(response)

        # Write header row
        writer.writerow(['Survey', 'Question', 'Answer', 'Respondent'])

        # Write data rows
        for response_obj in responses:
            writer.writerow(
                [response_obj.survey.name,
                response_obj.question.text,
                response_obj.answer.value,
                response_obj.respondent.first_name + ' ' + response_obj.respondent.last_name]
                )

        return response

    return HttpResponse('You not the owner of the survey')

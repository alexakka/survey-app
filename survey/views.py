from django.shortcuts import render, get_object_or_404, redirect
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


def survey_detail(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    is_author = request.user == survey.author
    return render(request, 'survey/survey_detail.html', {'survey': survey, 'is_author': is_author})



def complete_survey(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)

    respondent = Response.objects.filter(survey=survey, respondent=request.user)

    # check if user already complete a survey
    if respondent.exists():
        # re-initialising the storage to clear it
        request._messages = messages.storage.default_storage(request)

        messages.error(request, "You already complete the survey!")
        return redirect(reverse('survey_detail', args=[survey_id]))

    return render(request, 'survey/complete_survey.html', {'survey': survey})


def respondent_response(request, survey_id, respondent_id):
    responses = Response.objects.all().filter(survey=survey_id, respondent=respondent_id)
    return render(request, "survey/respondent_response.html", {"responses": responses})


def show_all_responses(request, survey_id):
    # all_responses = Response.objects.filter(survey=survey_id)
    # all_responses.group_by = ['respondent']
    all_responses = Response.objects.filter(survey=survey_id).distinct("respondent")
    return render(request, "survey/responses.html", {"responses": all_responses})


def submit_response(request, survey_id):
    if request.method == 'POST':

        survey = get_object_or_404(Survey, pk=survey_id)
        # adding one respondent to field
        survey.number_of_responses += 1
        survey.save()

        for question in survey.question_set.all():
            answer_id = request.POST.get(f'question_{question.id}')
            answer = get_object_or_404(Answer, pk=answer_id)

            response = Response(survey=survey, question=question, answer=answer, respondent=request.user)
            response.save()

        return redirect('index')

    return redirect('complete_survey', survey_id=survey_id)



@login_required
def profile(request):
    user = request.user
    return render(request, 'survey/profile.html', {'user': user})

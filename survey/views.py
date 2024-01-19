from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
    return render(request, 'survey/survey_detail.html', {'survey': survey})


def show_all_responses(request, survey_id):
    all_responses = Response.objects.filter(survey=survey_id)
    all_responses.group_by = ['respondent']
    return render(request, "survey/responses.html", {"responses": all_responses})


def submit_response(request, survey_id):
    if request.method == 'POST':
        survey = get_object_or_404(Survey, pk=survey_id)

        for question in survey.question_set.all():
            answer_id = request.POST.get(f'question_{question.id}')
            answer = get_object_or_404(Answer, pk=answer_id)

            response = Response(survey=survey, question=question, answer=answer, respondent=request.user)
            response.save()

        return redirect('index')

    return redirect('survey_detail', survey_id=survey_id)


from django.shortcuts import render
from django.http import HttpResponse

from.models import Question

# Create your views here.

def index(request):
    lattest_question_list = Question.objects.all() 
    return render(request, 'polls/index.html', {
        'lattest_question_list': lattest_question_list,
    })


def detail(request, question_id):
    return HttpResponse(f'You\'re watching the question number {question_id}')


def results(request, question_id):
    return HttpResponse(f'You\'re watching the results from the question number {question_id}')


def vote(request, question_id):
    return HttpResponse(f'You\'re voting the question number {question_id}')

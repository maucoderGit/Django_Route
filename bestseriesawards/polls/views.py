from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from.models import Question

# Create your views here.

def index(request: HttpResponse):
    """
    Index Function view.

    Get all polls

    Parameters:
    - Request: Request

    Returns:
    - Render response with:
        - HttpResponse.
        - Url
        - Questions: Dict[Object]
    """
    lattest_question_list = Question.objects.all() 
    return render(request, 'polls/index.html', {
        'lattest_question_list': lattest_question_list,
    })


def detail(request: HttpResponse, question_id: int):
    """
    Polls details

    Get a question by id

    Args:
    - request: Request
    - question_id: int

    Returns:
    - - Render response with:
        - Request.
        - Url
        - Questions: Dict[id]
    """
    question: Question | None = get_object_or_404(Question, pk=question_id)
    
    return render(request,'polls/detail.html', context={
        'question': question
    })


def results(request: HttpResponse, question_id):
    return HttpResponse(f'You\'re watching the results from the question number {question_id}')


def vote(request: HttpResponse, question_id):
    return HttpResponse(f'You\'re voting the question number {question_id}')

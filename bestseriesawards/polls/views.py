from typing import Optional
from django import forms
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from.models import Choice, Question

# Create your views here.

#def index(request: HttpResponse):
#    """
#    Index Function view.
#
#    Get all polls
#
#    Parameters:
#    - Request: Request
#
#    Returns:
#    - Render response with:
#        - HttpResponse.
#        - Url
#        - Questions: Dict[Object]
#    """
#    lattest_question_list = Question.objects.all() 
#    return render(request, 'polls/index.html', {
#        'lattest_question_list': lattest_question_list,
#    })


#def detail(request: HttpResponse, question_id: int):
#    """
#    Polls details
#
#    Get a question by id
#
#    Args:
#    - request: Request
#    - question_id: int
#
#    Returns:
#    - Render response with:
#       - Request.
#        - Url
#        - Questions: Dict[id]
#    """
#    question: Question | None = get_object_or_404(Question, pk=question_id)
#    
#    return render(request,'polls/detail.html', context={
#        'question': question
#   })


#def results(request: HttpResponse, question_id: int):
#    """
#    Results
#
#    Get questions results
#
#    Args:
#    - request: HttpResponse
#    - question_id: int
#
#    Returns:
#    - httpResponse:
#        - redirect: polls/results.html
#        - context: dict[str: Question]
#    """
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, 'polls/results.html', context={
#        'question': question
#    })

class IndexView(generic.ListView):
    """
    Class IndexView

    Attributes:
    - templeate_name: str = is a path to the template name
    - context_object_name: str = context paramter
    """

    template_name: str = 'polls/index.html'
    context_object_name: str = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published question"""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model: Question = Question
    template_name: str = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any question that aren't published yet
        """
        query_set = Question.objects.filter(pub_date__lte=timezone.now())
        
        for question in query_set:
            if len(question.choice_set.all()) <= 1:
                raise forms.ValidationError('At least one choice required.')
        return query_set


class ResultView(DetailView):
    template_name: str = 'polls/results.html'


def vote(request: HttpResponse, question_id: int):
    """
    Vote

    Vote for a choice

    Args:
    - request: HttpResponse
    - question_id: int

    Returns:
    - if there's a id, redirect to results view.
    - else render again the detail view with an error message.
    """
    # First we get a question using the id getted in the form
    question = get_object_or_404(Question, pk=question_id)

    # If there's a id we redirect to results view, else, we render again the
    # detail view with the error message.

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", context={
            'question': question,
            'error_message': 'You must select an option'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

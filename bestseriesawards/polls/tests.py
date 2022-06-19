import datetime
from urllib import response
from django import forms
from django.forms import ValidationError
from django.urls import reverse
from django.utils import timezone
from django.test import TestCase

from polls.models import Choice, Question

# Models

def create_question(question_text: str, days: float) -> Question:
    """
    Create a question with the given 'question_text', and published the given number of days offset to now (negative for questions published in the past, positive for questions that have yet to be published)
    
    Returns a Question model
    """
    time = timezone.now() + datetime.timedelta(days=days)
    question = Question(question_text=question_text, pub_date=time)

    # Create choices
    choice1 = Choice(question=question, choice_text="Choice 1", votes=0)
    choice2 = Choice(question=question, choice_text="Choice 2", votes=0)
    # Save questions
    question.save(choices=(choice1, choice2))
    
    return question

class QuestionModelTests(TestCase):

    def test_question_without_choices_not_must_be_possible(self):
        """
        If a question object is created must have almost one(1) choice or more.
        """
        question = Question(question_text="Question without choices", pub_date=timezone.now())
        
        # This function validate if a error is raised when we save a question without choices
        with self.assertRaises(forms.ValidationError):
            question.save()

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently returns False for a question whose pub_date is greatter
        """
        question = create_question(question_text='past question', days=-2)
        self.assertIs(question.was_published_recently(), False)

    def test_was_published_recently_with_recently_question(self):
        """
        Was_published_recently returns True for a question whose pub_date is less than 24 hours
        """
        question = create_question(question_text='past question', days=0)
        self.assertIs(question.was_published_recently(), True)
    
    def test_was_published_recently_with_future_question(self):
        """
        Was_publised_recently returns False for a question whose pub_date is in the future
        """
        question = create_question('future question', days=30)
        self.assertIs(question.was_published_recently(), False)

# Views

class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """
        If there're no any question, an appropiate message is deployed
        """
        response = self.client.get(reverse('polls:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_question_with_future_pub_date(self):
        """
        Validate if there're no any questions whose pub_date is in the future 
        """
        past_question = create_question('today', 0)
        future_question = create_question('future', days=10)

        response = self.client.get(reverse('polls:index'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [past_question])
     
    def test_past_question(self):
        """
        Question with a pub_date in the past are displayed on the index page
        """
        question = create_question('past', days=-10)
        response = self.client.get(reverse('polls:index'))
        
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])
    
    def test_future_question_and_past_question(self):
        """
        Even if both past and future question exist, only past question are displayed
        """
        past_question= create_question(question_text='past_question', days=-10)
        future_question = create_question(question_text='future_question', days=30)
        
        # The response must be created after the Question
        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(response.context['latest_question_list'], [past_question])
    
    def test_two_future_questions(self):
        """
        Even if two future question exist, any future question must not be displayed
        """
        future_question1 = create_question('first future', 10)
        future_question2 = create_question('second future', 16)

        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_two_past_questions(self):
        """
        The question index page must display mustiple question.
        """
        past1_question = create_question(question_text='past_question', days=-30)
        past2_question = create_question(question_text='future_question', days=-10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [past2_question, past1_question]
        )

class QuestionDetailViewTests(TestCase):
    
    def test_future_question(self):
        """
        The detail view of a question with a "pub_date" in the future returns a 404 error not found
        """
        future_question = create_question(question_text='future', days=20)
        url = reverse('polls:detail', args=(future_question.pk,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a "pub_date" in the past display a question's text
        """
        past_question = create_question(question_text='past', days=-20)
        url = reverse('polls:detail', args=(past_question.pk,))
        response = self.client.get(url)

        self.assertContains(response, past_question.question_text)

class QuestionResultsViewTests(TestCase):
    
    def test_results_question_no_questions(self):
        """
        If the question doesn't exist the view must response with a 404 status code error
        """
        url = reverse('polls:results', kwargs={'pk':1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_results_question_future_pub_date(self):
        """
        If the question results has a 'pub_date' in the future must response with a 404 status code
        """
        question = create_question('future quest', 30)
        url = reverse('polls:results', args=(question.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_results_question_with_past_pub_date(self):
        """
        if the question's "pub_date" was published in the past, must display it
        """
        question = create_question('past_question', days=-15)
        url = reverse('polls:results', args=(question.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)

    def test_results_view_must_display_all_choices(self):
        """
        The question result view must display all the choices of a question and the question text
        """
        question = create_question('question', days=-15)
        url = reverse('polls:results', args=(question.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)
        
        for choice in question.choice_set.all():
            self.assertContains(
                response,
                f'{choice.choice_text} -- {choice.votes} votes'
            )

import datetime
from django.db import models
from django import forms
from django.utils import timezone

# models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date_published")

    def __str__(self) -> str:
        return self.question_text

    def save(self, *args, **kwargs):
        choices = kwargs.get('choices')
        if choices and len(choices) >= 2:
            kwargs.pop('choices')
            super().save(*args, **kwargs)     
            for choice in choices:
                choice.question = self
                choice.save()
        else:
            raise forms.ValidationError("Must have 2 or more choices")

    def was_published_recently(self) -> bool:
        """
        Validate if a question was published recently.

        Returns True or False
        """
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.choice_text

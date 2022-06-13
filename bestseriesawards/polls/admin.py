from django.contrib import admin
from .models import Choice, Question

class ChoicesInline(admin.StackedInline):
    model = Choice
    can_delete = False
    verbose_name_plural = 'choices'

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = (ChoicesInline,)
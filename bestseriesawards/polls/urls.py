from django.urls import path
from . import views

urlpatterns = [
    # Example: /polls/
    path('', views.index, name='index'),
    # Example: /polls/5/
    path('<int:question_id>/', views.detail, name='question'),
    # Example: /polls/5/results
    path('<int:question_id>/results/', views.results, name='question'),
    # Example: /polls/5/results
    path('<int:question_id>/vote/', views.vote, name='question')
]
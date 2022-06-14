from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    # Example: /polls/
    path('', views.index, name='index'),
    # Example: /polls/5/
    path('<int:question_id>/detail/noimportaloquehagasaldrabien', views.detail, name='detail'),
    # Example: /polls/5/results
    path('<int:question_id>/results/', views.results, name='results'),
    # Example: /polls/5/results
    path('<int:question_id>/vote/', views.vote, name='vote')
]
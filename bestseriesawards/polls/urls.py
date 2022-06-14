from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    # Example: /polls/
    path('', views.IndexView.as_view(), name='index'),
    # Example: /polls/5/
    path('<int:pk>/detail/', views.DetailView.as_view(), name='detail'),
    # Example: /polls/5/results
    path('<int:pk>/results/', views.ResultView.as_view(), name='results'),
    # Example: /polls/5/results
    path('<int:question_id>/vote/', views.vote, name='vote')
]
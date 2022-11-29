from django.urls import path
from . import views
from .views import QuestionListView, QuestionDetailView, QuestionCreateView, QuestionUpdateView, QuestionDeleteView

urlpatterns = [
    path('', QuestionListView.as_view(), name='forum-index'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='forum-question-detail'),
    path('questions/new/', QuestionCreateView.as_view(), name='forum-question-create'),
    path('questions/<int:pk>/update/', QuestionUpdateView.as_view(), name='forum-question-update'),
    path('questions/<int:pk>/delete/', QuestionDeleteView.as_view(), name='forum-question-delete'),
    path('my_questions/', views.my_questions, name='forum-my-questions'),
    path('my_answers/', views.my_answers, name='forum-my-answers'),
    path('my_comments/', views.my_comments, name='forum-my-comments'),
]

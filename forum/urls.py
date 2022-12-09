from django.urls import path
from . import views
from .views import QuestionListView, QuestionDetailView, QuestionCreateView, QuestionUpdateView, QuestionDeleteView, AnswerCreateView, AnswerUpdateView, AnswerDeleteView, CommentUpdateView, CommentDeleteView

urlpatterns = [
    path('', QuestionListView.as_view(), name='forum-index'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='forum-question-detail'),
    path('questions/new/', QuestionCreateView.as_view(), name='forum-question-create'),
    path('questions/<int:pk>/update/', QuestionUpdateView.as_view(), name='forum-question-update'),
    path('questions/<int:pk>/delete/', QuestionDeleteView.as_view(), name='forum-question-delete'),
    path('questions/<int:pk>/answer/', AnswerCreateView.as_view(), name='forum-answer-create'),
    path('questions/answer/<int:pk>/update/', AnswerUpdateView.as_view(), name='forum-answer-update'),
    path('questions/answer/<int:pk>/delete/', AnswerDeleteView.as_view(), name='forum-answer-delete'),
    path('questions/comment/<int:pk>/update/', CommentUpdateView.as_view(), name='forum-comment-update'),
    path('questions/comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='forum-comment-delete'),
    path('my_questions/', views.my_questions, name='forum-my-questions'),
    path('my_answers/', views.my_answers, name='forum-my-answers'),
    path('my_comments/', views.my_comments, name='forum-my-comments'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.search, name='forum-search'),
]

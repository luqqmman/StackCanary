from django.shortcuts import render
from django.http import HttpResponse
from .models import Pertanyaan
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# user / currently logged in user ga perlu di-pass ke context, auto diurus sama django

def index(request):
    context = {
        'pertanyaan': Pertanyaan.objects.all()
    }
    return render(request, 'forum/index.html', context)

def questions(request):
    context = {
        'pertanyaan': Pertanyaan.objects.all() # pertanyaan yg diklik
    }
    return render(request, 'forum/questions.html')

# Kalau mau dibuka, harus login dulu

@login_required
def my_question(request):
    context = {
        'pertanyaan': [],
    }
    return render(request, 'forum/my_question.html', context)

@login_required
def my_answer(request):
    context = {
        'jawaban': [],
    }
    return render(request, 'forum/my_answer.html', context)

@login_required
def my_comment(request):
    context = {
        'komentar': [],
    }
    return render(request, 'forum/my_comment.html', context)
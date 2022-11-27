from django.shortcuts import render
from django.http import HttpResponse

user = {
    'name': 'luqman',
    'nim': 'G6401211094'
}

questions = [
    {
        'title': 'Lorem ipsum',
        'description': 'how to dual boot arch and windows'
    }, 
    {
        'title': 'Ipsum lorem',
        'description': 'why windows is haram'
    }
]

def index(request):
    context = {
        'user': user,
        'questions': questions
    }
    return render(request, 'forum/index.html', context)

def login(request):
    return render(request, 'forum/login.html')

def question(request):
    return render(request, 'forum/index.html')

def my_question(request):
    context = {
        'questions': [],
    }
    return render(request, 'forum/my_question.html', context)

def my_answer(request):
    context = {
        'answers': [],
    }
    return render(request, 'forum/my_answer.html', context)

def my_comment(request):
    context = {
        'comments': [],
    }
    return render(request, 'forum/my_comment.html', context)
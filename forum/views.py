from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from .models import Pertanyaan, Jawaban, Komentar

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


def search(request):
    if request.method == 'POST':
        context = {
            'pertanyaan': Pertanyaan.objects.filter(judul__icontains=request.POST['search']),
        }
        print(context)
        return render(request, 'forum/search.html', context)


    
# class based

class QuestionListView(ListView):
    model = Pertanyaan
    template_name = 'forum/index.html'
    context_object_name = 'pertanyaan'
    ordering = ['-waktu_upload']

class QuestionDetailView(DetailView):
    model = Pertanyaan

class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Pertanyaan
    fields = ['judul', 'konten', 'snippet']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Pertanyaan
    fields = ['judul', 'konten', 'snippet']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        question = self.get_object()
        if self.request.user == question.author:
            return True
        return False

class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Pertanyaan
    success_url = '/forum/my_questions/'

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.author:
            return True
        return False

# Kalau mau dibuka, harus login dulu

@login_required
def my_questions(request):
    context = {
        'pertanyaan': Pertanyaan.objects.filter(author=request.user),
    }
    return render(request, 'forum/my_questions.html', context)

@login_required
def my_answers(request):
    context = {
        'jawaban': Jawaban.objects.filter(author=request.user),
    }
    return render(request, 'forum/my_answers.html', context)

@login_required
def my_comments(request):
    context = {
        'komentar': Komentar.objects.filter(author=request.user),
    }
    return render(request, 'forum/my_comments.html', context)
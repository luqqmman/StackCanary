from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from .models import Pertanyaan, Jawaban, Komentar
from .forms import CommentForm, AnswerForm


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
    return redirect(reverse('forum-index'))


# class based

class QuestionListView(ListView):
    model = Pertanyaan
    template_name = 'forum/index.html'
    context_object_name = 'pertanyaan'
    ordering = ['-waktu_upload']

class QuestionDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        question = Pertanyaan.objects.get(pk=pk)

        comment_form = CommentForm()
        answer_form = AnswerForm()
        comment = Komentar.objects.filter(pertanyaan_asal=question).order_by('-waktu_upload')
        answer = Jawaban.objects.filter(pertanyaan_asal=question).order_by('-waktu_upload')

        context = {
            'pertanyaan': question,
            'form': comment_form,
            'komentar': comment,
            'jawaban': answer,
            'answer_form': answer_form,
        }

        return render(request, 'forum/pertanyaan_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        question = Pertanyaan.objects.get(pk=pk)

        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            new_answer = answer_form.save(commit=False)
            new_answer.author = request.user
            new_answer.pertanyaan_asal = question
            new_answer.save()

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.pertanyaan_asal = question
            new_comment.save()

        comment_form = CommentForm()
        answer_form = AnswerForm()

        comment = Komentar.objects.filter(pertanyaan_asal=question).order_by('-waktu_upload')
        answer = Jawaban.objects.filter(pertanyaan_asal=question).order_by('-waktu_upload')

        context = {
            'pertanyaan': question,
            'form': comment_form,
            'komentar': comment,
            'jawaban': answer,
            'answer_form': answer_form,
        }

        return render(request, 'forum/pertanyaan_detail.html', context)

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

'''
class AnswerCreateView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        question = Pertanyaan.objects.get(pk=pk)
        form = AnswerForm()

        context = {
            'pertanyaan': question,
            'form': form,
        }

        return render(request, 'forum/jawaban_form.html', context)

    def post(self, request, pk, *args, **kwargs):
        question = Pertanyaan.objects.get(pk=pk)
        form = AnswerForm(request.POST)

        if form.is_valid():
            new_answer = form.save(commit=False)
            new_answer.author = request.user
            new_answer.pertanyaan_asal = question
            new_answer.save()
        
        form = AnswerForm()
        comment = Komentar.objects.filter(pertanyaan_asal=question).order_by('-waktu_upload')
        answer = Jawaban.objects.filter(pertanyaan_asal=question).order_by('-waktu_upload')

        context = {
            'pertanyaan': question,
            'form': form,
            'komentar': comment,
            'jawaban': answer,
        }

        return render(request, 'forum/jawaban_form.html', context)
'''

class AnswerCreateView(LoginRequiredMixin, CreateView):
    model = Jawaban
    #template_name = 'home/comment-form.html'
    fields = ['konten', 'snippet']

    def get_context_data(self, **kwargs):
        context = super(AnswerCreateView, self).get_context_data(**kwargs)
        context['pertanyaan'] = Pertanyaan.objects.get(pk=7)
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class AnswerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
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
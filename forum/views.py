from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from .models import Pertanyaan, Jawaban, Komentar
from .forms import CommentForm, AnswerForm


# class based

class QuestionListView(ListView):
    model = Pertanyaan
    template_name = 'forum/index.html'
    context_object_name = 'pertanyaan'
    ordering = ['-waktu_upload']

class QuestionDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        question = Pertanyaan.objects.get(pk=pk)
        self.current_question = question

        comment_form = CommentForm()
        comment = Komentar.objects.filter(pertanyaan_asal=question).order_by('-waktu_upload')
        answer = Jawaban.objects.filter(pertanyaan_asal=question).order_by('-waktu_upload')

        context = {
            'pertanyaan': question,
            'form': comment_form,
            'komentar': comment,
            'jawaban': answer,
        }

        return render(request, 'forum/pertanyaan_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        question = Pertanyaan.objects.get(pk=pk)

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.pertanyaan_asal = question
            new_comment.save()

        comment_form = CommentForm()

        comment = Komentar.objects.filter(pertanyaan_asal=question).order_by('-waktu_upload')
        answer = Jawaban.objects.filter(pertanyaan_asal=question).order_by('-waktu_upload')

        context = {
            'pertanyaan': question,
            'form': comment_form,
            'komentar': comment,
            'jawaban': answer,
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


class AnswerCreateView(LoginRequiredMixin, CreateView):
    model = Jawaban
    fields = ['konten', 'snippet']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question_pk'] = self.kwargs['pk']
        context['pertanyaan'] = get_object_or_404(Pertanyaan, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.pertanyaan_asal = get_object_or_404(Pertanyaan, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('forum-question-detail', args=[self.kwargs['pk']])

class AnswerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Jawaban
    fields = ['konten', 'snippet']
    template_name = 'forum/jawaban_form_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jawaban'] = get_object_or_404(Jawaban, pk=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        answer = self.get_object()
        if self.request.user == answer.author:
            return True
        return False

    def get_success_url(self):
        answer = get_object_or_404(Jawaban, pk=self.kwargs['pk'])
        question = get_object_or_404(Pertanyaan, pk=answer.pertanyaan_asal.pk)
        return reverse('forum-question-detail', args=[question.pk])

class AnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Jawaban

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jawaban'] = get_object_or_404(Jawaban, pk=self.kwargs['pk'])
        return context

    def test_func(self):
        answer = self.get_object()
        if self.request.user == answer.author:
            return True
        return False
    
    def get_success_url(self):
        answer = get_object_or_404(Jawaban, pk=self.kwargs['pk'])
        question = get_object_or_404(Pertanyaan, pk=answer.pertanyaan_asal.pk)
        return reverse('forum-question-detail', args=[question.pk])

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Komentar
    fields = ['konten']
    template_name = 'forum/komentar_form_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['komentar'] = get_object_or_404(Komentar, pk=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False

    def get_success_url(self):
        comment = get_object_or_404(Komentar, pk=self.kwargs['pk'])
        question = get_object_or_404(Pertanyaan, pk=comment.pertanyaan_asal.pk)
        return reverse('forum-question-detail', args=[question.pk])

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Komentar

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['komentar'] = get_object_or_404(Komentar, pk=self.kwargs['pk'])
        return context

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False
    
    def get_success_url(self):
        comment = get_object_or_404(Komentar, pk=self.kwargs['pk'])
        question = get_object_or_404(Pertanyaan, pk=comment.pertanyaan_asal.pk)
        return reverse('forum-question-detail', args=[question.pk])

# function based

def search(request):
    if request.method == 'POST':
        context = {
            'pertanyaan': Pertanyaan.objects.filter(judul__icontains=request.POST['search']),
        }
        return render(request, 'forum/search.html', context)
    return redirect(reverse('forum-index'))

# kalau mau dibuka, harus login dulu

@login_required
def my_questions(request):
    questions = Pertanyaan.objects.filter(author=request.user).order_by('-waktu_upload')
    context = {
        'pertanyaan': questions,
    }
    return render(request, 'forum/my_questions.html', context)

@login_required
def my_answers(request):
    answers = Jawaban.objects.filter(author=request.user).order_by('-waktu_upload')
    context = {
        'jawaban': answers,
    }
    return render(request, 'forum/my_answers.html', context)

@login_required
def my_comments(request):
    comments = Komentar.objects.filter(author=request.user).order_by('-waktu_upload')
    context = {
        'komentar': comments,
    }
    return render(request, 'forum/my_comments.html', context)

@login_required
def profile(request):
    context = {
        'questions_asked': len(Pertanyaan.objects.filter(author=request.user)),
        'answers_given': len(Jawaban.objects.filter(author=request.user)),
        'comments_made': len(Komentar.objects.filter(author=request.user)),
    }
    return render(request, 'forum/profile.html', context)
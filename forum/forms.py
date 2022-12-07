from django import forms
from .models import Komentar, Jawaban

class CommentForm(forms.ModelForm):
    konten = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '2',
                   'placeholder': 'Write some comments...',
                   'value': 'none',
                   'class': 'form-control mt-1 mb-3',
                   }
        ))

    class Meta:
        model = Komentar
        fields = ['konten']

class AnswerForm(forms.ModelForm):
    konten = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Write your answer...',
                   'value': 'none',
                   'class': 'form-control mt-1 mb-3',
                   }
        ))
    snippet = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Add some code if any...',
                   'value': 'none',
                   'class': 'form-control mt-1 mb-3',
                   }
        ))

    class Meta:
        model = Jawaban
        fields = ['konten', 'snippet']
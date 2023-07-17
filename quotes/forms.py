from django import forms

from .models import Topic, Quote

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text']
        labels = {'text': ''}
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80})
        }

from django import forms
from .models import Notice

class NoticeCreateForm(forms.ModelForm):
    class Meta: 
        model = Notice
        fields = ['title', 'content', 'author_name']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Введите заголовок...'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Введите текст объявления...'
            }),
            'author_name': forms.TextInput(attrs={
                'placeholder': 'Введите имя автора...'
            })
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Информация',
            'author_name': 'Имя автора'
        }
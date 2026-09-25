from django import forms
from .models import Notice
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class NoticeCreateForm(forms.ModelForm):
    class Meta: 
        model = Notice
        # fields = ['title', 'content', 'author_name']
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full border border-zinc-300 focus:border-pink-500 focus:ring-1 focus:ring-pink-200 rounded-lg px-4 py-3 text-slate-800 outline-none bg-white',
                'placeholder': 'Введите заголовок...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full h-30 border border-zinc-300 focus:border-pink-500 focus:ring-1 focus:ring-pink-200 rounded-lg px-4 py-3 text-slate-800 outline-none bg-white',
                'placeholder': 'Введите текст объявления...'
            }),
            # 'author_name': forms.TextInput(attrs={
            #     'placeholder': 'Введите имя автора...'
            # })
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Информация',
            # 'author_name': 'Имя автора'
        }

class RegisterForm(UserCreationForm):
    error_messages = {
        'password_mismatch': 'Пароли не совпадают',
    }
    email = forms.EmailField(
        required = True,
        widget = forms.EmailInput(attrs={
            'class': 'w-full border border-zinc-300 focus:border-pink-500 focus:ring-1 focus:ring-pink-200 rounded-lg px-4 py-3 text-slate-800 outline-none bg-white',
            'placeholder': 'Введите e-mail'
        }),
        label='Электронная почта'
    )
    first_name = forms.CharField(
        required=True,
        widget = forms.TextInput(attrs={
            'class': 'w-full border border-zinc-300 focus:border-pink-500 focus:ring-1 focus:ring-pink-200 rounded-lg px-4 py-3 text-slate-800 outline-none bg-white',
            'placeholder': 'Введите имя'
        }),
        label='Имя'
    )
    
    last_name = forms.CharField(
        required=True,
        widget= forms.TextInput(attrs={
            'class': 'w-full border border-zinc-300 focus:border-pink-500 focus:ring-1 focus:ring-pink-200 rounded-lg px-4 py-3 text-slate-800 outline-none bg-white',
            'placeholder': 'Введите фамилию'
        }),
        label='Фамилия'
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].help_text = ''

        self.fields['username'].widget.attrs.update({
            'class': 'w-full border border-zinc-300 focus:border-pink-500 focus:ring-1 focus:ring-pink-200 rounded-lg px-4 py-3 text-slate-800 outline-none bg-white',
            'placeholder': 'Введите логин'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full border border-zinc-300 focus:border-pink-500 focus:ring-1 focus:ring-pink-200 rounded-lg px-4 py-3 text-slate-800 outline-none bg-white',
            'placeholder': 'Введите пароль'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full border border-zinc-300 focus:border-pink-500 focus:ring-1 focus:ring-pink-200 rounded-lg px-4 py-3 text-slate-800 outline-none bg-white',
            'placeholder': 'Повторите пароль'
        })
        self.fields['username'].label = 'Логин'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтвердите пароль'

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Такой E-mail уже существует!')
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        if not password:
            return password

        if len(password) < 8:
            raise forms.ValidationError('Пароль должен содержать не менее 8 символов.')
        
        has_letter = any(c.isalpha() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)

        if not (has_letter and has_digit and has_special):
            raise forms.ValidationError('Пароль должен содержать буквы, цифры и специальные символы.')

        return password

class StyledLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            "class": "w-full border border-zinc-300 focus:border-pink-500 focus:ring-1 focus:ring-pink-200 rounded-lg px-4 py-3 text-slate-800 outline-none bg-white",
            "placeholder": "Введите логин"
        })
        self.fields['password'].widget.attrs.update({
            "class": "w-full border border-zinc-300 focus:border-pink-500 focus:ring-1 focus:ring-pink-200 rounded-lg px-4 py-3 text-slate-800 outline-none bg-white",
            "placeholder": "Введите пароль"
        })
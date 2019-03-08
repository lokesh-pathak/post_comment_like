from django.forms import ModelForm, TextInput, CharField, ModelChoiceField, Select, Textarea, ModelMultipleChoiceField, SelectMultiple, CheckboxSelectMultiple
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import *
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Question, Comment

class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='Username',
        max_length=32
    )
    email = forms.CharField(
        required=True,
        label='Email',
        max_length=32,
    )
    password = forms.CharField(
        required=True,
        label='Password',
        max_length=32,
        widget=forms.PasswordInput()
    )

    def clean_password(self):
        min_length = 6
        password = self.cleaned_data.get('password', None)
        if len(password) < min_length:
            raise forms.ValidationError("The password must be at least %d characters long." % min_length)

        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if (User.objects.filter(email=email).exists()):
            raise forms.ValidationError('email already exists')

        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if (User.objects.filter(username=username).exists()):
            raise forms.ValidationError('user already exists')

        return username


class LoginForm(forms.Form):
    email = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput())

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email == '':
            raise forms.ValidationError("eamil can't be empty")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password == '':
            raise forms.ValidationError("password can't be empty")
        return password

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        try:
            username = User.objects.get(email=email)
        except:
            username = None
        # print username
        if authenticate(username=username, password=password) is None:
            raise forms.ValidationError("entered email and password is not correct.")


class QuestionForm(ModelForm):

    class Meta:
        model = Question
        fields = ['title', 'text']
        widgets = {'title': TextInput(attrs={'class': 'input form-control', 'placeholder': 'Question Title',
                                             'size': 50, 'type': 'text', 'id': 'id_title', 'name': 'title', 'autofocus':'autofocus'}),
                   'text': Textarea(attrs={'allow-special': 'true', 'rows': '10', 'name': 'description'})}
        exclude = ('author', 'create_date', 'published_date')


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {'text': Textarea(attrs={'allow-special': 'true', 'rows': '10', 'name': 'description'})}
        exclude = ('post', 'author', 'create_date')

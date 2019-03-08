from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django import forms
from .forms import UserRegistrationForm
from .forms import LoginForm, QuestionForm, CommentForm
from .models import Question, Like
from django.views.generic import ListView, CreateView
from django.http import JsonResponse
from django.template import loader



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            username = cleaned_data['username']
            email = cleaned_data['email']
            password = cleaned_data['password']
            User.objects.create_user(username, email, password)
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            email = cleaned_data['email']
            password = cleaned_data['password']
            username = User.objects.get(email=email)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
              raise forms.ValidationError('invalid email & password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')



def save(instance, user, post_id=None):
    """
    :param instance:
    :param user:
    """
    instance.author = user
    if post_id:
        instance.post_id = post_id
    instance.save()
    return instance


def getquestion(request):

    params = {}
    params['form'] = QuestionForm()
    return render(request, "question.html", params)



class Questions(CreateView, ListView):
    question_form_class = QuestionForm
    redirect_template_name = 'home'
    params = {}

    def get(self, request):
        """
        :param request:
        :return: Display List
        """
        questions = Question.objects.select_related().all()
        self.params['questions'] = questions
        return render(request, "home.html", self.params)

    def post(self, request):
        """
        :param request:
        :return:
        """
        que = self.question_form_class(request.POST)
        if que.is_valid():
            save(que.save(commit=False), request.user)
            return HttpResponseRedirect(self.redirect_template_name)


class Comments(CreateView, ListView):
    form_class = CommentForm
    template = 'comment.html'
    params = dict()

    def get(self, request, *args, **kwargs):
        """
        :param request:
        :return: Display List
        """
        self.params['form'] = self.form_class()
        self.params['post_id'] =  kwargs.get('question_id')
        comments_html = loader.render_to_string(self.template, self.params)
        context = {'comments_html': comments_html}
        return JsonResponse(context)


    def post(self, request, *args, **kwargs):
        """
        :param request:
        :return:
        """
        comment = self.form_class(request.POST)
        if comment.is_valid():
            save(comment.save(commit=False), request.user, request.POST['post_id'] )
            return HttpResponseRedirect('/')

class LikeDisLike(CreateView, ListView):

    def get(self, request, *args, **kwargs):
        """
        :param request:
        :return:
        """
        obj = Like.objects.create(comment_id=kwargs.get('comment_id'), author=request.user)
        if obj:
            return HttpResponseRedirect('/')


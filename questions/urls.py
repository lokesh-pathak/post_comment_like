from django.contrib import admin
from django.conf.urls import url
from django.contrib.auth.decorators import login_required


from questions import views

urlpatterns = [
    url(r'register', views.register, name="signup"),
    url(r'login', views.user_login, name="login"),
    url(r'logout', views.user_logout, name="logout"),
    url(r'^question/$',views.getquestion, name="question_form"),
 	url(r'^question/(?P<question_id>[0-9]+)/comment/$',login_required(views.Comments.as_view()), name="comment_form"),
    url(r'^comment/(?P<comment_id>[0-9]+)/like/$',login_required(views.LikeDisLike.as_view())),
    url(r'', login_required(views.Questions.as_view()), name='question_list'),
]





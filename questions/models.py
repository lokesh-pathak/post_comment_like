from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Question(models.Model):
    author = models.ForeignKey(User ,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)


    def __str__(self):
         return self.title



class Comment(models.Model):
    post = models.ForeignKey(Question,on_delete=models.CASCADE)
    author = models.ForeignKey(User ,on_delete=models.CASCADE)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.text


class Like(models.Model):
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
    author = models.ForeignKey(User ,on_delete=models.CASCADE)

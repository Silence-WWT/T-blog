from django.db import models
from myblog.settings import MEDIA_ROOT


class User(models.Model):
    username = models.CharField(max_length=100)  # 以后可以unique=True简化
    password = models.CharField(max_length=50)
    sex = models.CharField(max_length=10)
    head_show = models.FileField(upload_to=MEDIA_ROOT)
    register_date = models.DateField()
    email = models.EmailField()

    def __str__(self):
        return self.username


class Blog(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User)
    created_time = models.CharField(max_length=25)
    modified_time = models.CharField(max_length=25)
    content = models.TextField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, related_name='comment_author')
    target = models.ForeignKey(User, related_name='comment_target')
    created_time = models.DateTimeField()
    content = models.TextField()


class BlogImg(models.Model):
    image = models.FileField(upload_to=MEDIA_ROOT)
    blog = models.ForeignKey(Blog)


class Photo(models.Model):
    photo = models.FileField(upload_to=MEDIA_ROOT)
    author = models.ForeignKey(User)
    description = models.CharField(max_length=100)
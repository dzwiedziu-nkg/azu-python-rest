from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg
from django.utils import timezone


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Title')
    content = models.TextField(verbose_name='Content')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    pub_date = models.DateTimeField(default=timezone.now, verbose_name='Date published')

    def get_avg_score(self):
        return self.vote_set.aggregate(Avg('points'))['points__avg']

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-pub_date']


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name='Author')
    content = models.TextField(verbose_name='Comment body')
    pub_date = models.DateTimeField(default=timezone.now, verbose_name='Date published')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['pub_date']


class Vote(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    points = models.IntegerField(validators=[MaxValueValidator(6), MinValueValidator(1)])
    vote_date = models.DateTimeField(default=timezone.now, verbose_name='Date voted')

    class Meta:
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'
        ordering = ['vote_date']

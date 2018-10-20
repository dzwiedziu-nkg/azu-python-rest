from django.contrib import admin

from blog.models import Vote, Comment, Article


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


class VoteInline(admin.TabularInline):
    model = Vote
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [CommentInline, VoteInline]

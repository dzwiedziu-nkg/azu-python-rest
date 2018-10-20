from rest_framework import serializers

from blog.models import Article, Vote, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('article',)
        read_only_fields = ('pub_date',)


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        exclude = ('article',)
        read_only_fields = ('vote_date',)


class ArticleListSerializer(serializers.ModelSerializer):
    comments_count = serializers.SerializerMethodField(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)
    votes = serializers.SerializerMethodField(read_only=True)

    def get_comments_count(self, obj:Article):
        return obj.comment_set.count()

    def get_rating(self, obj:Article):
        return obj.get_avg_score()

    def get_votes(self, obj:Article):
        return obj.vote_set.count()

    class Meta:
        model = Article
        exclude = ('content',)


class ArticleWithCommentsSerializer(ArticleListSerializer):
    comments = CommentSerializer(many=True, read_only=True, source='comment_set')

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('pub_date', 'author')

from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from blog.models import Article, Comment
from blog.serializers import ArticleListSerializer, ArticleWithCommentsSerializer, CommentSerializer, VoteSerializer


class ArticlesViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        else:
            return ArticleWithCommentsSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def check_object_permissions(self, request, obj: Article):
        if self.action in ['update', 'destroy', 'partial_update']:
            user = self.request.user
            if not user.is_superuser and user.id != obj.author_id:
                self.permission_denied(
                    request, message='You can modify and delete only self articles'
                )
        super().check_object_permissions(request, obj)

    def check_permissions(self, request):
        if self.action != 'vote':
            super().check_permissions(request)

    @action(methods=['post'], detail=True)
    def vote(self, request, pk=None):
        serializer = VoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(article_id=pk)
        return Response({'status': 'voted'}, status=status.HTTP_201_CREATED)


class CommentsViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    serializer_class = CommentSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        article_id = int(self.kwargs['article_id'])
        return Comment.objects.filter(article_id=article_id)

    def perform_create(self, serializer):
        article_id = int(self.kwargs['article_id'])
        serializer.save(article_id=article_id)

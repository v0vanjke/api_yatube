from rest_framework import status, viewsets
from rest_framework.response import Response

from api.serializers import (CommentSerializer, GroupListSerializer,
                             PostSerializer)
from posts.models import Comment, Group, Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        post_id = self.kwargs.get('pk')
        post = Post.objects.get(pk=post_id)
        serializer = self.get_serializer(post, data=request.data)
        if request.user != post.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        post_id = self.kwargs.get('pk')
        post = Post.objects.get(pk=post_id)
        if request.user != post.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupListSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(
            post_id=self.kwargs.get('id'),
            author=self.request.user,
        )

    def get_queryset(self):
        post_id = self.kwargs.get('id')
        comment_queryset = Comment.objects.filter(post=post_id)
        return comment_queryset

    def update(self, request, *args, **kwargs):
        comment_id = self.kwargs.get('pk')
        comment = Comment.objects.get(pk=comment_id)
        serializer = self.get_serializer(comment, data=request.data)
        if request.user != comment.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        comment_id = self.kwargs.get('pk')
        comment = Comment.objects.get(pk=comment_id)
        if request.user != comment.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

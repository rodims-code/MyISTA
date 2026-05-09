from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Follow, Post, Comment, Like
from .serializers import (
    FollowSerializer, PostSerializer, CommentSerializer, LikeSerializer, UserBasicSerializer
)

User = get_user_model()

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        
        # Check if already liked
        like, created = Like.objects.get_or_create(user=user, post=post)
        
        if not created:
            # If already liked, unlike it
            like.delete()
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
            
        return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def toggle(self, request):
        following_id = request.data.get('following_id')
        if not following_id:
            return Response({'error': 'following_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            following_user = User.objects.get(id=following_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user == following_user:
            return Response({'error': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)

        follow, created = Follow.objects.get_or_create(follower=request.user, following=following_user)
        
        if not created:
            follow.delete()
            return Response({'status': 'unfollowed'}, status=status.HTTP_200_OK)
            
        return Response({'status': 'followed'}, status=status.HTTP_201_CREATED)

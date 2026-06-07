from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Follow, Post, Comment, Like, Favorite, Conversation, Message, Notification
from .serializers import (
    FollowSerializer, PostSerializer, CommentSerializer, LikeSerializer, UserBasicSerializer,
    FavoriteSerializer, ConversationSerializer, MessageSerializer, NotificationSerializer
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
            
        if post.author != user:
            Notification.objects.create(
                user=post.author,
                sender=user,
                type='like',
                post=post,
                text=f"{user.username} a aimé votre publication."
            )

        return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        post = self.get_object()
        favorite, created = Favorite.objects.get_or_create(user=request.user, post=post)

        if not created:
            favorite.delete()
            return Response({'status': 'removed'}, status=status.HTTP_200_OK)

        if post.author != request.user:
            Notification.objects.create(
                user=post.author,
                sender=request.user,
                type='favorite',
                post=post,
                text=f"{request.user.username} a enregistré votre publication."
            )

        return Response({'status': 'saved'}, status=status.HTTP_201_CREATED)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        if comment.post.author != self.request.user:
            Notification.objects.create(
                user=comment.post.author,
                sender=self.request.user,
                type='comment',
                post=comment.post,
                text=f"{self.request.user.username} a commenté votre publication."
            )

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

        Notification.objects.create(
            user=following_user,
            sender=request.user,
            type='follow',
            text=f"{request.user.username} vous suit maintenant."
        )

        return Response({'status': 'followed'}, status=status.HTTP_201_CREATED)

class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('post', 'user').order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def toggle(self, request):
        post_id = request.data.get('post_id')
        if not post_id:
            return Response({'error': 'post_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        favorite, created = Favorite.objects.get_or_create(user=request.user, post=post)
        if not created:
            favorite.delete()
            return Response({'status': 'removed'}, status=status.HTTP_200_OK)

        if post.author != request.user:
            Notification.objects.create(
                user=post.author,
                sender=request.user,
                type='favorite',
                post=post,
                text=f"{request.user.username} a enregistré votre publication."
            )

        return Response({'status': 'saved'}, status=status.HTTP_201_CREATED)

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Conversation.objects
            .filter(participants=self.request.user)
            .prefetch_related('participants', 'messages')
            .order_by('-updated_at')
        )

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participants') or request.data.get('participant_ids') or []
        participant_id = request.data.get('participant_id')

        if participant_id:
            participant_ids = [participant_id]

        participant_ids = [str(user_id) for user_id in participant_ids if str(user_id) != str(request.user.id)]
        if not participant_ids:
            return Response({'error': 'participant_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        participants = list(User.objects.filter(id__in=participant_ids))
        if not participants:
            return Response({'error': 'No participant found'}, status=status.HTTP_404_NOT_FOUND)

        if len(participants) == 1:
            conversation = (
                Conversation.objects
                .filter(participants=request.user)
                .filter(participants=participants[0])
                .first()
            )
            if conversation:
                serializer = self.get_serializer(conversation)
                return Response(serializer.data, status=status.HTTP_200_OK)

        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, *participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticated])
    def messages(self, request, pk=None):
        conversation = self.get_object()

        if request.method == 'GET':
            messages = conversation.messages.select_related('sender').order_by('created_at')
            serializer = MessageSerializer(messages, many=True, context={'request': request})
            return Response(serializer.data)

        content = request.data.get('content', '').strip()
        fichier = request.FILES.get('fichier')
        if not content and not fichier:
            return Response({'error': 'content or fichier is required'}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content,
            fichier=fichier
        )
        conversation.save()

        recipients = conversation.participants.exclude(id=request.user.id)
        for recipient in recipients:
            Notification.objects.create(
                user=recipient,
                sender=request.user,
                type='message',
                conversation=conversation,
                text=f"Nouveau message de {request.user.username}."
            )

        serializer = MessageSerializer(message, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_seen(self, request, pk=None):
        conversation = self.get_object()
        conversation.messages.exclude(sender=request.user).update(seen=True)
        return Response({'status': 'seen'}, status=status.HTTP_200_OK)

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).select_related('sender', 'post', 'conversation').order_by('-created_at')

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save(update_fields=['is_read'])
        return Response({'status': 'read'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_all_read(self, request):
        self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({'status': 'read'}, status=status.HTTP_200_OK)

class UserSearchViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserBasicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.all().order_by('username')
        query = self.request.query_params.get('q', '').strip()

        if query:
            queryset = queryset.filter(
                Q(username__icontains=query) |
                Q(matricule__icontains=query) |
                Q(filiere__icontains=query) |
                Q(niveau__icontains=query)
            )

        return queryset[:20]

from rest_framework import serializers
from .models import Follow, Post, Comment, Like, Favorite, Conversation, Message, Notification
from django.contrib.auth import get_user_model

User = get_user_model()

class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'matricule', 'role', 'filiere', 'niveau']

class FollowSerializer(serializers.ModelSerializer):
    follower_details = UserBasicSerializer(source='follower', read_only=True)
    following_details = UserBasicSerializer(source='following', read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'follower_details', 'following_details', 'created_at']
        read_only_fields = ['follower']

class CommentSerializer(serializers.ModelSerializer):
    author_details = UserBasicSerializer(source='author', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_details', 'content', 'created_at']
        read_only_fields = ['author']

class LikeSerializer(serializers.ModelSerializer):
    user_details = UserBasicSerializer(source='user', read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'user_details', 'created_at']
        read_only_fields = ['user']

class MessageSerializer(serializers.ModelSerializer):
    sender_details = UserBasicSerializer(source='sender', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'sender_details', 'content', 'fichier', 'seen', 'created_at']
        read_only_fields = ['sender', 'seen']

class ConversationSerializer(serializers.ModelSerializer):
    participants_details = UserBasicSerializer(source='participants', many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'participants_details', 'last_message', 'unread_count', 'created_at', 'updated_at']
        read_only_fields = ['participants']

    def get_last_message(self, obj):
        message = obj.messages.order_by('-created_at').first()
        if not message:
            return None
        return MessageSerializer(message, context=self.context).data

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.messages.exclude(sender=request.user).filter(seen=False).count()
        return 0

class FavoriteSerializer(serializers.ModelSerializer):
    user_details = UserBasicSerializer(source='user', read_only=True)
    post_details = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'post', 'post_details', 'user_details', 'created_at']
        read_only_fields = ['user']

    def get_post_details(self, obj):
        return PostSerializer(obj.post, context=self.context).data

class NotificationSerializer(serializers.ModelSerializer):
    sender_details = UserBasicSerializer(source='sender', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'user', 'sender', 'sender_details', 'type', 'post', 'conversation', 'text', 'is_read', 'created_at']
        read_only_fields = ['user']

class PostSerializer(serializers.ModelSerializer):
    author_details = UserBasicSerializer(source='author', read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    favorites_count = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_details', 'content', 'image', 'fichier', 'created_at', 'likes_count', 'comments_count', 'is_liked', 'favorites_count', 'is_favorited']
        read_only_fields = ['author']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def get_favorites_count(self, obj):
        return obj.favorites.count()

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorites.filter(user=request.user).exists()
        return False

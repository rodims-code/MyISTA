from rest_framework import serializers
from .models import Follow, Post, Comment, Like
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

class PostSerializer(serializers.ModelSerializer):
    author_details = UserBasicSerializer(source='author', read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_details', 'content', 'image', 'fichier', 'created_at', 'likes_count', 'comments_count', 'is_liked']
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

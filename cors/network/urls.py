from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet, CommentViewSet, FollowViewSet, FavoriteViewSet,
    ConversationViewSet, NotificationViewSet, UserSearchViewSet
)

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'follows', FollowViewSet)
router.register(r'favorites', FavoriteViewSet, basename='favorite')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'users', UserSearchViewSet, basename='network-user')

urlpatterns = [
    path('', include(router.urls)),
]

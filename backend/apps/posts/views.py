from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer, PostListSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Post model providing full CRUD operations.

    list: Get all posts
    create: Create a new post
    retrieve: Get a single post by ID
    update: Update a post (full update)
    partial_update: Partially update a post
    destroy: Delete a post
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']

    def get_serializer_class(self):
        """
        Use different serializer for list action.
        """
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer

    def get_permissions(self):
        """
        Set custom permissions for different actions.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAuthorOrReadOnly()]
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Set the author to the current user when creating a post.
        """
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'])
    def my_posts(self, request):
        """
        Get posts created by the current user.
        Endpoint: /api/posts/my_posts/
        """
        posts = self.queryset.filter(author=request.user)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def published(self, request):
        """
        Get only published posts.
        Endpoint: /api/posts/published/
        """
        posts = self.queryset.filter(is_published=True)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors to edit their own posts.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for the author
        return obj.author == request.user

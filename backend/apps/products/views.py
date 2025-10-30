from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Product model providing full CRUD operations.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at', 'name']

    def get_permissions(self):
        """Set custom permissions for different actions."""
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAuthorOrReadOnly()]
        return super().get_permissions()

    def perform_create(self, serializer):
        """Set the author to the current user when creating a product."""
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def my_products(self, request):
        """Get products created by the current user."""
        products = self.queryset.filter(created_by=request.user)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # @action(detail=False, methods=['get'])
    # def published(self, request):
    #     """Get only published posts."""
    #     posts = self.queryset.filter(is_published=True)
    #     serializer = self.get_serializer(posts, many=True)
    #     return Response(serializer.data)


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow authors to edit their own products."""

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for the author
        return obj.created_by == request.user
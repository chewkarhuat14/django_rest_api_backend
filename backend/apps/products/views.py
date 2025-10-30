from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework.pagination import PageNumberPagination


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow authors to edit their own products."""

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for the author
        return obj.created_by == request.user


class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'pagesize'
    max_page_size = 100

class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Product model providing full CRUD operations.
    """
    pagination_class = ProductPagination
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at', 'name']


    def get_queryset(self):
        """
        Limit products to the ones created by the current user.
        """
        user = self.request.user
        
        # If user is not authenticated, return nothing
        if not user.is_authenticated:
            return Product.objects.none()
        
        # Start with user's products only
        queryset = Product.objects.filter(created_by=user)
        
        # Apply search filter if provided
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Override create to set the created_by field to the current user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=201)

    @action(detail=False, methods=['get'])
    def low_cost(self, request):
        """Get products with low cost"""
        cost = request.query_params.get('cost', 100)
        products = self.queryset.filter(cost__lt=cost)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    

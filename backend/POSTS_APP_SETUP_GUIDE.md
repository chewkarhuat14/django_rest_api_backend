# Django Posts App - Complete CRUD Setup Guide

This guide provides step-by-step instructions for setting up a new Django app with full CRUD operations using Django REST Framework.

## Table of Contents
1. [Project Structure](#project-structure)
2. [Step-by-Step Setup](#step-by-step-setup)
3. [Model Details](#model-details)
4. [API Endpoints](#api-endpoints)
5. [Testing the API](#testing-the-api)
6. [Common Commands](#common-commands)

---

## Project Structure

After setup, your `apps/posts/` directory will contain:

```
apps/posts/
├── __init__.py
├── admin.py          # Admin interface configuration
├── apps.py           # App configuration
├── models.py         # Post model definition
├── serializers.py    # DRF serializers for JSON conversion
├── views.py          # API views and viewsets
├── urls.py           # URL routing for posts API
├── migrations/       # Database migrations
│   └── __init__.py
└── tests.py          # Unit tests (optional)
```

---

## Step-by-Step Setup

### Step 1: Create the Django App

```bash
# Create the app directory first
mkdir -p apps/posts

# Generate the Django app structure
python manage.py startapp posts apps/posts
```

**What this does:**
- Creates a new Django app named "posts" inside the `apps/` directory
- Generates default files: models.py, views.py, admin.py, etc.

---

### Step 2: Create the Post Model

**File:** `apps/posts/models.py`

```python
from django.db import models
from django.conf import settings


class Post(models.Model):
    """
    Post model for blog posts with CRUD operations.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title
```

**Model Fields Explained:**
- `title`: Post title (max 200 characters)
- `content`: Post content (unlimited text)
- `author`: Foreign key to User model
- `created_at`: Auto-set on creation
- `updated_at`: Auto-updated on save
- `is_published`: Boolean flag for published status

---

### Step 3: Create Serializers

**File:** `apps/posts/serializers.py`

```python
from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model with all CRUD operations.
    """
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'author',
            'author_username',
            'created_at',
            'updated_at',
            'is_published'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'author_username']

    def create(self, validated_data):
        """
        Create a new post with the current user as author.
        """
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing posts.
    """
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'author_username',
            'created_at',
            'is_published'
        ]
        read_only_fields = ['id', 'created_at', 'author_username']
```

**Why Two Serializers?**
- `PostSerializer`: Full detail for create/retrieve/update
- `PostListSerializer`: Lighter for list views (better performance)

---

### Step 4: Create Views

**File:** `apps/posts/views.py`

```python
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer, PostListSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Post model providing full CRUD operations.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']

    def get_serializer_class(self):
        """Use different serializer for list action."""
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer

    def get_permissions(self):
        """Set custom permissions for different actions."""
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAuthorOrReadOnly()]
        return super().get_permissions()

    def perform_create(self, serializer):
        """Set the author to the current user when creating a post."""
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'])
    def my_posts(self, request):
        """Get posts created by the current user."""
        posts = self.queryset.filter(author=request.user)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def published(self, request):
        """Get only published posts."""
        posts = self.queryset.filter(is_published=True)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow authors to edit their own posts."""

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for the author
        return obj.author == request.user
```

**Features:**
- Full CRUD operations via `ModelViewSet`
- Search functionality on title and content
- Ordering by created_at, updated_at, title
- Custom actions: `my_posts`, `published`
- Custom permission: only authors can edit/delete their posts

---

### Step 5: Create URL Configuration

**File:** `apps/posts/urls.py`

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

# The API URLs are determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]
```

**What this does:**
- Uses DRF's `DefaultRouter` to automatically generate URL patterns
- Creates standard REST endpoints for all CRUD operations

---

### Step 6: Configure Admin Interface

**File:** `apps/posts/admin.py`

```python
from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin interface for Post model."""

    list_display = ['id', 'title', 'author', 'is_published', 'created_at', 'updated_at']
    list_filter = ['is_published', 'created_at', 'updated_at']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'content', 'author')
        }),
        ('Status', {
            'fields': ('is_published',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
```

---

### Step 7: Update Main Settings

**File:** `config/settings.py`

Add the posts app to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',

    # Local apps
    'apps.users',
    'apps.posts',  # Add this line
]
```

---

### Step 8: Update Main URL Configuration

**File:** `config/urls.py`

Add the posts URLs to the main urlpatterns:

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/', include('apps.posts.urls')),  # Add this line
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

---

### Step 9: Create and Run Migrations

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate
```

**Expected Output:**
```
Migrations for 'posts':
  apps/posts/migrations/0001_initial.py
    - Create model Post
```

---

### Step 10: Create a Superuser (Optional)

```bash
# Create a superuser to test the admin interface
python manage.py createsuperuser
```

Follow the prompts to set username, email, and password.

---

## Model Details

### Post Model Fields

| Field | Type | Description | Options |
|-------|------|-------------|---------|
| `id` | AutoField | Primary key | Auto-generated |
| `title` | CharField | Post title | max_length=200 |
| `content` | TextField | Post content | Unlimited text |
| `author` | ForeignKey | User who created | Related to User model |
| `created_at` | DateTimeField | Creation timestamp | auto_now_add=True |
| `updated_at` | DateTimeField | Last update timestamp | auto_now=True |
| `is_published` | BooleanField | Published status | default=False |

### Model Relationships

- **Post → User**: Many-to-One (Each post has one author)
- **User → Posts**: One-to-Many (Each user can have many posts)

---

## API Endpoints

### Base URL: `http://localhost:8000/api/`

### Standard CRUD Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/posts/` | List all posts | No |
| POST | `/api/posts/` | Create a new post | Yes |
| GET | `/api/posts/{id}/` | Retrieve a specific post | No |
| PUT | `/api/posts/{id}/` | Full update of a post | Yes (author only) |
| PATCH | `/api/posts/{id}/` | Partial update of a post | Yes (author only) |
| DELETE | `/api/posts/{id}/` | Delete a post | Yes (author only) |

### Custom Action Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/posts/my_posts/` | Get current user's posts | Yes |
| GET | `/api/posts/published/` | Get only published posts | No |

### Query Parameters

**List Endpoint (`/api/posts/`)**

- **Search**: `?search=keyword`
  - Example: `/api/posts/?search=django`
  - Searches in title and content fields

- **Ordering**: `?ordering=field_name`
  - Example: `/api/posts/?ordering=-created_at`
  - Available fields: `created_at`, `updated_at`, `title`
  - Use `-` prefix for descending order

- **Pagination**: `?page=2`
  - Default page size: 10 items
  - Example: `/api/posts/?page=2`

---

## Testing the API

### 1. Start the Development Server

```bash
python manage.py runserver
```

Server will start at: `http://localhost:8000/`

---

### 2. Test with cURL

#### Get All Posts (No Auth Required)
```bash
curl http://localhost:8000/api/posts/
```

#### Create a Post (Auth Required)
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Post",
    "content": "This is the content of my first post.",
    "is_published": true
  }'
```

#### Get a Specific Post
```bash
curl http://localhost:8000/api/posts/1/
```

#### Update a Post (Auth Required - Author Only)
```bash
curl -X PATCH http://localhost:8000/api/posts/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title"
  }'
```

#### Delete a Post (Auth Required - Author Only)
```bash
curl -X DELETE http://localhost:8000/api/posts/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Search Posts
```bash
curl "http://localhost:8000/api/posts/?search=django"
```

#### Get My Posts
```bash
curl http://localhost:8000/api/posts/my_posts/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Get Published Posts
```bash
curl http://localhost:8000/api/posts/published/
```

---

### 3. Test with HTTPie (Alternative)

```bash
# Install HTTPie
pip install httpie

# Get all posts
http GET http://localhost:8000/api/posts/

# Create a post
http POST http://localhost:8000/api/posts/ \
  Authorization:"Bearer YOUR_ACCESS_TOKEN" \
  title="My First Post" \
  content="This is the content" \
  is_published=true
```

---

### 4. Test with Django Admin

1. Navigate to: `http://localhost:8000/admin/`
2. Login with your superuser credentials
3. Click on "Posts" to manage posts
4. Use the admin interface to create, edit, and delete posts

---

### 5. Test with DRF Browsable API

1. Navigate to: `http://localhost:8000/api/posts/`
2. You'll see Django REST Framework's browsable API
3. Use the HTML form to create/update posts
4. View JSON responses in the browser

---

## Common Commands

### Database Operations

```bash
# Create migration files
python manage.py makemigrations

# Show migration SQL (without applying)
python manage.py sqlmigrate posts 0001

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations

# Rollback migration
python manage.py migrate posts 0001  # Replace with migration number
```

### Development Server

```bash
# Run development server
python manage.py runserver

# Run on specific port
python manage.py runserver 8080

# Run on specific host/port
python manage.py runserver 0.0.0.0:8000
```

### Django Shell

```bash
# Open Django shell
python manage.py shell

# Example: Create a post in shell
>>> from apps.posts.models import Post
>>> from apps.users.models import User
>>> user = User.objects.first()
>>> post = Post.objects.create(
...     title="Test Post",
...     content="Test content",
...     author=user,
...     is_published=True
... )
>>> print(post)
```

### Testing

```bash
# Run all tests
python manage.py test

# Run tests for posts app only
python manage.py test apps.posts

# Run with verbose output
python manage.py test --verbosity=2
```

### Database Management

```bash
# Flush database (delete all data)
python manage.py flush

# Create database backup (PostgreSQL)
pg_dump -U dti_admin -d django_rest_db > backup.sql

# Restore database (PostgreSQL)
psql -U dti_admin -d django_rest_db < backup.sql
```

---

## Permissions Summary

| Action | Permission Required | Additional Check |
|--------|---------------------|------------------|
| List posts | None | - |
| View post detail | None | - |
| Create post | IsAuthenticated | Author auto-set to current user |
| Update post | IsAuthenticated | Must be post author |
| Delete post | IsAuthenticated | Must be post author |
| View my_posts | IsAuthenticated | Filters by current user |
| View published | None | - |

---

## Next Steps

### 1. Add Comments Feature
- Create a `Comment` model with ForeignKey to `Post`
- Add nested serializers
- Create comment endpoints

### 2. Add Categories/Tags
- Create `Category` or `Tag` models
- Add ManyToMany relationship with Post
- Add filtering by category/tag

### 3. Add Image Upload
- Add `ImageField` to Post model
- Configure media file handling
- Update serializers to handle file uploads

### 4. Add Pagination Customization
```python
# In views.py
from rest_framework.pagination import PageNumberPagination

class PostPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

# In PostViewSet
pagination_class = PostPagination
```

### 5. Add Tests
```python
# In tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from apps.users.models import User
from .models import Post

class PostAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )

    def test_list_posts(self):
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, 200)

    def test_create_post_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/posts/', {
            'title': 'New Post',
            'content': 'New content',
            'is_published': True
        })
        self.assertEqual(response.status_code, 201)
```

---

## Troubleshooting

### Common Issues

**Issue: "No such table: posts_post"**
```bash
# Solution: Run migrations
python manage.py makemigrations
python manage.py migrate
```

**Issue: "Permission denied" when creating/updating posts**
```bash
# Solution: Ensure you're authenticated with JWT token
# Get token first:
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

**Issue: "posts is not a registered namespace"**
```bash
# Solution: Check that 'apps.posts' is in INSTALLED_APPS
# in config/settings.py
```

**Issue: "relation does not exist" in PostgreSQL**
```bash
# Solution: Make sure migrations are applied
python manage.py migrate
```

---

## Summary

You have successfully created a Django posts app with:

- **Model**: Post model with title, content, author, timestamps
- **Serializers**: Full and list serializers for optimal performance
- **Views**: Complete CRUD operations using ModelViewSet
- **URLs**: RESTful routing with DefaultRouter
- **Admin**: Full-featured admin interface
- **Permissions**: Custom permissions for author-only editing
- **Features**: Search, ordering, filtering, custom actions

### File Checklist

- [x] `apps/posts/models.py` - Post model
- [x] `apps/posts/serializers.py` - Serializers
- [x] `apps/posts/views.py` - ViewSets and views
- [x] `apps/posts/urls.py` - URL routing
- [x] `apps/posts/admin.py` - Admin configuration
- [x] `config/settings.py` - Added 'apps.posts' to INSTALLED_APPS
- [x] `config/urls.py` - Added posts URLs
- [x] Migrations created and applied

### Quick Reference Card

```bash
# Setup
python manage.py makemigrations
python manage.py migrate

# Development
python manage.py runserver

# Testing
curl http://localhost:8000/api/posts/

# Admin
http://localhost:8000/admin/
```

---

**Generated**: 2025-10-29
**Django Version**: 4.x+
**Django REST Framework**: 3.x+

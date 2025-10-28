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

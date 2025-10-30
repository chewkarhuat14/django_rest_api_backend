from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for the Product model"""

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'cost', 'status', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    
    def validate_price(self, value):
        """Ensure the price is a positive value"""
        if value < 0:
            raise serializers.ValidationError("Price must be a positive value.")
        return value

    def validate_cost(self, value):
        """Ensure the cost is a positive value"""
        if value < 0:
            raise serializers.ValidationError("Cost must be a positive value.")
        return value

    def validate_status(self, value):
        """Ensure the status is a boolean value"""
        if not isinstance(value, bool):
            raise serializers.ValidationError("Status must be a boolean value.")
        return value

    def create(self, validated_data):
        """Create and return a new Product instance"""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
  
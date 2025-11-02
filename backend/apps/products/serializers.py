from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for the Product model"""

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'tax', 'cost', 'calculate_total_price', 'status', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    
    def validate_price(self, value):
        """Ensure the price is a positive value"""
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive value.")
        return value

    def validate_cost(self, value):
        """Ensure the cost is a positive value"""
        if value <= 0:
            raise serializers.ValidationError("Cost must be a positive value.")
        return value

    def validate_stock(self, value):
        """Ensure the stock is a non-negative integer"""
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value
        
    def validate_name(self, value):
        """Ensure the name is not empty"""
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        return value
    
    def validate_tax(self, value):
        """Ensure the tax is a non-negative value"""
        
        if value < 0.01:
            raise serializers.ValidationError("Tax must be at least 0.01 (1%).")
        
        if value > 1:
            raise serializers.ValidationError("Tax cannot exceed 1.00 (100%).")
        return value

    def validate_status(self, value):
        """Ensure the status is a boolean value"""
        if not isinstance(value, bool):
            raise serializers.ValidationError("Status must be a boolean value.")
        return value

    def validate(self, data):
        """
        Object-level validation to ensure cost is less than or equal to price.
        (You typically want to sell products for more than they cost you)

        This handles both create and update (including partial update) operations.
        """
        # Get values from data or fall back to existing instance values for updates
        if self.instance:  # This is an update
            cost = data.get('cost', self.instance.cost)
            price = data.get('price', self.instance.price)
        else:  # This is a create
            cost = data.get('cost')
            price = data.get('price')

        # Both fields must be present for comparison
        if cost is not None and price is not None:
            if cost > price:
                raise serializers.ValidationError(
                    "Cost cannot be higher than price. You would be selling at a loss!"
                )

        return data

    def create(self, validated_data):
        """Create and return a new Product instance"""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError  # Make sure to import this

class Product(models.Model):
    """
    Product model with CRUD operations.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total_price(self):
        """
        Calculate total price including tax.
        Example: tax = 0.06 means 6% tax.
        """
        return self.price * (1 + self.tax)

    def clean(self):
        """
        Ensure price is not less than cost.
        """
        if self.price < self.cost:
            raise ValidationError("Price cannot be less than cost.")

    def __str__(self):
        return f"{self.name} (created by {self.created_by.username})"

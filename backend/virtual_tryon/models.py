from django.db import models
import uuid

class TryOnSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_photo = models.ImageField(upload_to='original_photos/', null=True, blank=True)
    result_photo = models.ImageField(upload_to='result_photos/', null=True, blank=True)
    selected_clothing = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pendente'),
        ('processing', 'Processando'),
        ('completed', 'Concluído'),
        ('failed', 'Falhou'),
    ], default='pending')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Session {self.id} - {self.status}"

class ClothingItem(models.Model):
    CLOTHING_TYPES = [
        ('shirt', 'Camiseta'),
        ('pants', 'Calça'),
        ('shorts', 'Bermuda'),
        ('shoes', 'Tênis'),
    ]
    
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=CLOTHING_TYPES)
    image = models.ImageField(upload_to='clothing_items/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

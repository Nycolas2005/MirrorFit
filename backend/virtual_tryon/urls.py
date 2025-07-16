from django.urls import path
from .views import TryOnAPIView, HealthCheckView, ClothingItemsAPIView

urlpatterns = [
    path('try-on/', TryOnAPIView.as_view(), name='try-on'),
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('clothing-items/', ClothingItemsAPIView.as_view(), name='clothing-items'),
]

from django.urls import path
from .views import (
    wishlist_view,
    toggle_view
)
app_name = 'wishlist'

urlpatterns = [
    path('', wishlist_view, name='wishlist'),
    path('<int:livro_id>/', toggle_view, name='toggle'),
]

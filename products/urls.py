from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    ProductsListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDetailView,
    ProductDeleteView,
    ProductsViewSets
    )

urlpatterns = [
    path('', ProductsListView.as_view()),
    path('create', ProductCreateView.as_view()),
    path('update/<int:pk>', ProductUpdateView.as_view()),
    path('detail/<int:pk>', ProductDetailView.as_view()),
    path('delete/<int:pk>', ProductDeleteView.as_view()),
]

# router = DefaultRouter()
# router.register(r'all-methods/view-sets', ProductsViewSets, basename='products')
# urlpatterns += router.urls
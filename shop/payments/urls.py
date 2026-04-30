from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('item/<int:id>/', views.item_page),
    path('buy/<int:id>/', views.buy),
    path('success/', views.success),
    path('cancel/', views.cancel),
]
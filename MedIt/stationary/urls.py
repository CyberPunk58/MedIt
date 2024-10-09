from django.urls import path
from . import views

urlpatterns = [
    path('', views.stationary_view, name='stationary'),
    path('admin/', views.stationary_admin_view, name='stationary_admin'),
]
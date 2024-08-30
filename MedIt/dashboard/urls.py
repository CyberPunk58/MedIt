from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('admin/', views.dashboard_admin_view, name='dashboard_admin'),
    path('knowledge_base/', views.knowledge_base_view, name='knowledge_base'),
    path('knowledge_base/add-section/', views.add_section_view, name='add_section'),
    path('knowledge_base/add-article/', views.add_article_view, name='add_article'),
]

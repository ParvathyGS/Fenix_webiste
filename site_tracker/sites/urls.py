from django.urls import path
from . import views

urlpatterns = [
    path('', views.public_home, name='home'),
    path('dashboard/', views.site_list, name='list_sites'),
    path('site/<int:site_id>/', views.site_detail, name='site_detail'),
    path('site/add/', views.add_site, name='site_create'),
    path('site/edit/<int:site_id>/', views.edit_site, name='site_update'),
    path('site/delete/<int:site_id>/', views.delete_site, name='site_delete'),
    path('site/<int:site_id>/photo/add/', views.add_site_image, name='site_image_add'),
    path('photo/<int:image_id>/delete/', views.delete_site_image, name='site_image_delete'),
]

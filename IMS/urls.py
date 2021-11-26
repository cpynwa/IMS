from django.urls import path
from . import views

urlpatterns = [
    path('IMS/list', views.data_list, name='data_list'),
    path('IMS/<int:pk>/', views.data_detail, name='data_detail'),
    path('IMS/new', views.data_new, name='data_new'),
    path('IMS/<int:pk>/edit/', views.data_edit, name='data_edit'),
    path('IMS/search', views.search, name='data_search'),
    path('IMS/main', views.dashboard, name='data_dashboard'),
    path('IMS/list/export', views.data_export, name='data_export'),
    # path('detail/<int:pk>/delete', views.data_delete, name='data_delete'),

    path('IMS/delivery/list', views.delivery_list, name='delivery_list'),
    path('IMS/delivery/<int:pk>/', views.delivery_detail, name='delivery_detail'),
    path('IMS/delivery/new', views.delivery_new, name='delivery_new'),
    path('IMS/delivery/<int:pk>/edit', views.delivery_edit, name='delivery_edit'),
    path('IMS/delivery/search', views.delivery_search, name='delivery_search')
]
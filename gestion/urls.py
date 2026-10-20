from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('proveedores/', views.proveedores_lista, name='proveedores_lista'),
    path('proveedores/nuevo/', views.proveedor_crear, name='proveedor_crear'),
    path('proveedores/<int:pk>/', views.proveedor_detalle, name='proveedor_detalle'),
    path('proveedores/<int:pk>/editar/', views.proveedor_editar, name='proveedor_editar'),
    path('proveedores/<int:pk>/eliminar/', views.proveedor_eliminar, name='proveedor_eliminar'),
    path('compras/', views.compras_lista, name='compras_lista'),
    path('compras/nueva/', views.compra_crear, name='compra_crear'),
    path('compras/<int:pk>/', views.compra_detalle, name='compra_detalle'),
    path('compras/<int:pk>/editar/', views.compra_editar, name='compra_editar'),
    path('compras/<int:pk>/eliminar/', views.compra_eliminar, name='compra_eliminar'),
]

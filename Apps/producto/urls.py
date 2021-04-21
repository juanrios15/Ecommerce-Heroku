from django.contrib import admin
from django.urls import path

from . import views

app_name = "productos_app"

urlpatterns = [
   path('productos',views.VistaProductos.as_view(),name="productos"),
   path('detalleproducto/<slug>/',views.DetalleProducto.as_view(),name="detalle"),
   path('agregarfavorito/<producto>/',views.FavoritoCreateView.as_view(),name="addfavorito"),
   path('carrito',views.VistaCarrito.as_view(),name="carrito"),
   path('borrardelcarrito/<producto>',views.BorrarDelCarrito.as_view(),name="borrardelcarrito"),
]
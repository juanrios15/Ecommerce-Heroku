from django.contrib import admin
from django.urls import path

from . import views

app_name = "posts_app"

urlpatterns = [
    path('publicaciones',views.VistaPublicaciones.as_view(),name="publicaciones"),
    path('publicacion/<slug>',views.PublicacionView.as_view(),name="detallepost"),
    path('nuevapublicacion',views.NewPostView.as_view(),name="newpost"),
    path('editarpublicacion/<slug>',views.PostUpdateView.as_view(),name="editpost"),
    path('borrarfoto/<pk>',views.FotoDeleteView.as_view(),name="borrarfoto"),
]
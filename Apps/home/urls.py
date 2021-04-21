from django.contrib import admin
from django.urls import path

from . import views

app_name = "home_app"

urlpatterns = [
    path('',views.Inicio.as_view(),name="inicio"),
    path('registro',views.UserCreateView.as_view(),name="registrousuario"),
    path('login',views.Login.as_view(),name="loginusuario"),
    path('logout',views.Logout.as_view(),name="logoutusuario"),
    path('cambiarpassword',views.CambiarPassword.as_view(),name="cambiarpassword"),
    path('detalleusuario/<slug>/',views.UserDetailView.as_view(),name="detalleusuario"),
    path('updateusuario/',views.UsuarioUpdateView.as_view(),name="updateusuario"),
    path('eliminarusuario',views.UserDeleteView.as_view(),name="eliminarcuenta"),
    path('shoppingrecord',views.UserShoppingRecordView.as_view(),name="historialcompras"),
]
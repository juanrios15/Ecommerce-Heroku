from django.contrib import admin

# Register your models here.
from django.contrib import admin
from Apps.home.models import Departamento, Perfil, Servicio

from django.contrib.auth.admin import UserAdmin
from .models import User


class mipanel(admin.ModelAdmin):
    
    list_display = ('abreviacion','nombre')

class perfilpanel(admin.ModelAdmin):
    
    list_display = ('user','cargo','departamento','edad')
    search_fields = ("user","departamento")
    

# Register your models here.
admin.site.register(Perfil, perfilpanel)
admin.site.register(Departamento, mipanel)
admin.site.register(User, UserAdmin)
admin.site.register(Servicio)


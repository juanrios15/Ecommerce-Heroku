from django.contrib import admin

from Apps.publicaciones.models import Comentario, Etiqueta, Foto, Publicacion

class FotoInline(admin.TabularInline):
    
    model =  Foto
    max_num = Foto.MAX_FOTOS
    can_delete = False

class mipanel(admin.ModelAdmin):
    
    model = Publicacion
    inlines = (FotoInline,)
    readonly_fields = ("user","created_at","updated_at", "visitas")
    filter_horizontal = ('etiquetas',) #ver mas bonito en el admin la categoria de mchos a muchos
    
    list_display = ('titulo','user','visitas','created_at','publico')
    
    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user_id = request.user.id
        obj.save()

class comenpanel(admin.ModelAdmin):

    list_display = ('user','Publicacion','created_at','mensaje')
    search_fields = ("user__username","Publicacion__titulo")
    
    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user_id = request.user.id
        obj.save()

class fotopanel(admin.ModelAdmin):
    list_display = ('imagen','publicacion')
    
class etiquetapanel(admin.ModelAdmin):
    list_display = ('nombre','descripcion')
    

# Register your models here.
admin.site.register(Etiqueta,etiquetapanel)
admin.site.register(Publicacion, mipanel)
admin.site.register(Foto,fotopanel)
admin.site.register(Comentario,comenpanel)

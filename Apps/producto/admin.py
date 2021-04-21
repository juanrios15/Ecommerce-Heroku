from django.contrib import admin
from Apps.producto.models import CategoriaProducto, Color, DetalleVenta, Favorito, FotoProducto, Producto, Talla, Venta
# Register your models here.
class FotoInline(admin.TabularInline):
    
    model =  FotoProducto
    max_num = FotoProducto.MAX_FOTOS
    can_delete = False

class prodpanel(admin.ModelAdmin):
    
    model = Producto
    inlines = (FotoInline,)
    
    list_display = ('nombre','cantidad','precio','categoria','marca')
    readonly_fields = ("slug","created_at","updated_at", "visitas")
    search_fields = ("nombre","marca")
    list_filter = ("categoria__nombre",)
    
    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user_id = request.user.id
        obj.save()

class ventadetallepanel(admin.ModelAdmin):
    list_display = ('producto','venta','info_extra','cantidad','subtotal')
    search_fields = ("venta__id","producto__nombre")

class ventapanel(admin.ModelAdmin):
    list_display = ('id','fecha_venta','user','valor_total','email','celular')
    search_fields = ("id","user__username")
    

class colorpanel(admin.ModelAdmin):
    list_display = ('color','codigo')
    
class categoriapanel(admin.ModelAdmin):
    list_display = ('nombre','descripcion')
    
class favoritopanel(admin.ModelAdmin):
    list_display = ('producto','user','created_at')
    


admin.site.register(Producto,prodpanel)
admin.site.register(CategoriaProducto,categoriapanel)
admin.site.register(Favorito,favoritopanel)
admin.site.register(Venta,ventapanel)
admin.site.register(DetalleVenta,ventadetallepanel)
admin.site.register(Color,colorpanel)
admin.site.register(Talla)
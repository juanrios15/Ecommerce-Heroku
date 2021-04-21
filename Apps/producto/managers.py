from django.db import models

class ProductosManager(models.Manager):
    
    def buscar_pub(self,kword,categoria,orden):
        print("kword: ",kword,"categoria: ",categoria,"orden: ",orden)
        #busqueda por palabra clave y por filtro por categorias
        if orden == "visitas":
            orderby = '-visitas'
        elif orden == "antiguos":
            orderby = 'created_at'
        elif orden == "menorprecio":
            orderby = 'precio'
        elif orden == "mayorprecio":
            orderby = '-precio'
        else:
            orderby = '-created_at'
        
        if len(categoria) >0 and categoria!="todos":
            return self.filter(
                categoria__nombre = categoria,
                nombre__icontains = kword,
                publico=True
            ).order_by(orderby)
        
        else:
            return self.filter(
                nombre__icontains = kword,
                publico=True
            ).order_by(orderby)
            

class FotosProductosManager(models.Manager):
    def fotos_producto(self,slug):
        return self.filter(
            producto__slug=slug)
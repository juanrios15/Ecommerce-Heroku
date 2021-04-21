from datetime import datetime, timedelta

from django.db import models
from ckeditor.fields import RichTextField

from django.conf import settings

from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
User = get_user_model()

from Apps.producto.managers import FotosProductosManager, ProductosManager

# Create your models here.
class CategoriaProducto(models.Model):
    nombre = models.CharField(verbose_name="Categoria", max_length=100)
    descripcion = models.CharField(verbose_name="Descripcion", max_length=250)
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
    
    def __str__(self):
        return self.nombre
    
class Color(models.Model):
    color = models.CharField(max_length=50)
    codigo = models.CharField(max_length=7)
    
    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colores"
    
    def __str__(self):
        return self.color

class Talla(models.Model):
    talla = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = "Talla"
        verbose_name_plural = "Tallas"
    
    def __str__(self):
        return self.talla
    
    
class Producto(models.Model):
    
    nombre = models.CharField(max_length=150,verbose_name="Nombre")
    marca = models.CharField(verbose_name="Marca", max_length=250, default=None)
    cantidad = models.IntegerField()
    precio = models.IntegerField()
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE, verbose_name="Categorias")
    imagen = models.ImageField(upload_to="media", height_field=None, width_field=None, max_length=None,blank=True)
    descripcion = RichTextField(verbose_name="Descripcion",blank=True)
    color = models.ManyToManyField(Color,blank=True, related_name="coloresproducto")
    talla = models.ManyToManyField(Talla,blank=True, related_name="tallasproducto")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Usuario", on_delete=models.CASCADE, editable=False)
    publico = models.BooleanField(default=False)
    visitas = models.IntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at= models.DateTimeField(auto_now=True, verbose_name="Actualizado el")
    slug = models.SlugField(default="",editable=False,max_length=150)
    
    objects = ProductosManager()
    
    class Meta:
        verbose_name= "Producto"
        verbose_name_plural = "Productos"
    
    def __str__(self):
        return self.nombre

    def save(self,*args, **kwargs):
        
        if not self.slug:
            now = datetime.now()
            total_time = timedelta(
                hours=now.hour,
                minutes=now.minute,
                seconds=now.second
            )

            seconds = int(total_time.total_seconds())
            slug_unique = '%s-%s-%s' % (self.nombre,self.marca, str(seconds))
            self.slug = slugify(slug_unique)

        super(Producto,self).save(*args, **kwargs)
    
    def get_absolute_url(self):
    
        return reverse_lazy(
            'productos_app:detalle',
            kwargs = {
                'slug': self.slug
            }
        
    )

class FotoProducto(models.Model):
    MAX_FOTOS = 7
    
    producto = models.ForeignKey(Producto, verbose_name=("Producto"), on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="media", height_field=None, width_field=None, max_length=None,blank=False)
    
    objects = FotosProductosManager()
    
    class Meta:
        verbose_name= "Foto"
        verbose_name_plural = "Fotos"
        
    def __str__(self):
        return str(self.imagen) 


class Favorito(models.Model):
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    
    class Meta:
        unique_together = ('producto','user')
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'

    def __str__(self):
        return self.producto.nombre


class Venta(models.Model):
    
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,blank=True, null=True)
    fecha_venta = models.DateTimeField('Fecha de Venta',)
    valor_total = models.IntegerField()
    nombre = models.CharField(max_length=150,blank=False)
    apellido = models.CharField(max_length=150,blank=False)
    email = models.EmailField(max_length=254,blank=False)
    direccion = models.CharField(max_length=350,blank=False)
    ciudad = models.CharField(max_length=50,blank=False)
    departamento = models.CharField(max_length=50,blank=False)
    celular = models.CharField(max_length=15)
    forma_pago = models.CharField(max_length=25)
    
    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'

    def __str__(self):
        fecha = str(self.fecha_venta.strftime('%d-%m-%y %H:%M'))
        return f'ID={self.id} - {fecha} - {self.nombre} {self.apellido} - Total $ {self.valor_total}'

class DetalleVenta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    info_extra = models.CharField(max_length=150, blank=True,default=" ")
    cantidad = models.IntegerField()
    subtotal = models.IntegerField()
    
    
    class Meta:
        verbose_name = 'Producto Vendido'
        verbose_name_plural = 'Productos vendidos'

    def __str__(self):
        return f"{self.producto}"
    
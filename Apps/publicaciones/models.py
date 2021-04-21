from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from ckeditor.fields import RichTextField
from django.conf import settings

from .managers import FotosManager
from Apps.publicaciones.managers import ComentariosManager, PublicacionesManager, EtiquetasManager
from django.template.defaultfilters import slugify

# Create your models here.
class Etiqueta(models.Model):
    nombre = models.CharField(verbose_name="Etiqueta", max_length=100)
    descripcion = models.CharField(verbose_name="Descripcion", max_length=250)
    
    objects = EtiquetasManager()
    
    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"
    
    def __str__(self):
        return self.nombre
    
class Publicacion(models.Model):
    
    titulo = models.CharField(max_length=150,verbose_name="Titulo")
    resumen = models.CharField(verbose_name="Resumen", max_length=250)
    etiquetas = models.ManyToManyField(Etiqueta, verbose_name="Etiquetas", blank=True, related_name="tags_pubs")
    imagen = models.ImageField(upload_to="media", height_field=None, width_field=None, max_length=None,blank=True)
    video = models.FileField(verbose_name="Video", upload_to="media",blank=True)
    descripcion = RichTextField(verbose_name="Descripcion",blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Usuario", on_delete=models.CASCADE, editable=False)
    publico = models.BooleanField(default=False)
    visitas = models.IntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at= models.DateTimeField(auto_now=True, verbose_name="Actualizado el")
    slug = models.SlugField(default="",editable=False,max_length=150)
    
    
    objects = PublicacionesManager()
    class Meta:
        verbose_name= "Publicación"
        verbose_name_plural = "Publicaciones"
        ordering = ["titulo","-created_at"]
        # db_table = 'publicaciones'
    
    def __str__(self):
        return self.titulo
    
    def save(self,*args, **kwargs):
        
        if not self.slug:
            now = datetime.now()
            total_time = timedelta(
                hours=now.hour,
                minutes=now.minute,
                seconds=now.second
            )

            seconds = int(total_time.total_seconds())
            slug_unique = '%s-%s' % (self.titulo, str(seconds))
            self.slug = slugify(slug_unique)

        super(Publicacion,self).save(*args, **kwargs)

class Foto(models.Model):
    
    MAX_FOTOS = 5
    
    publicacion = models.ForeignKey(Publicacion, verbose_name=("Publicacion"), on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="media", height_field=None, width_field=None, max_length=None,blank=False)

    
    objects = FotosManager()
    
    class Meta:
        verbose_name= "Foto"
        verbose_name_plural = "Fotos"
        
    def __str__(self):
        return str(self.imagen) 

class Comentario(models.Model):
    
    Publicacion = models.ForeignKey(Publicacion, verbose_name=("Publicacion"), on_delete=models.CASCADE)
    mensaje = models.CharField(verbose_name="Mensaje", max_length=250)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Usuario", on_delete=models.CASCADE, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at= models.DateTimeField(auto_now=True, verbose_name="Actualizado el")
    
    objects = ComentariosManager()
    
    class Meta:
        verbose_name= "Comentario"
        verbose_name_plural = "Comentarios"
        
    def __str__(self):
        return "Comentario de: "+ str(self.user) + " en la publicacion: "+ str(self.Publicacion)
    
    
    
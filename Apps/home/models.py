from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from ckeditor.fields import RichTextField

from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify

class User(AbstractUser):
    slug = models.SlugField()
    
    def save(self,*args, **kwargs):
        
        slug_unique = '%s' % (self.username)
        self.slug = slugify(slug_unique)

        super(User,self).save(*args, **kwargs)
        

# Create your models here.

class Departamento(models.Model):
    nombre = models.CharField(verbose_name="Nombre", max_length=100)
    abreviacion = models.CharField(verbose_name="Abreviación", max_length=50)

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
    
    def __str__(self):
        return self.nombre

class Perfil(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=("Usuario"), on_delete=models.CASCADE)
    cargo= models.CharField(verbose_name="Cargo", max_length=150,blank=True)
    bio = RichTextField(verbose_name="Biografía",blank=True)
    edad = models.IntegerField(default=0)
    departamento = models.ForeignKey(Departamento, verbose_name=("Departamento"), on_delete=models.CASCADE,blank=True, null=True)
    foto = models.ImageField(upload_to="media", height_field=None, width_field=None, max_length=None, blank=True)
    linkedin = models.URLField(verbose_name=("Perfil linkedin"), max_length=200, blank=True)
    
    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"
    
    def __str__(self):
        return self.user.get_full_name()
    

        
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
        

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.perfil.save()

class Servicio(models.Model):
    nombre = models.CharField(max_length=150)
    resumen = models.CharField(max_length=250, default=" ")
    descripcion = RichTextField(verbose_name="Descripción")
    imagen = models.ImageField(upload_to="media", height_field=None, width_field=None, max_length=None)
    
    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
    
    def __str__(self):
        return self.nombre

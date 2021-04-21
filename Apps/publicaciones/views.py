from datetime import datetime
import random

from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.db.models import Avg, Count
from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models.functions import Lower
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.core.paginator import Paginator

from django.views.generic import ListView, DetailView, CreateView, TemplateView, FormView, UpdateView, View

from Apps.publicaciones.models import Comentario, Etiqueta, Foto, Publicacion
from Apps.publicaciones.forms import NewPostForm, PostFormSet
from Apps.producto.models import Favorito, Producto
from django.contrib import messages
from django.http import HttpResponseRedirect
# Create your views here.


class VistaPublicaciones(ListView):
    
    model = Publicacion
    template_name= "publicaciones/lista.html"
    paginate_by = 5
    context_object_name= "publicaciones"
    
    def get_context_data(self, **kwargs):
        context = super(VistaPublicaciones,self).get_context_data(**kwargs)
        context["etiquetas"] = Etiqueta.objects.all()
        context["etiqueta"] = self.request.GET.get("etiqueta",'')
        context["kword"] = self.request.GET.get("kword",'')
        context['orden'] = self.request.GET.get("orden",'')
        
        #Usando el values que funciona como el group by de SQL
        #context["comments"] = Comentario.objects.values('user').annotate(cuenta=Count('user'),nombre=Lower('user__username'))
        
        return context
    
    def get_queryset(self):
        kword = self.request.GET.get("kword",'')
        etiqueta = self.request.GET.get("etiqueta",'')
        orden = self.request.GET.get("orden",'')
        
        #TODO: toca arreglar el buscador y todo eso para los filtros, por ahora que de un solo boton se hagan los cambios
        lista = Publicacion.objects.buscar_pub(kword,etiqueta,orden).annotate(comments_count=Count('comentario', distinct=True),fotos_count=Count('foto', distinct=True))
        return lista

    


class PublicacionView(CreateView):
    model= Comentario
    fields = ('mensaje',)
    template_name= "publicaciones/detalle.html"
    
    
    #En este view se puede ver el detalle de la publicacion, las fotos, comentarios y se puede agregar un comentario
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['publicacion'] = Publicacion.objects.get(slug=self.kwargs['slug'])
        context['publicacion'].visitas +=1
        context['publicacion'].save(update_fields=['visitas'])
        context['galeria'] = Foto.objects.fotos_publicacion(self.kwargs['slug'])
        # context["favoritos"] = Favorito.objects.filter(user__id = self.request.user.id).values_list('producto__id',flat=True)
        context['comentarios'] = Comentario.objects.comentarios_publicacion(self.kwargs['slug']).order_by('-updated_at')[:10]
        
        x = list(Producto.objects.all().order_by('created_at')[:10])
        xx= random.sample(x,k=3)
        context['productos']= xx
        #USANDO EL PAGINATOR PARA CREAR UNA PAGINACION DE LOS COMENTARIOS QUE TIENE LA PUBLICACION
        # p = Paginator(x,5) 
        # page_number = self.request.GET.get('page')
        # page_obj = p.get_page(page_number)
        # context['comentarios'] = page_obj
        
        #context['edad_prom'] = Comentario.objects.comentarios_publicacion(self.kwargs['slug']).aggregate(prom=Avg('user__perfil__edad',distinct=True))
        
        return context
    
    def form_valid(self,form):

        form.instance.user = self.request.user
        form.instance.Publicacion = Publicacion.objects.get(slug=self.kwargs['slug'])

        return super(PublicacionView,self).form_valid(form)
    
    def get_success_url(self):
        return self.request.path


class NewPostView(LoginRequiredMixin,CreateView):
    
    form_class = NewPostForm
    template_name = "publicaciones/crear.html"
    success_url = reverse_lazy('posts_app:publicaciones')
    login_url = reverse_lazy('home_app:loginusuario')
    # extra_context = {'foto_formset': BookFormSet}
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["foto_formset"] = PostFormSet
        return context
    
    
    def form_valid(self,form):

        form.instance.user = self.request.user
        
        t = form.save()
        pub = Publicacion.objects.get(pk=t.id)
        formset = PostFormSet(self.request.POST, self.request.FILES, instance=pub)
        print(formset)
        formset.save()

        return super(NewPostView,self).form_valid(form)
    


class PostUpdateView(LoginRequiredMixin,UpdateView):
    
    model = Publicacion
    form_class = NewPostForm
    template_name = "publicaciones/actualizar.html"
    login_url = reverse_lazy('home_app:loginusuario')
    
    def get_success_url(self):
        slug = self.kwargs['slug']
        return reverse_lazy('posts_app:detallepost', kwargs={'slug': slug})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["foto_formset"] = PostFormSet
        context["fotos"] = Foto.objects.filter(publicacion__slug=self.kwargs['slug'])
        context["pub"] = Publicacion.objects.get(slug=self.kwargs['slug'])
        return context
    
    
    def form_valid(self,form):

        form.instance.user = self.request.user
        
        t = form.save()
        pub = Publicacion.objects.get(pk=t.id)
        formset = PostFormSet(self.request.POST, self.request.FILES, instance=pub)
        print(formset)
        formset.save()
        messages.success(self.request,"Publicación actualizada con exito")

        return super(PostUpdateView,self).form_valid(form)


class FotoDeleteView(LoginRequiredMixin,View):
    login_url = reverse_lazy('home_app:loginusuario')
    
    def post(self,request,*args,**kwargs):
        # print(self.kwargs["pk"])
        foto = Foto.objects.get(id=self.kwargs["pk"])
        foto.delete()
        messages.success(self.request, 'Foto borrada')        
        
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
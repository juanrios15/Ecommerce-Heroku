
from django.shortcuts import redirect, render

from django.views.generic import CreateView, TemplateView, DetailView, UpdateView, FormView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.messages.views import SuccessMessageMixin 

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.db.models import Count
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView

from Apps.publicaciones.models import Comentario, Etiqueta, Publicacion
from Apps.home.models import Perfil, Servicio
from Apps.home.forms import ProfileForm, UserForm, UserCreateForm
from django.contrib.auth import logout

import random
import string
from Apps.producto.models import DetalleVenta, Favorito, Producto

from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
User = get_user_model()

# def code_generator(size=6,chars=string.ascii_uppercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))



#from Apps.home.forms import UserRegisterForm
# Create your views here.
class Inicio(TemplateView):
    template_name = "home/inicio.html"
    
    
    def get_context_data(self, **kwargs):
        context = super(Inicio, self).get_context_data(**kwargs)
        
        #muestra de productos
        muestra_productos= list(Producto.objects.all().order_by('-created_at')[:10])
        productos_nuevos = random.sample(muestra_productos,k=4)
        context["productos"] = productos_nuevos
        
        #muestra de populares
        muestra_populares = list(Producto.objects.all().order_by('-visitas')[:10])
        populares = random.sample(muestra_populares,k=3)
        context["populares"] = populares
        
        #muestra de publicaciones
        muestra_publicaciones = list(Publicacion.objects.all().order_by('-created_at')[:3])
        publicaciones_nuevas = random.sample(muestra_publicaciones,k=2)
        context["publicaciones"] = publicaciones_nuevas
        
        #primeros servicios
        
        context["servicios"] = Servicio.objects.all().order_by('id')[:3]
        
        return context
    


class UserCreateView(SuccessMessageMixin,CreateView):
    form_class = UserCreateForm
    template_name = "home/registro.html"
    success_url = reverse_lazy('home_app:loginusuario')
    success_message = "Usuario registrado con exito, por favor inicie sesión..."
    

class Login(SuccessMessageMixin,LoginView):
    template_name = 'home/login.html'
    success_message = "Bienvenido!!!"
    
class Logout(LoginRequiredMixin,LogoutView):
    login_url = reverse_lazy('home_app:loginusuario')
    next_page = reverse_lazy('home_app:inicio')
    
    def get_next_page(self):
        next_page = super(Logout, self).get_next_page()
        messages.success(self.request, 'Hasta Pronto')
        return next_page
    
class CambiarPassword(LoginRequiredMixin,PasswordChangeView):
    template_name = "home/cambiarpassword.html"
    success_url = reverse_lazy('home_app:loginusuario')
    login_url = reverse_lazy('home_app:loginusuario')
    
    def form_valid(self, form):
        messages.success(self.request, "Contraseña modificada correctamente, por favor inicie sesión nuevamente")
        logout(self.request)
        return super().form_valid(form)

class UserDetailView(DetailView):
    
    template_name = "home/detalleusuario.html"
    model = User
    context_object_name = 'usuario'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.kwargs['slug']
        context["etiquetas"] = Etiqueta.objects.etiquetas_usuarios(user)
        
        #TODO: Paginacion del historial de comentarios del usuario
        
        context["comentarios"] = Comentario.objects.filter(user__slug=user).order_by('-created_at')[:10]
        context["total_comentarios"] = Comentario.objects.filter(user__slug=user).aggregate(total=Count('id'))
        x = Favorito.objects.filter(user__slug=user).order_by('-created_at')
        
        #USANDO EL PAGINATOR PARA CREAR UNA PAGINACION DE LOS COMENTARIOS QUE TIENE LA PUBLICACION
        p = Paginator(x,6) 
        page_number = self.request.GET.get('page')
        page_obj = p.get_page(page_number)
        context["page_obj"] = page_obj
        
        return context
    
    

#Una forma de hacer sin clases dos formularios


# @login_required
# def update_profile(request):
    
#     if request.method == 'POST':
#         user_form = UserForm(request.POST, instance=request.user)
#         profile_form = ProfileForm(request.POST, instance=request.user.perfil)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, ('Your profile was successfully updated!'))
#             return redirect(reverse_lazy('home_app:detalleusuario')) #falta arreglar esto
#         else:
#             messages.error(request, ('Please correct the error below.'))
#     else:
#         user_form = UserForm(instance=request.user)
#         profile_form = ProfileForm(instance=request.user.perfil)
        
#     return render(request, 'home/update.html', {
#         'form': user_form,
#         'profile_form': profile_form
#     })
    
class UsuarioUpdateView(LoginRequiredMixin,FormView):
    
    form_class = UserForm
    template_name = "home/update.html"
    success_url = reverse_lazy('home_app:inicio')
    extra_context = {'profile_form': ProfileForm}
    login_url = reverse_lazy('home_app:loginusuario')
    
    def get_context_data(self, **kwargs):
        context = super(UsuarioUpdateView,self).get_context_data(**kwargs)
        
        context['form'] = UserForm(instance=self.request.user) 
        context['profile_form'] = ProfileForm(instance=self.request.user.perfil)
        
        return context
    
    def form_valid(self, form):

        user_form = UserForm(self.request.POST,  instance=self.request.user)
        profile_form = ProfileForm(self.request.POST,self.request.FILES, instance=self.request.user.perfil)
        user_form.save()
        profile_form.save()
        
        return super().form_valid(form)

class UserDeleteView(LoginRequiredMixin,View):
    login_url = reverse_lazy('home_app:loginusuario')
    
    def post(self,request,*args,**kwargs):
        
        user = User.objects.get(id=self.request.user.id)
        user.delete()
        messages.success(self.request, 'Cuenta eliminada con exito')        
        
        return HttpResponseRedirect(
                reverse(
                    'home_app:inicio'
                )
            )


class UserShoppingRecordView(LoginRequiredMixin,TemplateView):
    template_name = "home/shoppingrecord.html"
    login_url = reverse_lazy('home_app:loginusuario')
    
    def get_context_data(self, **kwargs):
        context = super(UserShoppingRecordView, self).get_context_data(**kwargs)
        
        context['record'] = DetalleVenta.objects.filter(venta__user__id=self.request.user.id).order_by('-venta__fecha_venta')
        
        return context
        
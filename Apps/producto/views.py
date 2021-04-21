from django.shortcuts import render
from django.utils import timezone
# Create your views here.
from django.views.generic import ListView, FormView, TemplateView, View, CreateView
from Apps.producto.models import CategoriaProducto, Color, DetalleVenta, Favorito, FotoProducto, Producto, Venta
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin 


from Apps.producto.forms import CarritoForm, VentaForm
from django.db.models import Avg, Count, FloatField, Max
from django.http import HttpResponseRedirect
import random
from django.contrib import messages
from django.core.paginator import Paginator


class VistaProductos(ListView):
    
    model = Producto
    template_name= "productos/lista.html"
    paginate_by = 12
    context_object_name= "productos"
    
    def get_context_data(self, **kwargs):
        context = super(VistaProductos,self).get_context_data(**kwargs)
        context["categoria"] = self.request.GET.get("categoria",'')
        context["kword"] = self.request.GET.get("kword",'')
        context['orden'] = self.request.GET.get("orden",'')
        
        #context["precios"] = context["productos"].aggregate(Avg('precio'),Max('precio'))
        context["categorias"] = CategoriaProducto.objects.all().annotate(cant_prod=Count('producto'))
        # context["favoritos"] = Favorito.objects.filter(user__id = self.request.user.id).values_list('producto__id',flat=True)
        context["todos"] = Producto.objects.all().aggregate(total=Count('id'))
    #     context["precio_diff"] = Producto.objects.aggregate(price_diff=Max('precio', output_field=FloatField()) - Avg('precio'))
        return context
    
    def get_queryset(self):
        kword = self.request.GET.get("kword",'')
        categoria = self.request.GET.get("categoria",'')
        orden = self.request.GET.get("orden",'')
        
        #TODO: toca arreglar el buscador y todo eso para los filtros, por ahora que de un solo boton se hagan los cambios
        lista = Producto.objects.buscar_pub(kword,categoria,orden)
        return lista

class DetalleProducto(FormView):
    
    form_class = CarritoForm
    template_name= "productos/detalle.html"
    success_url = reverse_lazy('productos_app:productos')
    
    def get_context_data(self, **kwargs):
        context = super(DetalleProducto,self).get_context_data(**kwargs)
        context['producto'] =  Producto.objects.get(slug=self.kwargs['slug'])
        context['producto'].visitas +=1
        context['producto'].save(update_fields=['visitas'])
        context['colores'] = Color.objects.filter(coloresproducto__id=context['producto'].id)
        context['galeria'] = FotoProducto.objects.fotos_producto(self.kwargs['slug'])
        x = list(Producto.objects.filter(categoria=context['producto'].categoria).order_by('created_at').exclude(id=context['producto'].id)[:10])
        try:
            producto_recomendado = random.sample(x,k=1)
        except:
            producto_recomendado = []
        context['productos']= producto_recomendado
        
        #muestra de populares
        muestra_populares = list(Producto.objects.all().order_by('-visitas')[:10])
        populares = random.sample(muestra_populares,k=2)
        context["populares"] = populares
        
        return context
    
    def get_form_kwargs(self):
        kwargs = super(DetalleProducto, self).get_form_kwargs()

        # get users, note: you can access request using: self.request
        producto = Producto.objects.get(slug=self.kwargs['slug'])
        kwargs['id'] = producto.id
        kwargs['slug'] = self.kwargs['slug']
        try:
            kwargs['cart'] = self.request.session['cart']
        except:
            kwargs['cart'] = {}
        return kwargs

    def form_valid(self,form):
        extra_info = {
            'color': str(form.cleaned_data['color']),
            'talla': str(form.cleaned_data['talla'])
        }
        #extra_info=f"Color: {form.cleaned_data['color']}, Talla: {form.cleaned_data['talla']}, Tamaño: {form.cleaned_data['size']}"

        cart = self.request.session.get('cart', {})
        prod = f"{self.kwargs['slug']}{form.cleaned_data['color']}{form.cleaned_data['talla']}"

        cart[prod] = [self.kwargs['slug'],form.cleaned_data['cantidad'],extra_info]
        
        self.request.session['cart'] = cart
        messages.success(self.request, "Producto agregado al carrito con exito")
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))   

class VistaCarrito(CreateView):
    
    form_class= VentaForm
    template_name= "productos/carrito.html"
    
    def get_context_data(self, **kwargs):
        context = super(VistaCarrito,self).get_context_data(**kwargs)
        lista = []
        total = 0
        total1 = 0
        costo_envio = 9500
        try:
            if len(self.request.session['cart']) >=1:
                for x in self.request.session['cart']:
                    cantidad = self.request.session['cart'][x][1]
                    j = Producto.objects.get(slug=self.request.session['cart'][x][0])
                    extra_info = self.request.session['cart'][x][2]
                    identificador = x
                    subtotal = j.precio * cantidad
                    lista.append([j,cantidad,subtotal,extra_info,x])
                    total1 += subtotal
                
                p = Paginator(lista,5) 
                page_number = self.request.GET.get('page')
                page_obj = p.get_page(page_number)
                context["page_obj"] = page_obj
                # context["carrito"] = lista
                if total1 >250000:
                    context["descontado"] = costo_envio
                    costo_envio = 0
                total = total1 + costo_envio
                context["subtotal"] = total1
                context["costo_envio"] = costo_envio
                context["total"] = total
            else:
                raise Exception
            
        except:
            context["page_obj"] = lista
            # context["carrito"] = lista
            context["costo_envio"] = 0
            total = total1
            context["subtotal"] = total
            context["total"] = total
        
        tototal = self.request.session.get('total', {})
       # print(self.request.session['total'])
        tototal['total'] = total
        self.request.session['total'] = tototal
        
        #muestra de populares
        muestra_populares = list(Producto.objects.all().order_by('-visitas')[:10])
        populares = random.sample(muestra_populares,k=2)
        context["populares"] = populares
            
        return context
    
    def get_form_kwargs(self):
        kwargs = super(VistaCarrito, self).get_form_kwargs()
        try:
            kwargs['total'] = self.request.session['total']['total']
        except:
            kwargs['total'] = 0
        return kwargs

    def form_valid(self, form):

        if len(self.request.session["cart"])>0:
            
            venta = Venta.objects.create(
                fecha_venta = timezone.now(),
                valor_total = self.request.session['total']['total'],
                nombre = form.cleaned_data["nombre"],
                apellido = form.cleaned_data["apellido"],
                email = form.cleaned_data["email"],
                direccion = form.cleaned_data["direccion"],
                ciudad = form.cleaned_data["ciudad"],
                departamento = form.cleaned_data["departamento"],
                celular = form.cleaned_data["celular"],
                forma_pago = form.cleaned_data["forma_pago"],
            )
            
            if self.request.user.username:
                venta.user = self.request.user
                venta.save()
            
            lista = []
            for x in self.request.session['cart']:
                i = self.request.session['cart'][x][1]
                j = Producto.objects.get(slug=self.request.session['cart'][x][0])
                subtotal = j.precio *i
                extra_info = self.request.session['cart'][x][2]
                lista.append([j,i,subtotal,extra_info])
                    
            # for x,y in zip(productos,cantidades):
            #     subtotal = x.precio * y
            
            detalle_productos = []
            actualizar_productos = []
            for detalle in lista:
                detalle_venta = DetalleVenta(
                    producto = detalle[0],
                    venta = venta,
                    cantidad = detalle[1],
                    subtotal = detalle[2],
                    info_extra = f"Color: {detalle[3]['color']}, Talla: {detalle[3]['talla']}" 
                )
                detalle_productos.append(detalle_venta)
                
                producto = detalle[0]
                if producto in actualizar_productos:
                    i = actualizar_productos.index(producto)
                    print(actualizar_productos[i].cantidad)
                    actualizar_productos[i].cantidad = actualizar_productos[i].cantidad - detalle[1]
                else:   
                    producto.cantidad = producto.cantidad - detalle[1] 
                    actualizar_productos.append(producto)
            DetalleVenta.objects.bulk_create(detalle_productos)
            # actualizamos el stock
            Producto.objects.bulk_update(actualizar_productos, ['cantidad'])
            del self.request.session['cart']
            del self.request.session['total']
            
            messages.success(self.request, "Felicidades, la compra ha sido aprobada, en los proximos minutos te llegará un email de confirmación")
            
            return HttpResponseRedirect(
                    reverse('home_app:inicio'))
        else:
            return None
        
class BorrarDelCarrito(View):
    
    def post(self,request,*args,**kwargs):
        
        producto = self.kwargs["producto"]
        try:
            if producto == "BorrarTodo":
                del self.request.session['cart']
            else:
                self.request.session['cart'].pop(producto)
                self.request.session.modified = True
            return HttpResponseRedirect(
                reverse(
                    'productos_app:carrito'
                )
            )
        except:
            return HttpResponseRedirect(
                reverse(
                    'productos_app:carrito'
                )
            )
        
class FavoritoCreateView(LoginRequiredMixin,View):
    
    login_url = reverse_lazy('home_app:loginusuario')
    
    def post(self,request,*args,**kwargs):
        usuario = self.request.user
        producto = Producto.objects.get(id=self.kwargs['producto'])
        try:
            Favorito.objects.create(
                user = usuario,
                producto = producto,
            )
        except:
            Favorito.objects.get(
                user = usuario,
                producto = producto,
            ).delete()

        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

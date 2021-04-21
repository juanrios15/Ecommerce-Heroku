
from Apps.producto.models import CategoriaProducto, Favorito

def cant_carrito(request):
    try:
        cant_carrito = len(request.session["cart"])
    except:
        cant_carrito = 0
    
    return { 'cantidad_carrito': cant_carrito}

def categorias(request):
    categorias = CategoriaProducto.objects.values_list('nombre')[:10]
    
    return { 'categorias_nombres': categorias}

def favoritos(request):
    favoritos = Favorito.objects.filter(user__id = request.user.id).values_list('producto__id',flat=True)
    
    return { 'favoritos': favoritos}

def pagina_actual(request):
    actual = request.path
    
    return { 'pagina_actual': actual}
    
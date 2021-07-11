# rotar-ecommerce

* Aun no se han configurado los archivos media usando S3(Amazon), por lo que no es posible visualizar las imagenes que se guardan en media_url de django...

Enlace: https://morning-savannah-31438.herokuapp.com/

# rotar-ecommerce

### Proyecto Ecommerce para la empresa Rotar Ingeniería.
### Utilizando Django 3.1 con  Vistas basadas en clases (CBV)

El proyecto esta compuesto por 3 Apps:
- Home:       Manejo de usuarios y paginas basicas del proyecto
- Productos:  Modelo de Productos y Modelo de Venta y Detalle Venta para el carrito de compras
- Publicaciones: Modelo para publicaciones junto con modelo de comentarios

He creado el carrito de mercado sin necesidad de hacer un modelo para este, utilizando unicamente el requests.session de Django y su diccionario.


Home:
- Class AbstractUser para sobre escribir User de django y agregar un slug.
- Usuario activo puede agregar productos a su lista de favoritos, comentar publicaciones y modificar o eliminar su perfil.
- El usuario puede visualizar su lista de favoritos, comentarios y el historial de compras
- El usuario is_staff puede crear nuevas publicaciones y modificar las publicaciones de las que es dueño.
- Unicamente *superuser* puede administrar los productos y lo debe hacer desde admin.

Productos:
- Contiene los siguientes modelos: Producto, Color, Talla, CategoriaProducto, Favorito, FotoProducto, Venta, DetalleVenta
- Favorito tiene relación Unique Together entre Usuario y Producto
- El modelo de venta resume la venta, mientras que en DetalleVenta se describe la venta por cada producto.
- Se puede hacer busqueda de productos, filtro por categoria y ordenar por precio, popularidad o novedad.
- En la mayoria de las paginas es posible visualizar recomendaciones de productos, basadas en popularidad.

Carrito:
- request.session para almacenar la información en forma de diccionario y luego mostrarla en el view del carrito.
- En el dado caso que el cliente especifique un detalle como el color o talla, esta información extra tambien será almacenada.
- No es necesario crear un usuario para hacer uso del carrito.


Publicaciones:
- Si se cuenta con un usuario, se puede comentar las publicaciones y estos se podran ver en el detalle de esta.
- Al igual que con los productos, es posible realizar busqueda, filtro por etiquetas y ordenar por novedad o popularidad
- Usando formset inline y javascript se puede agregar mas fotografias al momento de crear una nueva publicación

#### Bootstrap 5. Para diseño responsivo Mobile First.


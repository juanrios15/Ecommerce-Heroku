from django import forms
from Apps.producto.models import Color, Producto, Talla, Venta



class CarritoForm(forms.Form):
    
    color = forms.ModelChoiceField(queryset=Color.objects.all(),required=False,widget=forms.RadioSelect)
    talla = forms.ModelChoiceField(queryset=Talla.objects.all(),required=False)
    talla.widget.attrs.update({'class': 'form-select'})
    
    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop('id', None)
        self.slug = kwargs.pop('slug', None)
        self.cart = kwargs.pop('cart', None)
        super(CarritoForm, self).__init__(*args, **kwargs) 
        self.fields['color'].queryset = Color.objects.filter(coloresproducto__id=self.id)
        self.fields['talla'].queryset = Talla.objects.filter(tallasproducto__id=self.id).order_by('talla')
        self.fields['talla'].empty_label = None
    
    cantidad = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(
            attrs = {
                'value': '1',
                'class': 'form-control',
            }
        )
    )
    
    # talla = forms.MultipleChoiceField(choices=Talla.objects.all(), required=False)
    # size = forms.MultipleChoiceField(choices=Size.objects.all(), required=False)
    
    
    #producto = forms.ForeignKey(Producto, verbose_name="Producto", on_delete=models.CASCADE, editable=False)
    
    def clean(self):
        cleaned_data =super(CarritoForm, self).clean()
        print(self.cart)
        producto = Producto.objects.get(id=self.id)
        cantidad = self.cleaned_data['cantidad']
        for x in self.cart:
            if producto.slug == self.cart[x][0]:
                cantidad+=self.cart[x][1]
                
        if cantidad>producto.cantidad:
            raise forms.ValidationError('Lo sentimos, no contamos con esa cantidad!')
        
        return self.cleaned_data

class VentaForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.total = kwargs.pop('total', None)
        super(VentaForm, self).__init__(*args, **kwargs) 
    
    class Meta:
        model = Venta
        fields= ('nombre','apellido','direccion','email','ciudad','departamento','celular','forma_pago',)
    
    
    def clean(self):
        cleaned_data =super(VentaForm, self).clean()
        
        if self.total < 25000:
            raise forms.ValidationError('Aceptamos compras minimo de $25.000, lo sentimos')
        return self.cleaned_data
from django import forms
from Apps.publicaciones.models import Foto, Publicacion
from django.forms.models import inlineformset_factory
from ckeditor.fields import RichTextFormField

class NewPostForm(forms.ModelForm):
    
    descripcion = RichTextFormField(config_name="refault")
    
    class Meta:
        model = Publicacion
        fields = ('titulo','resumen','etiquetas','descripcion','imagen','publico',)
        widgets = {
            'titulo': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'resumen': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'imagen': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'publico': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
            'etiquetas': forms.SelectMultiple(
                attrs={
                    'class': 'form-select',
                    'size': 6
                }
            ),            
        }


PostFormSet = inlineformset_factory(
        Publicacion, 
        Foto, 
        fields=('imagen',),
        can_delete=False, 
        max_num=5,
        widgets= {
            'imagen': forms.FileInput(
                attrs={
                        'class': 'form-control'
                    }
                )
            }
    )
    
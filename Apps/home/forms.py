from django import forms

from .models import Perfil
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.forms import UserCreationForm
from ckeditor.fields import RichTextFormField, CKEditorWidget


#Formularios para actualizar perfil y usuario al tiempo
class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields= ('first_name','last_name','email',)
        widgets= {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }
        

class ProfileForm(forms.ModelForm):
    
    bio = RichTextFormField(config_name="refault")
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs) 
        self.fields['departamento'].empty_label = None
    
    class Meta:    
        
        model = Perfil
        fields= ('cargo','bio','departamento','foto','linkedin')
        
        widgets= {
            'cargo': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'departamento': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
            'foto': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'linkedin': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'https://www.linkedin.com/in/usuario123/'
                }
            )
            
        }
    

#Crear usuario
class UserCreateForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
    
    username = forms.CharField(
            label='Username',
            required=True,
            widget=forms.TextInput(
                attrs={
                    'class': "form-control",
                }
            )
        )
    email = forms.EmailField(
            label='Email',
            required=True,
            widget=forms.EmailInput(
                attrs={
                    'class': "form-control",
                }
            )
        )
    class Meta:
        model = User
        fields = ("username","email")
    
    
    # def save(self, commit=True):
    #     user = super().save(commit=False)
         
    #     user.set_password(self.cleaned_data["password1"])
    #     user.is_active = False
    #     if commit:
    #         user.save()
    #     return user
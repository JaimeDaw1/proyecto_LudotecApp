from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms

class Login(AuthenticationForm):
    error_messages = {
        'invalid_login': 'Por favor, ingresa un nombre de usuario y contraseña correctos'
    }

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Usuario')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)
    first_name = forms.CharField(label='Nombre')
    last_name = forms.CharField(label='Apellidos')
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
                self.fields[field].widget.attrs.update({'class': 'form-control'})  #Con estas últimas lineas sobreescribimos el init de la superclase(UserCreationForm)
                

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Nombre de usuario", widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = Userfields = ('username', 'password')
       
    
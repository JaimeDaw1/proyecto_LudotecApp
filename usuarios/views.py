from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import LoginUserForm, RegisterUserForm


def login_user(request):
    if request.method == 'POST':      
       form = LoginUserForm(request, request.POST)
       if form.is_valid():
            user = form.get_user()
            login(request, user)
            # return redirect('home')
            next = request.GET.get('next', 'home') #Esto hace que se pueda redirigir a home ya sea despues de hacer login normal, o despues de hacer login al querer primero crear un formulario
            messages.success(request, f'Hola {user}')
            return redirect(next)
        
       else:
            messages.warning(request, 'Usuario o contraseña incorrectos. Prueba otra vez')
            return redirect('login')
                  
    else:
        if 'next' in request.GET:
            messages.warning(request, 'Inicia sesión o regístrate antes de acceder a esa página') #Con este if mostramos el mensaje si el usuario intenta acceder a crear enquisa o crear opcion sin estar antes logueado. El next es la comprobación, porque al querer acceder a crear enquisa o crear opcion sin estar logueado, en la URL aparece "next"
        form = LoginUserForm()
        
    return render(request, 'usuarios/login.html', {'form': form})


def logout_user(request):  
    logout(request)
    messages.success(request, 'Hasta pronto')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guardar el usuario
            login(request, user)  # Autenticar al usuario
            messages.success(request, f'Bienvenido {user.username}')
            return redirect('home')
        else:
            # Mensaje que se muestra si hubo algún error al validar el formulario
            messages.warning(request, 'Hubo un error al registrar el usuario. Por favor, inténtalo de nuevo.')
            return redirect('register_user')
    else:
        form = RegisterUserForm()
    return render(request, 'usuarios/register_user.html', {'form': form})
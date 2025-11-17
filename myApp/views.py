from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import ReservaForm
from .models import Reserva

def welcome(request):
    return render(request, 'welcome.html')

def redirect_gruop(user):
    if user.is_superuser:
        return redirect('admin')
    else:
        return redirect('main')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect_gruop(user)
        messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, "login.html")

def logout_view(request):
    """Cierra sesión y vuelve a welcome."""
    auth_logout(request)
    return redirect(request, "welcome")

@login_required
def main(request):
    return render(request, "main.html")

@login_required
def admin_view(request):
    if not request.user.is_superuser:
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return redirect("welcome")
    return render(request,'admin_dashboard.html') 

@login_required
def formulario(request):
    context = {}
    
    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('formulario')
        else:
            context['errores'] = form.errors
            context['form'] = form  # Mantenemos el formulario con los datos ingresados
    else:
        context['form'] = ReservaForm()  #
    
    return render(request, "formulario.html", context)
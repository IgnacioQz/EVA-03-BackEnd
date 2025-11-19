from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReservaForm
from .models import Reserva,Sala

def main(request):
    # Limpia reservas vencidas antes de mostrar la página
    Sala.limpiar_reservas_vencidas()

    salas = Sala.objects.all()
    reservas = Reserva.objects.all()
    context = {}

    context['salas'] = salas
    context['reservas'] = reservas

    return render(request, "main.html", context)


def formulario(request):
    context = {}

    # Limpia reservas vencidas antes de mostrar la página
    Sala.limpiar_reservas_vencidas()
    
    if request.method == "POST":
        form = ReservaForm(request.POST)

        # Verifica si los datos son válidos
        if form.is_valid():
            form.save()
            return redirect('main')
        else:
            context['form'] = form  # Devuelve el formulario con errores
    else:
        context['form'] = ReservaForm()  
    
    return render(request, "formulario.html", context)

def detalleSala(request,id):
    context = {}

    sala = Sala.objects.get(id = id)  
    reservas = Reserva.objects.all()  
    context["reservas"] = reservas
    context["sala"] = sala
    
    return render(request,"detalle.html", context)

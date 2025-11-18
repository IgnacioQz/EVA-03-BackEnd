from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReservaForm
from .models import Reserva,Sala

def main(request):
    Sala.limpiar_reservas_vencidas()
    salas = Sala.objects.all()
    reservas = Reserva.objects.all()
    context = {}

    context['salas'] = salas
    context['reservas'] = reservas

    return render(request, "main.html", context)


def formulario(request):
    context = {}
    eliminadas = Sala.limpiar_reservas_vencidas()

    if eliminadas > 0:
        messages.success(request, f"Se limpiaron {eliminadas} reserva(s) vencida(s)")
    
    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Reserva creada exitosamente!")
            return redirect('main')
        else:
            context['form'] = form  # Mantenemos el formulario con los datos ingresados
    else:
        context['form'] = ReservaForm()  # Creamos nuevo formulario
    
    return render(request, "formulario.html", context)

def detalleSala(request,id):
    context = {}
    sala = Sala.objects.get(id = id)  
    reservas = Reserva.objects.all()  
    context["reservas"] = reservas
    context["sala"] = sala
    return render(request,"detalle.html", context)

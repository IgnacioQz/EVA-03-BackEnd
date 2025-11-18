from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReservaForm
from .models import Reserva,Sala

def main(request):
    Sala.limpiar_reservas_vencidas()
    return render(request, "main.html")


def formulario(request):
    eliminadas = Sala.limpiar_reservas_vencidas()

    if eliminadas > 0:
        messages.success(request, f"Se limpiaron {eliminadas} reserva(s) vencida(s)")

    context = {}
    
    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Reserva creada exitosamente!")
            return redirect('main')
        else:
            context['form'] = form  # Mantenemos el formulario con los datos ingresados
    else:
        context['form'] = ReservaForm()  #
    
    return render(request, "formulario.html", context)
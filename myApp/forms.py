from django import forms   
from .models import Reserva
from datetime import timedelta
from django.utils import timezone

class ReservaForm(forms.ModelForm):
    class Meta: 
        model = Reserva
        fields = ['rut_persona','sala','personas']
        widgets = {
            'rut_persona': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12345678-9'
            }),
            'sala': forms.Select(attrs={'class': 'form-control'}),
            'personas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            })
        }

    def save(self, commit=True):
        reserva = super().save(commit=False)
        #Fecha y hora de inicio 
        ahora = timezone.now()
        reserva.fecha_reserva = ahora.date()
        reserva.hora_inicio = ahora.time() 
        #hora de termino: 2 horas
        hora_termino = ahora + timedelta(hours=2)
        reserva.hora_fin = hora_termino.time()
        if commit:
            reserva.save()
        return reserva

            

    
        
        
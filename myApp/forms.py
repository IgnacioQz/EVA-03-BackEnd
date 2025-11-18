from django import forms   
from .models import Reserva
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError

class ReservaForm(forms.ModelForm):
    class Meta: 
        model = Reserva
        fields = ['rut_persona', 'sala', 'personas']
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
    
    def clean(self):
        cleaned_data = super().clean()
        sala = cleaned_data.get('sala')
        personas = cleaned_data.get('personas')
    
        if sala and personas:
            # Validar capacidad
            if personas > sala.capacidad:
                self.add_error('personas', f"El número de personas ({personas}) excede la capacidad de la sala ({sala.capacidad}).")
            
            # Calcular fecha/hora que se usarán al guardar
            ahora = timezone.localtime(timezone.now())
            fecha_hora_inicio = ahora
            fecha_hora_fin = ahora + timedelta(hours=2)
            
            # Validar disponibilidad de la sala
            if not sala.disponibilidad(fecha_hora_inicio, fecha_hora_fin):
                self.add_error('sala', "La sala no está disponible en este momento. Ya existe una reserva activa.")
        
        return cleaned_data
    
    def save(self, commit=True):
        reserva = super().save(commit=False)
        
        # Fecha/hora de inicio (hora actual de Chile)
        ahora = timezone.localtime(timezone.now())
        reserva.fecha_hora_inicio = ahora
        
        # Fecha/hora de término: 2 horas después
        reserva.fecha_hora_fin = ahora + timedelta(hours=2)
        
        if commit:
            reserva.save()
        
        return reserva
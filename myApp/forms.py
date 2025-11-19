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
    
    def clean_personas(self):
        #Validación del campo personas
        personas = self.cleaned_data.get('personas')
        if personas and personas < 1:
            raise ValidationError("Debe haber al menos 1 persona en la reserva.")
        return personas
    
    def clean(self):
        #Validación global del formulario
        cleaned_data = super().clean()
        sala = cleaned_data.get('sala')
        personas = cleaned_data.get('personas')
        
        # validar si tenemos sala y personas sin errores previos
        if not sala or not personas:
            return cleaned_data
        
        # Validar capacidad
        if personas > sala.capacidad:
            raise ValidationError({
                'personas': f"El número de personas ({personas}) excede la capacidad de la sala ({sala.capacidad})."
            })
        
        # Calcular horario
        ahora = timezone.localtime(timezone.now()).replace(second=0, microsecond=0)
        fecha_hora_inicio = ahora
        fecha_hora_fin = ahora + timedelta(hours=2)
        
        # Validar disponibilidad
        if not sala.verificar_disponibilidad(fecha_hora_inicio, fecha_hora_fin):
            raise ValidationError({
                'sala': "La sala no está disponible en este momento. Ya existe una reserva activa."
            })
        
        return cleaned_data
    
    def save(self, commit=True):
        #Guardar la reserva con fechas automáticas
        reserva = super().save(commit=False)
        
        # Asignar fechas
        ahora = timezone.localtime(timezone.now()).replace(second=0, microsecond=0)
        reserva.fecha_hora_inicio = ahora
        reserva.fecha_hora_fin = ahora + timedelta(hours=2)
        
        if commit:
            reserva.save()
        
        return reserva
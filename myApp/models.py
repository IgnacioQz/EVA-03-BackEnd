from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# Modelo para sala 
class Sala(models.Model):
    nombre = models.CharField(max_length=100)
    capacidad = models.IntegerField()

    def __str__(self):
        return self.nombre
    
    def disponibilidad(self, fecha_hora_inicio, fecha_hora_fin, reserva_actual=None):
        # Buscar reservas que se solapen con el rango solicitado
        reservas = Reserva.objects.filter(sala=self)
        
        if reserva_actual:
            reservas = reservas.exclude(id=reserva_actual.id)
        
        for reserva in reservas:
            # Verificar solapamiento
            if (fecha_hora_inicio < reserva.fecha_hora_fin and 
                fecha_hora_fin > reserva.fecha_hora_inicio):
                return False
        
        return True
    
    class Meta:
        verbose_name = "Sala"
        verbose_name_plural = "Salas"


# Modelo para Reservación
class Reserva(models.Model):
    rut_persona = models.CharField(max_length=12)
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField()
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    personas = models.IntegerField(default=1)

    def __str__(self):
        return f"Reserva de {self.rut_persona} en {self.sala.nombre} el {self.fecha_hora_inicio.strftime('%d/%m/%Y %H:%M')}"
    
    def clean(self):
        # Validación: la fecha/hora de inicio debe ser anterior a la de fin
        if self.fecha_hora_inicio and self.fecha_hora_fin:
            if self.fecha_hora_inicio >= self.fecha_hora_fin:
                raise ValidationError("La fecha/hora de inicio debe ser anterior a la de fin.")
        
        # Validación: la fecha de reserva no debe ser en el pasado
        if self.fecha_hora_inicio:
            if self.fecha_hora_inicio < timezone.now():
                raise ValidationError("La fecha/hora de reserva no puede ser en el pasado.")
        
        # Validación: el número de personas no puede exceder la capacidad de la sala
        if self.sala and self.personas:
            if self.personas > self.sala.capacidad:
                raise ValidationError(
                    f"El número de personas ({self.personas}) excede la capacidad de la sala ({self.sala.capacidad})."
                )
        
        # Validación: el número de personas debe ser al menos 1
        if self.personas and self.personas < 1:
            raise ValidationError("Debe haber al menos 1 persona en la reserva.")
        
        # Validación: la sala debe estar disponible en el horario seleccionado
        if self.sala and self.fecha_hora_inicio and self.fecha_hora_fin:
            if not self.sala.disponibilidad(
                self.fecha_hora_inicio, 
                self.fecha_hora_fin, 
                reserva_actual=self
            ):
                raise ValidationError("La sala no está disponible en el horario seleccionado.")
    
    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-fecha_hora_inicio']
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

#modelo para sala 

class Sala(models.Model):
    nombre = models.CharField(max_length=100)
    capacidad = models.IntegerField()

    def __str__(self):
        return self.nombre
    
    def disponibilidad(self, fecha, hora_inicio, hora_fin, reserva_actual=None):
        reservas = Reserva.objects.filter(sala=self, fecha_reserva=fecha)
        if reserva_actual:
            reservas = reservas.exclude(id=reserva_actual.id) # Excluir la reserva actual al verificar disponibilidad
        for reserva in reservas:
            if (hora_inicio < reserva.hora_fin and hora_fin > reserva.hora_inicio):
                return False
        return True
    
    class Meta:
        verbose_name = "Sala"
        verbose_name_plural = "Salas"
    
    

#modelo para Reservacion
class Reserva(models.Model):
    rut_persona = models.CharField(max_length=12)
    fecha_reserva = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE) #relacion con sala
    personas = models.IntegerField(default=1)

    def __str__(self):
        return f"Reserva de {self.rut_persona} en {self.sala.nombre} el {self.fecha_reserva}"
    
    def clean(self):
        # Validacion: la hora de inicio debe ser anterior a la hora de fin
        if self.hora_inicio >= self.hora_fin:
            raise ValidationError("La hora de inicio debe ser anterior a la hora de fin.")
        
        # Validacion: la  fecha de reserva no debe ser en el pasado
        if self.fecha_reserva < timezone.now().date():
            raise ValidationError("La fecha de reserva no puede ser en el pasado.")
        
        # Validacion: la cantidad de personas no debe exceder la capacidad de la sala
        if self.sala and self.personas > self.sala.capacidad:
            raise ValidationError("La cantidad de personas excede la capacidad de la sala.")
        
        #validacion: la cantidad de personas debe ser al menos 1
        if self.personas < 1:
            raise ValidationError("La cantidad de personas debe ser al menos 1.")
        
        # Validacion: la sala debe estar disponible en el horario seleccionado
        if self.sala and self.fecha_reserva and self.hora_inicio and self.hora_fin: 
            if not self.sala.disponibilidad( 
                self.fecha_reserva, 
                self.hora_inicio, 
                self.hora_fin, 
                reserva_actual=self
                ):
                raise ValidationError("La sala no está disponible en el horario seleccionado.")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-fecha_reserva', 'hora_inicio']
        



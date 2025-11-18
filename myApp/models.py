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
        try:
            sala_nombre = self.sala.nombre if self.sala else "Sin sala"
            fecha_str = self.fecha_hora_inicio.strftime('%d/%m/%Y %H:%M') if self.fecha_hora_inicio else "Sin fecha"
            return f"Reserva de {self.rut_persona} en {sala_nombre} el {fecha_str}"
        except Exception:
            return f"Reserva #{self.id if self.id else 'nueva'}"
    
    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-fecha_hora_inicio']
from django.db import models
from django.utils import timezone

class Sala(models.Model):
    nombre = models.CharField(max_length=100)
    capacidad = models.IntegerField()
    sala_disponible = models.BooleanField(default= True)

    def __str__(self):
        return self.nombre
    
    @staticmethod
    def limpiar_reservas_vencidas():
        ahora = timezone.now()
        # Busca reservas que ya terminaron
        reservas_vencidas = Reserva.objects.filter(fecha_hora_fin__lt=ahora)

        #Salas a eliminar
        salas_vencidas = set(reservas_vencidas.values_list('sala_id', flat=True))
        
        #Eliminar reservas vencidas
        count = reservas_vencidas.count()
        reservas_vencidas.delete()
        
        #Actualizar disponibilidad de salas
        for sala_id in salas_vencidas:
            try: 
                sala= Sala.objects.get(id=sala_id)
                sala.actualizar_disponibilidad()
            except Sala.DoesNotExist:
                pass

        return count
    
    def actualizar_disponibilidad(self):
        ahora = timezone.now()

        #Verificar reservas activas
        reserva_activa = Reserva.objects.filter(
            sala = self,
            fecha_hora_inicio__lte = ahora,
            fecha_hora_fin__gt = ahora
        ).exists()

        # Si hay reserva activa, la sala está ocupada
        self.sala_disponible = not reserva_activa
        self.save(update_fields=['sala_disponible'])
    
    def verificar_disponibilidad(self, fecha_hora_inicio, fecha_hora_fin, reserva_actual=None):
        #Limpiar reservas vencidas antes de consultar disponibilidad
        Sala.limpiar_reservas_vencidas()
        
        # Obtiene reservas de esta sala
        reservas = Reserva.objects.filter(sala=self)
        
        if reserva_actual and reserva_actual.id:
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
        
    def save(self, *args, **kwargs):
        super().save(*args,**kwargs)

        # Actualizar disponibilidad de la sala después de guardar
        if self.sala:
            self.sala.actualizar_disponibilidad()

    def delete(self, *args, **kwargs):
        sala = self.sala
        super().delete(*args,**kwargs)

        # Actualizar disponibilidad de la sala después de guardar
        if sala:
            sala.actualizar_disponibilidad()
    
    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-fecha_hora_inicio']
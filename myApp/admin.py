from django.contrib import admin
from .models import Sala, Reserva

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'capacidad')
    search_fields = ('nombre',)

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('rut_persona', 'sala', 'fecha_reserva', 'hora_inicio', 'hora_fin', 'personas')
    list_filter = ('sala', 'fecha_reserva')
    search_fields = ('rut_persona',)
    ordering = ('-fecha_reserva', 'hora_inicio')

admin.site.site_header = "Administración de Reservas de Salas"
admin.site.site_title = "Admin Reservas Salas"
admin.site.index_title = "Panel de Administración"
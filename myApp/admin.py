from django.contrib import admin
from .models import Sala, Reserva

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'capacidad', 'sala_disponible')
    search_fields = ('nombre',)

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['rut_persona', 'sala', 'fecha_hora_inicio', 'fecha_hora_fin', 'personas']
    list_filter = ('sala', 'fecha_hora_inicio')
    search_fields = ('rut_persona',)
    ordering = ['fecha_hora_inicio']
    date_hierarchy = 'fecha_hora_inicio'

from django.contrib import admin
from .models import Sala, Reserva

admin.site.site_header = "Administración de Reservas de Salas"
admin.site.site_title = "Admin Reservas Salas"
admin.site.index_title = "Panel de Administración"
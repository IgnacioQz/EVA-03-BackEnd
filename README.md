📘 README – Sistema de Reservas de Salas (Django)
Descripción

Proyecto correspondiente a la Evaluación Sumativa 3 de Programación Back End.
La aplicación permite gestionar salas de estudio del ITID y realizar reservas con duración máxima de 2 horas, usando Django y una Base de Datos externa.

Funcionalidades

Gestión de salas (Admin): crear, editar, eliminar, habilitar y visualizar salas.

Página principal: listar salas y mostrar disponibilidad.

Detalle de sala: si está reservada, muestra hora de inicio y término.

Reservas: formulario con ModelForm, registro automático de inicio y fin (+2 horas), verificación de disponibilidad.

Detalles Técnicos

Uso de Base de Datos externa.

Manejo de credenciales con django-environ.

Panel de administración habilitado.

Validación de que la sala queda disponible al modificar la hora de término.

Seguridad

El repositorio no incluye archivos sensibles:
venv/, **pycache**/, .env, db.sqlite3, ni credenciales.

Demostración Esperada

El proyecto debe mostrar:

CRUD de salas y su reflejo en la BD

Visualización de salas en la página principal

Creación de reservas y registro en la BD

Cambio de hora de término para verificar disponibilidad automática

# coding=utf-8

from django.contrib import admin

from ..models import Materia


@admin.register(Materia)
class Materia(admin.ModelAdmin):
    """
    Especificación de la representación de Area en la interfaz de administración.
    """
    list_display = (
        'nombre',
        'codigo',
    )

    list_filter = (
        'especialidad',
        'plan',
    )
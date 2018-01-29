# coding=utf-8

import json

from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from ..adapters.google_calendar import generar_lista_eventos


def obtener_codigo_aleatorio():
    random = get_random_string().upper()
    while Recurso.objects.filter(codigo=random).exists():
        random = get_random_string().upper()
    return random


class Recurso(models.Model):
    # Atributos
    calendar_codigo = models.CharField(
        max_length=100,
        verbose_name='ID del calendario',
        help_text='Puede conocerse al acceder a los detalles del calendario en Google Calendar. '
                  'Su formato habitual es: "identificador@group.calendar.google.com". '
                  'Por ejemplo, un valor válido es: '
                  '"pi4pfu4alasbojtd1v1bj32oc0@group.calendar.google.com".',
    )
    calendar_color = models.CharField(
        max_length=10,
        blank=True,
        verbose_name='Color del calendario',
        help_text='Color con el que se visualizan los eventos del calendario. '
                  'Debe estar en formato hexadecimal. Por ejemplo, un valor válido es: '
                  '"#ff8c0a"',
    )

    activo = models.BooleanField(default=True)

    codigo = models.CharField(max_length=12, unique=True, default=obtener_codigo_aleatorio)

    class Meta:
        """
        Información de la clase.
        """
        app_label = 'app_reservas'
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'

    def __str__(self):
        """
        Representación de la instancia.
        """
        return '{0!s}'.format(self.get_nombre_corto())

    # Método sobreescrito para el guardado de una instancia.
    def save(self, *args, **kwargs):
        # Guarda la instancia actual.
        super(Recurso, self).save(*args, **kwargs)
        # Encola la tarea de Celery para la obtención de los eventos de la instancia.
        from ..tasks import obtener_eventos_recurso_especifico
        obtener_eventos_recurso_especifico.delay(self)

    def get_nombre_corto(self):
        """
        Retorna el nombre corto de la instancia.
        """
        return 'Recurso: {0:d}'.format(self.id)

    def get_eventos(self):
        return generar_lista_eventos(self.calendar_codigo)

    def get_eventos_json(self):
        eventos = self.get_eventos()
        eventos_json = '['
        primera_iteracion = True
        for evento in eventos:
            if primera_iteracion:
                primera_iteracion = False
            else:
                eventos_json += ',\n'
            evento_str = json.dumps({
                'title': evento['titulo'],
                'start': evento['inicio_str'],
                'end': evento['fin_str'],
                'resourceId': str(self.id)
            })
            eventos_json += evento_str
        eventos_json += ']'
        return eventos_json

    def get_nearby_reservations(self):
        from app_reservas.models import Reserva
        reserva_qs = Reserva.objects.filter(
                 recurso__id=self.id,
                 historicoestadoreserva__estado='1',
                 historicoestadoreserva__fechaFin__isnull=True,
                 # horarioreserva__dia=timezone.now().weekday()
             )
        inicio = timezone.localtime(timezone.now()) - timezone.timedelta(minutes=10)
        fin = timezone.localtime(timezone.now()) + timezone.timedelta(minutes=100)
        neaby_reservation = []
        #for reserva in reserva_qs:
        #    horario_obj = reserva.horarioreserva_set.get(dia=timezone.now().weekday())
        #    if horario_obj.inicio > inicio.time() or horario_obj.inicio < fin.time():
        #        neaby_reservation.append(reserva)
        return reserva_qs

    def get_active_reservations(self):
        from app_reservas.models import Reserva
        reservas_qs = Reserva.objects.filter(
            recurso__id=self.id,
            historicoestadoreserva__estado='1',
            historicoestadoreserva__fechaFin__isnull=True
        )
        return reservas_qs

    def get_active_loan(self):
        prestamos = self.prestamos_all.filter(prestamo__fin__isnull=True)[:1]
        if prestamos:
            return prestamos[0].prestamo
        return None

# coding=utf-8

from django.db import models


class Cuerpo(models.Model):
    # Atributos
    numero = models.PositiveSmallIntegerField()

    # Representación del objeto
    def __str__(self):
        return '{0!s}'.format(self.get_nombre_corto())

    def get_nombre_corto(self):
        return 'Cuerpo {0:d}'.format(self.numero)

    def get_niveles(self):
        return self.nivel_set.order_by('numero')

    # Información de la clase
    class Meta:
        app_label = 'app_reservas'
        ordering = ['numero']
        verbose_name = 'Cuerpo'
        verbose_name_plural = 'Cuerpos'
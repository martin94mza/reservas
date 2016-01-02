from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.index,
        name='index'
    ),
    url(
        r'^cuerpo_(?P<num_cuerpo>[0-9]+)/$',
        views.cuerpo_detalle,
        name='cuerpo_detalle'
    ),
    url(
        r'^cuerpo_(?P<num_cuerpo>[0-9]+)/nivel_(?P<num_nivel>-?[0-9]+)/$',
        views.nivel_detalle,
        name='nivel_detalle'
    ),
    url(
        r'^aula/(?P<aula_id>[0-9]+)/$',
        views.aula_detalle,
        name='aula_detalle'
    ),
    url(
        r'^area/(?P<slug_area>[A-Za-z0-9]+)/$',
        views.area_detalle,
        name='area_detalle'
    ),
    url(
        r'^recurso/(?P<recurso_id>[0-9]+)/eventos/$',
        views.recurso_eventos_json,
        name='recurso_eventos_json'
    ),
    url(
        r'^laboratorio_informatico/$',
        views.laboratorio_informatico_listado,
        name='laboratorio_informatico_listado'
    ),
    url(
        r'^laboratorio_informatico/(?P<alias_laboratorio>[A-Za-z0-9]+)/$',
        views.laboratorio_informatico_detalle,
        name='laboratorio_informatico_detalle'
    ),
    url(
        r'^solicitud/aula/$',
        views.solicitud_aula,
        name='solicitud_aula'
    ),
    url(
        r'^solicitud/laboratorio_informatico/$',
        views.solicitud_laboratorio_informatico,
        name='solicitud_laboratorio_informatico'
    ),
]

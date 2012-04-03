from django.conf.urls.defaults import *
from django.views.generic import TemplateView, ListView
from biblioteca.forms import *
from biblioteca.models import *

urlpatterns = patterns('biblioteca.views',
    url(r'^test-404$', TemplateView.as_view(template_name="404.html")),

    url(r'^$',          'home'),
    url(r'^ricerca_r$', 'ricerca.ricerca_rapida'),
    url(r'^ricerca$',	'ricerca.ricerca_avanzata'),

    url(r'^edizioni$',                          ListView.as_view(
                                                    queryset=Edizione.objects.order_by('titolo'))),
    url(r'^edizioni/(?P<pk>\d+)$',              'edizione.dettagli'),
    url(r'^edizioni/(?P<pk>\d+)/modifica$',     'edizione.modifica'),
    url(r'^edizioni/(?P<pk>\d+)/elimina$',      'edizione.elimina'),
    url(r'^edizioni/aggiungi$',                 'edizione.aggiungi'),
    url(r'^edizioni/aggiungi/googlebooks',      TemplateView.as_view(
                                                    template_name='biblioteca/googlebooks_import.html')),


    url(r'^copie/(?P<pk>\d+)/\+prestiti$',              'prestiti.copia'),
    url(r'^copie/(?P<pk>\d+)/\+prestiti/aggiungi$',     'prestiti.aggiungi'),

    url(r'^prestiti$',                                  'prestiti.lista'),
    url(r'^prestiti/(?P<pk>\d+)$',                      'prestiti.dettagli'),
    url(r'^prestiti/(?P<pk>\d+)/modifica$',             'prestiti.modifica'),
    url(r'^prestiti/(?P<pk>\d+)/restituisci$',          'prestiti.restituisci'),

    url(r'^armadi$',                            'armadio'),
    url(r'^armadi/(?P<nome_armadio>[\w\d]+)$',  'armadio'),


)



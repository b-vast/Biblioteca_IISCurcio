
from django.template  import RequestContext
from django.shortcuts import render_to_response
#from django.db        import QuerySet

from biblioteca.search import edizioni_advanced_search, edizioni_simple_search

def ricerca(search_callback, template, request):

    params = request.GET.copy()
    for key, value in params.iteritems():
	if value == '':
	    del params[key]

    queryset = None
    if len(params) > 0:
	queryset = search_callback(params)

    count = 0
    if type(queryset) is 'QuerySet': count = queryset.count()
    elif type(queryset) is list:     count = len(queryset)

    context_data = {
	'done' : (queryset != None),
	'results': queryset,
	'params': params
    }
    if params.has_key('q'):
	context_data['query'] = params['q']

    return render_to_response(template, context_data,
			      context_instance=RequestContext(request))

def ricerca_avanzata(request):
    return ricerca(edizioni_advanced_search, 
		   "biblioteca/ricerca_avanzata.html",
		   request)

def ricerca_rapida(request):
    return ricerca(edizioni_simple_search, 
		   "biblioteca/ricerca_rapida.html",
		   request)


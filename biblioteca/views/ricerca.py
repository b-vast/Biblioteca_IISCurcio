
from django.template  import RequestContext
from django.shortcuts import render_to_response

from biblioteca.search import search

def ricerca(request):

    if len(request.GET) > 0:
        context_data =  { 'results': search(request.GET) }
        if request.GET.has_key('q'):
            context_data['query'] = request.GET['q']
    else:
        context_data = {}

    return render_to_response("biblioteca/ricerca.html", context_data,
            context_instance=RequestContext(request))


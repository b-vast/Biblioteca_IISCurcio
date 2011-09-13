
from django.shortcuts import render_to_response

from biblioteca.search import search

def ricerca(request):

    if request.GET.has_key('q'):
        context_data =  { 'results': search(request.GET)
                        , 'query': request.GET['q']
                        }
    elif request.GET.has_key('adv'):
        context_data = {}
    else:
        context_data = {}

    return render_to_response("biblioteca/ricerca.html", context_data)


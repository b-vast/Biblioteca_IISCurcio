
from django.db.models import Q
from biblioteca.models import *

### TODO: Use full-text search 

def prestiti_simple_search(query, solo_non_restituiti=True):
    words = query.split()

    results = {}

    queryset = Prestito.objects
    if solo_non_restituiti:
        queryset = queryset.filter(datarestituzione__isnull=True)
    for word in words:
        q = Q()
        for field in '''nome cognome categoria classe
                        nomeresp cognomeresp note
                        copia__edizione__titolo
                        copia__edizione__casaeditrice
                        copia__edizione__autore__nome
                        copia__edizione__autore__cognome
                     '''.split():
            kwargs = { field+'__icontains' : word }
            q = q | Q(**kwargs)
        queryset = queryset.filter(q)

    return queryset

def prestiti_search(params):
    assert params.has_key('query'), \
        'missing parameter "query"' # TODO replace with advanced search
    solo_non_restituiti = not params.get('restituiti', False)
    return prestiti_simple_search(params['query'], solo_non_restituiti)

def edizioni_simple_search(query):
    words = query.split()

    results = {}

    for word in words:
        for field in ['titolo', 'casaeditrice', 'anno', 'isbn',
                        'autore__nome', 'autore__cognome']:
            kwargs = { field+'__icontains' : word }
            edizioni = Edizione.objects.filter(**kwargs)
            for e in edizioni:
                if not results.has_key(e.id):
                    results[e.id] = 1
                else:
                    results[e.id] += 1

    results = results.items()
    results.sort(cmp=lambda a, b: cmp(b[1], a[1]))
    return [ Edizione.objects.get(pk=id) for id, score in results ]

def edizioni_advanced_search(params):

    results = {}

    for field in ['titolo', 'casaeditrice', 'anno', 'isbn',
                    'autore__nome', 'autore__cognome']:
        if not params.has_key(field): continue

        for word in params[field].split():
            kwargs = { field+'__icontains' : params[field] }
            edizioni = Edizione.objects.filter(**kwargs)
            for e in edizioni:
                if not results.has_key(e.id):
                    results[e.id] = 1
                else:
                    results[e.id] += 1

    results = results.items()
    results.sort(cmp=lambda a, b: cmp(b[1], a[1]))
    return [ Edizione.objects.get(pk=id) for id, score in results ]


def search(params):
    if params.has_key('q'):
        return edizioni_simple_search(params['q'])
    else:
        return edizioni_advanced_search(params)



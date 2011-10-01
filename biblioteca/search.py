
from django.db.models import Q
from biblioteca.models import *

### TODO: Use full-text search 

def prestiti_simple_search(query, solo_non_restituiti):
    words = query.split()

    results = {}

    for word in words:
        for field in '''nome cognome categoria classe
                        nomeresp cognomeresp note
                        copia__edizione__titolo
                        copia__edizione__casaeditrice
                        copia__edizione__autore__nome
                        copia__edizione__autore__cognome
                     '''.split():
            kwargs = { field+'__icontains' : word }
            if solo_non_restituiti:
                kwargs['datarestituzione__isnull'] = True
            prestiti = Prestito.objects.filter(**kwargs)
            for p in prestiti:
                if not results.has_key(p.id):
                    results[p.id] = 1
                else:
                    results[p.id] += 1

    results = results.items()
    results.sort(cmp=lambda a, b: cmp(b[1], a[1]))
    return [ Prestito.objects.get(pk=id) for id, score in results ]

def prestiti_search(params):
    if params.has_key('q'):
        solo_non_restituiti = not params.get('old', False)
        return prestiti_simple_search(params['q'], solo_non_restituiti)
    else:
        raise ValueError('missing parameter "q"') # TODO replace with advanced search

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



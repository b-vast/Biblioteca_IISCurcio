
from django.db.models import Q
from biblioteca.models import *

### TODO: Use full-text search

def simple_search(query):
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

def advanced_search(params):

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
        return simple_search(params['q'])
    else:
        return advanced_search(params)


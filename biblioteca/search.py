
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

def edizioni_simple_search(params):
    if not params.has_key('q'): return None

    words = params['q'].split()

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

    keys = ['titolo',   'casaeditrice',
	    'anno',	'isbn',
	    'autori',   'armadio', 
	    'scaffale', 'posizione']

    not_specified = 0
    query = Edizione.objects.all()

    for key in keys:
	if not params.has_key(key): 
	    not_specified += 1
	    continue

	if key == 'autori':
	    for word in params[key].split():
		# WHERE ( Autori.nome LIKE '%<word>%' 
		#	    OR Autori.cognome LIKE '%<word>%' ) AND ...
		query = query & \
			( Edizione.objects.filter(autore__nome__icontains=word) \
			  | Edizione.objects.filter(autore__cognome__icontains=word))

	elif key in ['armadio', 'scaffale', 'posizione']:
	    kwargs = { 'copia__'+key: params[key].strip() }
	    query = query & Edizione.objects.filter(**kwargs)

	else:
	    for word in params[key].split():
		kwargs = { key+'__icontains': word }
		query = query & Edizione.objects.filter(**kwargs)

    if not_specified == len(keys): return None
    return query.distinct()



from django.http import HttpResponse
from django.shortcuts import render_to_response
from biblioteca.models import *

def home(request):
    prestiti = Prestito.objects.filter(datarestituzione__isnull=True)
    context_data = { 'prestiti': prestiti }

    return render_to_response('biblioteca/home.html', context_data)

def armadio(request, nome_armadio=None):
    armadi = Copia.objects.values('armadio').distinct()
    armadi = [ row['armadio'] for row in armadi ]

    if nome_armadio:
        armadio = {}
        copie = Copia.objects.filter(armadio=nome_armadio)

        for copia in copie:
            if not armadio.has_key(copia.scaffale):
                armadio[copia.scaffale] = {}

            armadio[copia.scaffale][copia.posizione] = \
                copia
        
        for scaffale in armadio.iterkeys():
            last = max(armadio[scaffale].keys())
            for i in range(last):
                if not armadio[scaffale].has_key(i+1):
                    armadio[scaffale][i+1] = None
            
        context_data = {
            'armadi':   armadi,
            'nome_armadio':  nome_armadio,
            'armadio': armadio,
        }

    else:
        context_data = { 'armadi': armadi }

    return render_to_response('biblioteca/armadio.html', context_data)


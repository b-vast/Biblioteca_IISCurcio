from django.http                    import HttpResponse, HttpResponseRedirect
from django.shortcuts               import render_to_response, get_object_or_404
from django.forms.models            import inlineformset_factory
from django.forms                   import widgets
from django.template                import RequestContext

from biblioteca.models  import *
from biblioteca.forms   import *
from biblioteca.widgets import ContentEditableWidget

import datetime

def lista(request):
    solo_restituiti = not request.GET.get('old')

    objects = Prestito.objects.order_by('-dataconsegna')
    if solo_restituiti: objects = objects.filter(datarestituzione__isnull=True)

    context_data = { 'object_list': objects }
    return render_to_response('biblioteca/prestito_list.html', context_data)

def dettagli(request, pk):
    prestito = get_object_or_404(Prestito, pk=pk)
    context_data = {
        'mode': 'prestito',
        'prestito': prestito,
        'copia': prestito.copia,
        'prestiti': prestito.copia.prestito_set.filter(datarestituzione__isnull=False).order_by('dataconsegna')
    }
    return render_to_response('biblioteca/prestiti_copia.html', context_data,
                                context_instance=RequestContext(request))



def modifica(request, pk):
    prestito = get_object_or_404(Prestito, pk=pk)
    id_copia = prestito.copia.id
    if request.method == 'POST':
        form_data = request.POST.copy()
        form_data['copia'] = id_copia
        form = PrestitoForm(form_data, instance=prestito)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/copie/%d/+prestiti" % id_copia)
    else:
        form = PrestitoForm(instance=prestito)


    context_data = {
        'form': form,
        'copia': prestito.copia
    }
    return render_to_response('biblioteca/prestito_form.html', context_data,
                                context_instance=RequestContext(request))


# 
# Prestiti relativi a una copia
#
def copia(request, pk):
    copia = get_object_or_404(Copia, pk=pk)
    context_data = {
        'mode': 'copia',
        'prestito': copia.prestito_corrente(),
        'copia': copia,
        'prestiti': copia.prestito_set.filter(datarestituzione__isnull=False).order_by('dataconsegna')
    }
    return render_to_response('biblioteca/prestiti_copia.html', context_data,
                                context_instance=RequestContext(request))

def restituisci(request, pk):
    prestito = get_object_or_404(Prestito, pk=pk)

    if request.method == 'POST':
        prestito.datarestituzione = datetime.datetime.now()
        prestito.save()
        return HttpResponseRedirect('/copie/%d/+prestiti' % prestito.copia.id)

def aggiungi(request, pk):
    copia = get_object_or_404(Copia, pk=pk)

    if request.method == 'POST':
        form_data = request.POST.copy()
        form_data['copia'] = copia.id
        form = PrestitoForm(form_data)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/copie/"+pk+"/+prestiti")
    else:
        form = PrestitoForm()

    context_data = {
        'form': form,
        'copia': copia,
    }
    return render_to_response('biblioteca/prestito_form.html', context_data,
                                context_instance=RequestContext(request))





from django.http                    import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts               import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.template                import RequestContext

from biblioteca.models  import *
from biblioteca.forms   import *

def dettagli(request, pk):
    edizione = get_object_or_404(Edizione, id=pk)
    context_data = {
        'edizione': edizione,
        'autori':   edizione.autore_set.order_by('cognome'),
    }
    return render_to_response('biblioteca/edizione_detail.html', context_data,
            context_instance=RequestContext(request))

def modifica(request, pk):
    edizione = get_object_or_404(Edizione, pk=pk)

    if request.method == 'POST':
        form, fs_autori, fs_copie = \
                EdizioneForm(request.POST, instance=edizione), \
                Autori_InlineFormSet(request.POST, instance=edizione, prefix='autori'), \
                Copie_InlineFormSet(request.POST, instance=edizione, prefix='copie')

        if form.is_valid() and fs_autori.is_valid() and fs_copie.is_valid():
            form.save()
            fs_autori.save()
            fs_copie.save()
            return HttpResponseRedirect('/edizioni/'+pk)
    else:
        autori_queryset = edizione.autore_set.order_by('cognome')

        form, fs_autori, fs_copie = \
                EdizioneForm(instance=edizione), \
                Autori_InlineFormSet(instance=edizione, queryset=autori_queryset, prefix='autori'), \
                Copie_InlineFormSet(instance=edizione, prefix='copie')

    context_data = {
        'object': edizione,
        'form': form,
        'formset_autori': fs_autori,
        'formset_copie': fs_copie,
    }
    return render_to_response('biblioteca/edizione_form.html', context_data,
                                context_instance=RequestContext(request))


def aggiungi(request):
    if request.method == 'POST':
        form = EdizioneForm(request.POST)
        if form.is_valid():
            form.save()
            edizione = form.instance
        else:
            edizione = None

        fs_autori = Autori_InlineFormSet(request.POST, instance=edizione, prefix='autori')
        fs_copie = Copie_InlineFormSet(request.POST, instance=edizione, prefix='copie')
        if edizione and fs_autori.is_valid() and fs_copie.is_valid():
            fs_autori.save()
            fs_copie.save()
            return HttpResponseRedirect('/edizioni/'+str(edizione.id))

    else:
        form = EdizioneForm(initial=request.GET.items())

        # Crea e popola il formset, partendo dai parametri GET. Fa ribrezzo, lo so.
        init_autori = request.GET.getlist('autori')
        Autori_IFS = inlineformset_factory(Edizione, Autore, can_delete=True, \
                                            extra=max(1, len(init_autori)))
        fs_autori = Autori_IFS(prefix='autori')
        for subform, autore in zip(fs_autori.forms, init_autori):
            toks = autore.split(',', 2)
            if len(toks) < 2: toks.append('')
            subform.initial =   { 'nome'   : toks[0]
                                , 'cognome': toks[1] }

        Copie_IFS = inlineformset_factory(Edizione, Copia, can_delete=True, extra=1)
        fs_copie = Copie_IFS(prefix='copie')

    context_data = {
        'form': form,
        'formset_autori': fs_autori,
        'formset_copie': fs_copie,
    }
    return render_to_response('biblioteca/edizione_form.html', context_data,
                                context_instance=RequestContext(request))


def elimina(request, pk):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    edizione = get_object_or_404(Edizione, pk=pk)
    edizione.delete()

    return HttpResponseRedirect('/edizioni')



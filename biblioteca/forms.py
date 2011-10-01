
from django.forms           import *
from django.forms.models    import inlineformset_factory

from biblioteca.models  import * 
from biblioteca.widgets import ContentEditableWidget


class EdizioneForm(ModelForm):
    class Meta:
        model = Edizione

'''
def copieinline_formfield_callback(field):
    if field.name == 'note':
        return field.formfield(widget=ContentEditableWidget)
    else:
        return field.formfield()
'''

Autori_InlineFormSet = inlineformset_factory(Edizione, Autore, extra=1, can_delete=True)

Copie_InlineFormSet = inlineformset_factory(Edizione, Copia, extra=1, can_delete=True)
                                                #formfield_callback=copieinline_formfield_callback)

class PrestitoForm(ModelForm):
    class Meta:
        model = Prestito

class RicercaPrestitiForm(Form):
    query = CharField(required=False)
    restituiti = BooleanField(required=False)
    order = ChoiceField(required=False, choices=(
                            ('consegna', 'Data consegna'),
                            ('restituzione', 'Data restituzione'),
                            ('beneficiario', 'Cognome/nome'),
                        ))
    

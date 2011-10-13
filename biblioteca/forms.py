
from django.forms           import *
from django.forms.models    import inlineformset_factory

from biblioteca.models  import * 

class EdizioneForm(ModelForm):
    class Meta:
        model = Edizione

Autori_InlineFormSet = inlineformset_factory(Edizione, Autore, extra=1, can_delete=True)

Copie_InlineFormSet = inlineformset_factory(Edizione, Copia, extra=1, can_delete=True)

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
    

from django.db import models

from datetime import date

class Edizione(models.Model):
    titolo          = models.CharField(max_length=900, db_column='Titolo')
    casaeditrice    = models.CharField(max_length=135, db_column='CasaEditrice',
                                        blank=True, verbose_name='Casa editrice')
    anno            = models.CharField(max_length=4, db_column='Anno', blank=True, null=True)
    isbn            = models.CharField(max_length=60, db_column='ISBN',
                                        blank=True, verbose_name='ISBN')

    def __unicode__(self):
        return "<Edizione#%d: %s>" % (self.id, self.titolo)
    class Meta:
        db_table = u'Edizioni'
        verbose_name_plural = 'Edizioni'

class Autore(models.Model):
    nome        = models.CharField(max_length=135, db_column='Nome')
    cognome     = models.CharField(max_length=300, db_column='Cognome')
    edizione    = models.ForeignKey(Edizione, db_column='FK_IdEdizione')
    
    def __unicode__(self):
        return "<Autore#%d: %s %s>" % (self.id, self.nome, self.cognome)
    class Meta:
        db_table = u'Autori'
        unique_together = ('nome', 'cognome', 'edizione')
        verbose_name_plural = 'Autori'


class Copia(models.Model):
    armadio     = models.CharField(max_length=15, db_column='Armadio')
    scaffale    = models.CharField(max_length=15, db_column='Scaffale')
    posizione   = models.IntegerField(db_column='Posizione')
    note        = models.TextField(db_column='Note', blank=True)
    dataora     = models.DateTimeField(null=True, db_column='DataOra', auto_now_add=True)
    edizione    = models.ForeignKey(Edizione, db_column='FK_idEdizione')

    def __unicode__(self):
        return "<Copia#%d: %s %s %d>" % (self.id, self.armadio, self.scaffale, self.posizione)
    class Meta:
        db_table = u'Copie'
        unique_together = ('armadio', 'scaffale', 'posizione')
        verbose_name_plural = 'Copie'

    def prestito_corrente(self):
        try:
            return self.prestito_set.get(datarestituzione__isnull=True)
        except Prestito.DoesNotExist:
            return None


class Prestito(models.Model):
    nome        = models.CharField(max_length=135, db_column='Nome')
    cognome     = models.CharField(max_length=135, db_column='Cognome')
    categoria   = models.CharField(max_length=60, db_column='Categoria')
    classe      = models.CharField(max_length=30, db_column='Classe', blank=True)

    dataconsegna        = models.DateField(db_column='DataConsegna', auto_now_add=True)
    datarestituzione    = models.DateField(null=True, db_column='DataRestituzione', blank=True)

    nomeresp    = models.CharField(max_length=135, db_column='NomeResp')
    cognomeresp = models.CharField(max_length=135, db_column='CognomeResp')

    note = models.TextField(db_column='Note', blank=True)

    copia = models.ForeignKey(Copia, db_column='FK_idCopia')

    def __unicode__(self):
        return "<Prestito#%d: %s %s, %s>" % (self.id, self.nome, self.cognome, self.dataconsegna)
    class Meta:
        db_table = u'Prestiti'
        verbose_name_plural = 'Prestiti'

    def durata(self):
        if self.datarestituzione == None:
            return date.today() - self.dataconsegna
        else:
            return self.datarestituzione - self.dataconsegna




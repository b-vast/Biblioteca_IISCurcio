from biblioteca.models import *
from django.contrib import admin

class AutoreInlineAdmin(admin.TabularInline):
    model = Autore
    extra = 1

class CopiaInlineAdmin(admin.StackedInline):
    model = Copia
    extra = 1

class EdizioneAdmin(admin.ModelAdmin):
    model = Edizione
    list_display = ('titolo', 'casaeditrice', 'anno', 'isbn')
    inlines = [AutoreInlineAdmin, CopiaInlineAdmin]

class CopiaAdmin(admin.ModelAdmin):
    model = Edizione
    list_display = ('armadio', 'scaffale', 'posizione', 'dataora')

admin.site.register(Edizione, EdizioneAdmin)
admin.site.register(Copia, CopiaAdmin)


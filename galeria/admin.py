from django.contrib import admin
from .models import Foto

class FotoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'local', 'data_foto', 'status', 'estrela')
    list_filter = ('status', 'estrela', 'local')
    search_fields = ('titulo', 'descricao', 'local')
    list_editable = ('status', 'estrela')

admin.site.register(Foto, FotoAdmin)
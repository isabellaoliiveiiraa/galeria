from django.views.generic import ListView, DetailView
from .models import Foto
from django.db.models import Q

# View da página inicial (agora mais simples)
class GaleriaView(ListView):
    model = Foto
    template_name = 'galeria/index.html'
    context_object_name = 'fotos'

    def get_queryset(self):
        return Foto.objects.filter(status='PUBLICADO').order_by('-estrela', '-data_foto')

# View da página de detalhes (não muda)
class FotoDetailView(DetailView):
    model = Foto
    template_name = 'galeria/detalhe_foto.html'
    context_object_name = 'foto'

# Nova view para a página de pesquisa dedicada
class PaginaPesquisaView(ListView):
    model = Foto
    template_name = 'galeria/pagina_pesquisa.html'
    context_object_name = 'fotos'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            # A lógica de busca vive aqui agora
            return Foto.objects.filter(
                Q(titulo__icontains=query) |
                Q(descricao__icontains=query) |
                Q(local__icontains=query),
                status='PUBLICADO'
            ).order_by('-estrela', '-data_foto')
        
        # Se não houver busca, não retorna nenhuma foto
        return Foto.objects.none()

    def get_context_data(self, **kwargs):
        # Passa o termo de busca para o template para exibi-lo na caixa de texto
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView, View
from django.contrib import messages  # <-- IMPORT ADICIONADO
from django.db.models import Q
from .models import Foto

class GaleriaView(ListView):
    model = Foto
    template_name = 'galeria/index.html'
    context_object_name = 'fotos'

    def get_queryset(self):
        return Foto.objects.filter(status='PUBLICADO', estrela=False).order_by('-data_foto')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fotos_destaque'] = Foto.objects.filter(status='PUBLICADO', estrela=True).order_by('-data_foto')
        return context

class FotoDetailView(DetailView):
    model = Foto
    template_name = 'galeria/detalhe_foto.html'
    context_object_name = 'foto'

class PaginaPesquisaView(ListView):
    model = Foto
    template_name = 'galeria/pagina_pesquisa.html'
    context_object_name = 'fotos'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Foto.objects.filter(
                Q(titulo__icontains=query) |
                Q(descricao__icontains=query) |
                Q(local__icontains=query),
                status='PUBLICADO'
            ).order_by('-estrela', '-data_foto')
        
        return Foto.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class SobreNosView(TemplateView):
    template_name = 'galeria/sobre_nos.html'

# <-- VERSÃO CORRETA E ÚNICA DA VIEW DE CONTATO -->
class ContatoView(View):
    def get(self, request):
        """Este método é chamado quando o usuário apenas visita a página."""
        return render(request, 'galeria/contato.html')

    def post(self, request):
        """Este método é chamado quando o usuário envia o formulário."""
        # Pega os dados do formulário
        nome = request.POST.get('name')
        email = request.POST.get('email')
        mensagem = request.POST.get('message')

        # Você pode usar os dados aqui (enviar email, salvar no banco, etc.)
        # Por enquanto, apenas imprimimos no console para confirmar o recebimento
        print(f"Nova mensagem recebida de: {nome} ({email})")

        # Adiciona uma mensagem de sucesso para ser exibida na próxima página
        messages.success(request, 'Sua mensagem foi enviada com sucesso!')

        # Redireciona o usuário para a página inicial
        return redirect('galeria:lista_fotos')
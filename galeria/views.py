from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView, View
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail
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


class ContatoView(View):
    def get(self, request):
        return render(request, 'galeria/contato.html')

    def post(self, request):
        nome = request.POST.get('name')
        email = request.POST.get('email')
        mensagem = request.POST.get('message')

        # Etapa 1: Armazenar o contacto (continua igual)
        dados_contato = f"{nome},{email},'{mensagem.replace(',',';')}'\n"
        with open("contatos_recebidos.csv", "a", encoding='utf-8') as arquivo:
            arquivo.write(dados_contato)

        # Etapa 2: Enviar o e-mail usando a função do Django
        try:
            assunto = "Recebemos a sua mensagem!"
            corpo_email = f"Olá {nome},\n\nObrigado por entrar em contacto. A sua mensagem foi recebida e responderemos em breve.\n\nAtenciosamente,\nA Sua Galeria"
            
            send_mail(
                assunto,
                corpo_email,
                'nao-responda@suagaleria.com',  # E-mail remetente
                [email],                       # Lista de destinatários
                fail_silently=False,
            )
        except Exception as e:
            messages.error(request, 'Ocorreu um erro ao processar a sua mensagem.')
            print(f"Erro ao enviar e-mail: {e}")
            return render(request, 'galeria/contato.html')

        # Etapa 3: Redirecionar para a página principal da galeria
        messages.success(request, 'A sua mensagem foi enviada com sucesso!')
        return redirect('galeria:lista_fotos')
from django.urls import path
from .views import GaleriaView, FotoDetailView, PaginaPesquisaView

app_name = 'galeria'

urlpatterns = [
    path('', GaleriaView.as_view(), name='lista_fotos'),
    path('foto/<int:pk>/', FotoDetailView.as_view(), name='detalhe_foto'),
    path('pesquisar/', PaginaPesquisaView.as_view(), name='pagina_pesquisa'),
]
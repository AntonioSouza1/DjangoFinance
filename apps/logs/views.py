from auditlog.models import LogEntry
from django.shortcuts import render

from django.views.generic import ListView

class LogListView(ListView):
    # O modelo que será consultado. É o modelo do django-auditlog.
    model = LogEntry

    # Define o nome da template que será renderizada.
    template_name = 'logs/logs.html'

    # Define o nome da variável de contexto na template.
    context_object_name = 'log_entries'

    # Opcional: Define a paginação (exibindo 25 logs por página)
    paginate_by = 25

    def get_queryset(self):
        # Consulta para ordenar os logs do mais recente para o mais antigo (recomendado)
        queryset = super().get_queryset().order_by('-timestamp')

        # Opcional: Implemente filtros aqui se necessário
        # Ex: Filtrar por um modelo específico, se o usuário clicar em um botão
        # model_id = self.request.GET.get('model_id')
        # if model_id:
        #     queryset = queryset.filter(content_type__model=model_id)

        return queryset
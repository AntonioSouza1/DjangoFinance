from django.contrib import messages
from django.core.exceptions import PermissionDenied


class SuccessErrorMessageMixin:
    success_message = 'Salvo com sucesso!'
    error_message = 'Erro ao processar'

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response

    def form_invalid(self, form):
        for msgs in form.errors.values():
            for msg in msgs:
                messages.error(self.request, msg)
        return super().form_invalid(form)


from django.shortcuts import redirect
from django.contrib import messages


class UserIsOwnerMixin:
    # URL padrão caso a View não defina nenhuma
    permission_denied_url = 'dashboard:home'

    def dispatch(self, request, *args, **kwargs):
        # Tenta pegar o objeto.
        # Nota: get_object() só funciona em UpdateView, DeleteView e DetailView.
        try:
            obj = self.get_object()
        except:
            # Se o objeto nem existe (404), deixamos o Django tratar ou redirecionamos
            return super().dispatch(request, *args, **kwargs)

        # A LÓGICA DE PROTEÇÃO
        if obj.user != request.user:
            # 1. Adiciona a mensagem
            messages.error(request, "Você não tem permissão para acessar este registro.")

            # 2. Verifica se a View definiu uma URL específica
            # getattr(objeto, 'nome_atributo', 'valor_padrao')
            redirect_to = getattr(self, 'permission_denied_url', 'dashboard:home')

            # 3. Faz o redirecionamento em vez do erro 403
            return redirect(redirect_to)

        return super().dispatch(request, *args, **kwargs)

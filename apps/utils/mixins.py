from django.contrib import messages

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

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = 'contas'

    def ready(self):
        # Importado pelo efeito: registra a criação do perfil junto com a conta.
        from . import signals  # noqa: F401

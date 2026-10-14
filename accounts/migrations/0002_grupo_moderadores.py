from django.contrib.auth.management import create_permissions
from django.db import migrations

GROUP = 'Moderadores'

# UC11 (moderar comentário) e UC13 (gerenciar usuários). Moderador é concedido
# à mão por quem administra a plataforma (RN08), incluindo a conta no grupo e
# marcando o acesso ao admin.
PERMISSIONS = [
    ('comments', 'view_comment'),
    ('comments', 'change_comment'),
    ('auth', 'view_user'),
    ('auth', 'change_user'),
]


def create_group(apps, schema_editor):
    # As permissões só existem depois do post_migrate; aqui são criadas antes,
    # para que o grupo já nasça com elas.
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None

    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    group, _ = Group.objects.get_or_create(name=GROUP)
    for app_label, codename in PERMISSIONS:
        group.permissions.add(
            Permission.objects.get(content_type__app_label=app_label, codename=codename)
        )


def remove_group(apps, schema_editor):
    apps.get_model('auth', 'Group').objects.filter(name=GROUP).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('comments', '0001_initial'),
    ]

    operations = [migrations.RunPython(create_group, remove_group)]

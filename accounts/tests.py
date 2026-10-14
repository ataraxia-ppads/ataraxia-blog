"""Testes de accounts, com o identificador do caso de teste do plano."""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from .models import Profile

User = get_user_model()


class SignUpTests(TestCase):
    url = reverse('accounts:signup')

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user('ana', 'ana@example.com', 'Senha#forte1')

    def signup(self, username='carla', email='carla@example.com', password='Ataraxia#2026'):
        return self.client.post(self.url, {
            'username': username, 'email': email,
            'password1': password, 'password2': password,
        })

    def password_errors(self, password, username='carla'):
        response = self.signup(username=username, password=password)
        self.assertEqual(response.status_code, 200)
        return ' '.join(response.context['form'].errors.get('password2', []))

    def test_cadastro_cria_conta_perfil_e_sessao(self):
        response = self.signup()
        self.assertRedirects(response, reverse('posts:list'))
        carla = User.objects.get(username='carla')
        self.assertTrue(Profile.objects.filter(user=carla).exists())
        self.assertEqual(int(self.client.session['_auth_user_id']), carla.pk)

    def test_ct05_02_nome_de_usuario_repetido(self):
        response = self.signup(username='ana')
        form = response.context['form']
        self.assertTrue(form.has_error('username'))
        self.assertContains(response, 'value="carla@example.com"')
        self.assertNotContains(response, 'Ataraxia#2026')

    def test_ct05_03_email_repetido(self):
        response = self.signup(email='ANA@example.com')
        self.assertFormError(
            response.context['form'], 'email', 'Já existe uma conta com este e-mail.'
        )

    def test_ct05_04_senha_com_sete_caracteres(self):
        self.assertIn('pelo menos 8 caracteres', self.password_errors('Atx#202'))

    def test_ct05_05_senha_com_oito_caracteres(self):
        self.assertRedirects(self.signup(password='Atx#2026'), reverse('posts:list'))

    def test_ct05_06_senha_so_numerica(self):
        self.assertIn('inteiramente numérica', self.password_errors('48271935'))

    def test_ct05_07_senha_comum(self):
        self.assertIn('muito comum', self.password_errors('password'))

    def test_ct05_08_senha_parecida_com_usuario(self):
        errors = self.password_errors('carlamendes1', username='carlamendes')
        self.assertIn('muito parecida', errors)

    def test_ct05_09_senha_guardada_como_hash(self):
        self.signup()
        stored = User.objects.get(username='carla').password
        self.assertTrue(stored.startswith('pbkdf2_sha256$'))
        self.assertNotIn('Ataraxia#2026', stored)

    def test_ct05_10_conta_nova_nao_entra_no_admin(self):
        self.signup()
        carla = User.objects.get(username='carla')
        self.assertFalse(carla.is_staff or carla.is_superuser)
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('admin:login'), response['Location'])


class LoginTests(TestCase):
    url = reverse('accounts:login')

    @classmethod
    def setUpTestData(cls):
        cls.ana = User.objects.create_user('ana', 'ana@example.com', 'Senha#forte1')

    def error_for(self, username, password):
        response = self.client.post(self.url, {'username': username, 'password': password})
        return response.context['form'].non_field_errors()

    def test_ct06_02_e_ct06_03_mesma_mensagem_para_senha_e_usuario(self):
        wrong_password = self.error_for('ana', 'errada')
        unknown_user = self.error_for('zeca', 'qualquer')
        self.assertTrue(wrong_password)
        self.assertEqual(wrong_password, unknown_user)

    def test_ct06_04_sair_encerra_a_sessao(self):
        self.client.force_login(self.ana)
        self.client.post(reverse('accounts:logout'))
        response = self.client.get(reverse('posts:create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.url, response['Location'])


class ProfileTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ana = User.objects.create_user('ana', 'ana@example.com', 'Senha#forte1')
        cls.bruno = User.objects.create_user('bruno', 'bruno@example.com', 'Senha#forte2')

    def test_ct07_03_edicao_atua_so_sobre_a_sessao(self):
        self.client.force_login(self.bruno)
        self.client.post(reverse('accounts:profile_edit'),
                         {'display_name': 'Invasor', 'bio': 'x', 'user': self.ana.pk})
        self.assertEqual(Profile.objects.get(user=self.bruno).display_name, 'Invasor')
        self.assertEqual(Profile.objects.get(user=self.ana).display_name, '')

    def test_ct07_04_edicao_exige_autenticacao(self):
        response = self.client.get(reverse('accounts:profile_edit'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('accounts:login'), response['Location'])


class AdminPermissionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ana = User.objects.create_user('ana', 'ana@example.com', 'Senha#forte1')
        cls.bruno = User.objects.create_user('bruno', 'bruno@example.com', 'Senha#forte2')
        cls.admin = User.objects.create_superuser('admin', 'admin@example.com', 'Senha#forte3')
        cls.moderator = User.objects.create_user(
            'moderador', 'mod@example.com', 'Senha#forte4', is_staff=True
        )
        cls.moderator.groups.add(Group.objects.get(name='Moderadores'))

    def change_url(self, user):
        return reverse('admin:auth_user_change', args=[user.pk])

    def test_ct11_04_autor_nao_acessa_o_admin(self):
        self.client.force_login(self.ana)
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 302)

    def test_ct13_02_conta_desativada_nao_entra(self):
        self.bruno.is_active = False
        self.bruno.save()
        self.assertFalse(self.client.login(username='bruno', password='Senha#forte2'))

    def test_ct13_03_moderador_nao_ve_superusuario(self):
        self.client.force_login(self.moderator)
        for user in (self.moderator, self.bruno):
            response = self.client.get(self.change_url(user))
            self.assertEqual(response.status_code, 200)
            fields = response.context['adminform'].form.fields
            self.assertIn('is_active', fields)
            self.assertIn('groups', fields)
            self.assertNotIn('is_superuser', fields)
            self.assertNotIn('user_permissions', fields)

    def test_ct13_04_moderador_nao_altera_superusuario(self):
        self.client.force_login(self.moderator)
        response = self.client.post(self.change_url(self.admin), {
            'username': 'admin', 'email': 'outro@example.com', 'is_active': '',
        })
        self.assertEqual(response.status_code, 403)
        self.admin.refresh_from_db()
        self.assertTrue(self.admin.is_active)
        self.assertEqual(self.admin.email, 'admin@example.com')

    def test_moderador_concede_o_papel_a_outro(self):
        # CT13.01, executado também à mão: o grupo dá acesso à moderação.
        self.client.force_login(self.moderator)
        group = Group.objects.get(name='Moderadores')
        response = self.client.post(self.change_url(self.bruno), {
            'username': 'bruno', 'email': 'bruno@example.com', 'is_active': 'on',
            'is_staff': 'on', 'groups': [group.pk],
            'profile-TOTAL_FORMS': '1', 'profile-INITIAL_FORMS': '1',
            'profile-MIN_NUM_FORMS': '0', 'profile-MAX_NUM_FORMS': '1',
            'profile-0-id': self.bruno.profile.pk, 'profile-0-user': self.bruno.pk,
            'profile-0-display_name': '', 'profile-0-bio': '',
        })
        self.assertEqual(response.status_code, 302)
        self.bruno.refresh_from_db()
        self.assertTrue(self.bruno.has_perm('comments.change_comment'))
        self.assertFalse(self.bruno.is_superuser)

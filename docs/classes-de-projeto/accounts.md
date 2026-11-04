## accounts

```mermaid
classDiagram
    class User {
        <<Model do Django>>
        +CharField username
        +EmailField email
        +CharField password
        +check_password()
    }
    class Profile {
        <<Model>>
        +OneToOneField user
        +CharField display_name
        +TextField bio
        +get_absolute_url()
        +__str__()
    }
    class SignUpForm {
        <<Form>>
        +CharField username
        +EmailField email
        +CharField password1
        +CharField password2
        +clean_email()
    }
    class ProfileForm {
        <<Form>>
        +CharField display_name
        +TextField bio
    }
    class SignUpView {
        <<View>>
        +form_class
        +success_url
        +dispatch()
        +form_valid()
    }
    class ProfileDetailView {
        <<View>>
        +get_object()
        +get_context_data()
    }
    class ProfileUpdateView {
        <<View>>
        +form_class
        +get_object()
        +form_valid()
    }

    class UserAdmin {
        <<Admin>>
        +moderator_fieldsets
        +get_fieldsets()
        +get_readonly_fields()
        +has_change_permission()
        +has_delete_permission()
    }

    User "1" -- "1" Profile : perfil
    SignUpView --> SignUpForm : valida com
    SignUpForm --> User : cria
    ProfileDetailView --> Profile : exibe
    ProfileUpdateView --> ProfileForm : valida com
    ProfileForm --> Profile : edita
    UserAdmin --> User : gerencia
```

**Figura 16 — Classes de projeto de accounts**

O usuário é o `User` do próprio Django, e não um modelo novo. A informação que o
projeto acrescenta fica no `Profile`, ligado a ele um para um. Trocar o modelo
de usuário depois da primeira migração é caro e nada no escopo exige isso.

`SignUpForm` é quem garante RN06 e RN07: herda o `save()` do `UserCreationForm`, que grava a senha como hash, e a validação de robustez é a do Django, não uma regra escrita à mão. O perfil é criado pelo sinal `create_profile` sempre que uma conta nasce, seja pelo cadastro, pelo admin ou pelo `createsuperuser`, para que não exista usuário sem perfil.

`ProfileUpdateView` devolve sempre o perfil de quem está autenticado, e é assim que o autor não edita o perfil de outro. `ProfileDetailView` é a face pública da conta: mostra nome de exibição, biografia e os textos publicados do autor.

`UserAdmin` substitui o cadastro de usuários padrão do admin para atender UC13 com segurança. No admin padrão, quem pode alterar usuários enxerga também o campo de superusuário e as permissões avulsas, e poderia conceder a si mesmo acesso total. Para quem não é superusuário, `get_fieldsets()` mostra apenas situação da conta, acesso ao admin e grupos, e `has_change_permission()` e `has_delete_permission()` recusam alterar ou excluir a conta de um superusuário.

A restrição fica registrada como regra de negócio de UC13:

- **RN18 —** O moderador gerencia as contas de autores, mas não vê nem concede
  o papel de superusuário, e não altera a conta de quem o tem.

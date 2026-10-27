# Aula 4 — Passo a passo: templates e autenticação no Django

Este guia explica quais arquivos modificar para acrescentar login, logout, uma página restrita e uma demonstração de permissões ao projeto da biblioteca.

> As instruções abaixo descrevem a implementação já feita neste projeto. Faça as alterações nos arquivos existentes sem apagar as rotas, views ou conteúdo que pertencem às aulas anteriores.

## 1. Confira as configurações do Django

Abra `meu_projeto/settings.py`. O projeto já deve ter:

- `django.contrib.auth` e `django.contrib.sessions` em `INSTALLED_APPS`;
- `django.contrib.sessions.middleware.SessionMiddleware` e `django.contrib.auth.middleware.AuthenticationMiddleware` em `MIDDLEWARE`;
- `django.contrib.auth.context_processors.auth` na lista `context_processors` dos templates.

Essas opções permitem que o Django use usuários, sessões e a variável `user` nos templates. Não é preciso criar um model de usuário para esta aula.

No final das configurações, acrescente os endereços para onde o Django redireciona depois de entrar e sair:

```python
LOGIN_REDIRECT_URL = "core:area_restrita"
LOGOUT_REDIRECT_URL = "core:inicio"
```

## 2. Crie a view protegida

Abra `core/views.py`. Acrescente o import do decorador junto aos imports existentes:

```python
from django.contrib.auth.decorators import login_required
```

Depois da view `inicio`, acrescente:

```python
@login_required(login_url="core:login")
def area_restrita(request):
    return render(request, "core/area_restrita.html")
```

O decorador permite abrir a página somente depois do login. Se a pessoa estiver desconectada, o Django a envia para a rota `core:login` e, após entrar, retorna à página que ela tentou acessar.

## 3. Adicione as rotas de autenticação

Abra `core/urls.py`. Importe as views nativas de autenticação do Django:

```python
from django.contrib.auth import views as auth_views
```

Dentro de `urlpatterns`, mantenha as rotas existentes e acrescente as seguintes:

```python
path(
    "login/",
    auth_views.LoginView.as_view(template_name="core/login.html"),
    name="login",
),
path("logout/", auth_views.LogoutView.as_view(), name="logout"),
path("area-restrita/", views.area_restrita, name="area_restrita"),
```

As views `LoginView` e `LogoutView` fazem o trabalho de autenticar e encerrar a sessão; não implemente comparação ou armazenamento manual de senhas.

## 4. Crie o template de login

Crie `core/templates/core/login.html`. Como `APP_DIRS = True` já está habilitado, o Django encontra o arquivo dentro da pasta do app.

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Entrar | Aula Django</title>
</head>
<body>
    <main>
        <h1>Entrar</h1>
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <input type="hidden" name="next" value="{{ next }}">
            <button type="submit">Entrar</button>
        </form>
        <a href="{% url 'core:inicio' %}">Voltar ao início</a>
    </main>
</body>
</html>
```

`form.as_p` exibe o formulário fornecido pelo Django. O token CSRF protege o envio do formulário.

## 5. Crie o template da área restrita

Crie `core/templates/core/area_restrita.html`:

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Área restrita | Aula Django</title>
</head>
<body>
    <main>
        <h1>Área restrita</h1>
        <p>Olá, {{ user.username }}. Você está autenticado.</p>

        {% if perms.core.view_livro %}
            <p>Seu usuário tem permissão para visualizar livros.</p>
        {% else %}
            <p>Seu usuário não tem permissão para visualizar livros.</p>
        {% endif %}

        {% if user.is_staff %}
            <p>Seu usuário pode acessar o painel administrativo.</p>
            <a href="{% url 'admin:index' %}">Abrir o Admin</a>
        {% endif %}

        <a href="{% url 'core:inicio' %}">Voltar ao início</a>
        <form method="post" action="{% url 'core:logout' %}">
            {% csrf_token %}
            <button type="submit">Sair</button>
        </form>
    </main>
</body>
</html>
```

`user.is_authenticated` identifica se a pessoa entrou. `perms.core.view_livro` verifica a permissão de visualizar o model `Livro`. `user.is_staff` indica se a conta pode acessar o Admin; para entrar nele, a conta também precisa estar ativa.

## 6. Atualize a página inicial

Abra `core/templates/core/inicio.html`. Mantenha os links e conteúdos já existentes e acrescente na navegação um link para a área restrita e uma opção condicional de login ou logout:

```html
<li><a href="{% url 'core:area_restrita' %}">Área restrita</a></li>
{% if user.is_authenticated %}
    <li>Olá, {{ user.username }}!</li>
    <li>
        <form method="post" action="{% url 'core:logout' %}">
            {% csrf_token %}
            <button type="submit">Sair</button>
        </form>
    </li>
{% else %}
    <li><a href="{% url 'core:login' %}">Entrar</a></li>
{% endif %}
```

O logout é enviado por `POST`, com CSRF. Não use um link `GET` para encerrar a sessão.

## 7. Prepare o banco e uma conta de teste

```powershell
python -m venv .venv            # cria ambiente virtual (se não existir)
.\.venv\Scripts\Activate.ps1    # ativa o venv no PowerShell
python manage.py migrate        # aplica migrations (cria tabelas de auth, sessions, etc.)
python manage.py createsuperuser # cria conta admin interativamente
python manage.py runserver      # sobe o servidor de desenvolvimento
```

## 8. Execute e teste no navegador

Inicie o servidor:

```powershell
python manage.py runserver
```

Abra `http://127.0.0.1:8000/` e teste este fluxo:

1. Sem login, abra `/area-restrita/`. A página deve redirecionar para `/login/`.
2. Entre com a conta de teste. O Django deve redirecionar para a área restrita.
3. Na área restrita, confira o nome do usuário e a mensagem sobre a permissão.
4. Use **Sair**. Ao tentar abrir a área restrita novamente, será necessário entrar de novo.

## 9. Experimente a permissão no Admin

Entre em `/admin/` com a conta administradora. Na página de um usuário, conceda a permissão **Can view livro** (em português, **Pode visualizar livro**) e salve.

Para acessar o Admin, o usuário precisa estar ativo e ter **Status da equipe** (`is_staff`) habilitado. Depois, entre no site com esse usuário e abra `/area-restrita/`: a mensagem sobre a permissão deve indicar que ele pode visualizar livros.

Esta aula apenas demonstra a permissão no template. Em uma aplicação real, uma view que execute uma ação protegida também precisa verificar essa permissão no servidor, por exemplo com `@permission_required`.

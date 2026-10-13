# 🐍 Guia de Introdução ao Django

Repositório dedicado aos estudos de **Django**, um framework web desenvolvido em Python que facilita a criação de aplicações web de forma organizada, segura e eficiente.

Neste guia, você aprenderá a configurar o ambiente de desenvolvimento, criar um projeto Django, desenvolver sua primeira aplicação e utilizar o painel administrativo.

---

## 📚 Sumário

- [🛠️ 1. Criando o ambiente de trabalho](#️-1-criando-o-ambiente-de-trabalho)
- [📦 2. Instalando o Django](#-2-instalando-o-django)
- [🚀 3. Criando o projeto](#-3-criando-o-projeto)
- [🧩 4. Criando a primeira aplicação](#-4-criando-a-primeira-aplicação)
- [⚙️ 5. Registrando a aplicação](#️-5-registrando-a-aplicação)
- [🗄️ 6. Executando as migrações](#️-6-executando-as-migrações)
- [🔐 7. Criando um superusuário](#-7-criando-um-superusuário)
- [▶️ 8. Executando o servidor](#️-8-executando-o-servidor)
- [🏗️ 9. Entendendo a arquitetura MVT](#️-9-entendendo-a-arquitetura-mvt)
- [💡 10. Exemplo prático: criando um Model](#-10-exemplo-prático-criando-um-model)

---

## 🛠️ 1. Criando o ambiente de trabalho

Antes de começar, é importante criar um ambiente virtual para isolar as dependências do projeto e evitar conflitos entre diferentes versões de bibliotecas Python.

### Criando o ambiente virtual

Abra o terminal na pasta do projeto e execute:

```bash
python -m venv .venv
```

### Ativando o ambiente virtual

No Windows, utilizando o PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Se estiver utilizando o Prompt de Comando (CMD):

```bat
.venv\Scripts\activate.bat
```

> **⚠️ Possível erro:** se o PowerShell informar que a execução de scripts está desabilitada, execute:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Confirme a alteração, se solicitado, e tente ativar o ambiente novamente.

Quando o ambiente estiver ativo, você verá algo semelhante a `(.venv)` no início da linha do terminal.

---

## 📦 2. Instalando o Django

Com o ambiente virtual ativado, instale o Django:

```bash
python -m pip install django
```

Para verificar se a instalação foi concluída corretamente, execute:

```bash
python -m django --version
```

O terminal exibirá a versão instalada do framework.

---

## 🚀 3. Criando o projeto

Para criar a estrutura inicial do projeto Django, execute:

```bash
django-admin startproject meu_projeto .
```

O ponto (`.`) no final do comando indica que os arquivos do projeto serão criados no diretório atual, sem gerar uma pasta extra para o projeto.

A estrutura inicial será semelhante a esta:

```text
meu-projeto/
├── .venv/
├── meu_projeto/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── .gitignore
```

**Principais arquivos:**

- `manage.py`: executa comandos administrativos do Django.
- `settings.py`: contém as configurações do projeto.
- `urls.py`: define as rotas principais.
- `asgi.py` e `wsgi.py`: permitem a integração com servidores de aplicação.

---

## 🧩 4. Criando a primeira aplicação

No Django, um **projeto** representa a configuração geral do sistema, enquanto uma **app** concentra funcionalidades específicas.

Para criar a primeira aplicação, chamada `core`, execute:

```bash
python manage.py startapp core
```

A estrutura da aplicação será semelhante a esta:

```text
core/
├── migrations/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── tests.py
└── views.py
```

**Função dos principais arquivos:**

- `models.py`: define os modelos e os dados do sistema.
- `views.py`: contém as funções ou classes responsáveis pelo processamento das requisições.
- `admin.py`: configura o painel administrativo.
- `apps.py`: contém a configuração da aplicação.
- `migrations/`: armazena os arquivos de migração do banco de dados.

---

## ⚙️ 5. Registrando a aplicação

Para que o Django reconheça a aplicação `core`, abra o arquivo `meu_projeto/settings.py`.

Localize a lista `INSTALLED_APPS` e adicione `'core'`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Aplicações do projeto
    'core',
]
```

Salve o arquivo após realizar a alteração.

---

## 🗄️ 6. Executando as migrações

Por padrão, o Django utiliza o SQLite como banco de dados em novos projetos. Ele também fornece modelos e migrações para funcionalidades como autenticação, administração e sessões.

Para criar as tabelas iniciais do banco de dados, execute:

```bash
python manage.py migrate
```

O comando aplica as migrações disponíveis e prepara o banco de dados para utilização.

---

## 🔐 7. Criando um superusuário

O Django possui um painel administrativo integrado que permite gerenciar os dados da aplicação.

Para criar uma conta com acesso administrativo, execute:

```bash
python manage.py createsuperuser
```

Em seguida, informe os dados solicitados pelo terminal:

- Nome de usuário;
- Endereço de e-mail, se solicitado;
- Senha.

**Importante:** a senha não será exibida enquanto você digita. Isso é normal.

---

## ▶️ 8. Executando o servidor

Para iniciar o servidor de desenvolvimento, execute:

```bash
python manage.py runserver
```

Se tudo estiver configurado corretamente, a aplicação estará disponível localmente.

| Recurso | Endereço |
|---|---|
| Aplicação | [http://127.0.0.1:8000/](http://127.0.0.1:8000/) |
| Painel administrativo | [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) |

Acesse o painel administrativo e entre com as credenciais criadas na etapa anterior.

> **Nota:** o servidor de desenvolvimento é destinado a testes locais, não à publicação de aplicações em produção.

---

## 🏗️ 9. Entendendo a arquitetura MVT

O Django utiliza o padrão arquitetural **MVT (Model-View-Template)**, semelhante ao MVC, mas com algumas diferenças na distribuição das responsabilidades.

| Componente | Responsabilidade | Arquivo ou diretório |
|---|---|---|
| **Model** | Define os dados e o relacionamento com o banco por meio do ORM. | `core/models.py` |
| **View** | Processa requisições, executa regras de negócio e prepara respostas. | `core/views.py` |
| **Template** | Define a apresentação da interface, geralmente em HTML. | `core/templates/` |
| **URLconf** | Associa endereços às views correspondentes. | `urls.py` |

### Como funciona o fluxo?

1. O usuário acessa uma URL pelo navegador.
2. O Django identifica a rota correspondente.
3. A view processa a requisição e, quando necessário, consulta os models.
4. A view pode renderizar um template HTML.
5. O Django devolve a resposta ao navegador.

---

## 💡 10. Exemplo prático: criando um Model

Vamos criar um modelo chamado `Item` para armazenar informações no banco de dados e disponibilizá-las no painel administrativo.

### 10.1. Definindo o Model

Abra `core/models.py` e adicione:

```python
from django.db import models


class Item(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
```

**Entendendo os campos:**

- `CharField`: armazena textos curtos, limitados a 100 caracteres neste exemplo.
- `TextField`: armazena textos maiores; `blank=True` permite deixar o campo vazio nos formulários.
- `DateTimeField`: registra data e hora automaticamente na criação do objeto.
- `__str__()`: define como o objeto será representado em texto, por exemplo, no painel administrativo.

### 10.2. Criando e aplicando as migrações

Após salvar o arquivo, execute:

```bash
python manage.py makemigrations
```

Esse comando gera os arquivos de migração com base nas alterações dos models.

Depois, aplique as alterações ao banco:

```bash
python manage.py migrate
```

### 10.3. Registrando o Model no Admin

Abra `core/admin.py` e adicione:

```python
from django.contrib import admin
from .models import Item

admin.site.register(Item)
```

### 10.4. Testando no painel administrativo

Se o servidor ainda não estiver em execução, inicie-o:

```bash
python manage.py runserver
```

Acesse [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) e entre com seu superusuário.

O modelo `Item` estará disponível para operações de **CRUD**:

- **Create:** criar novos itens.
- **Read:** visualizar os itens cadastrados.
- **Update:** editar os registros existentes.
- **Delete:** excluir registros.

O Django Admin já fornece uma interface para essas operações básicas, sem exigir a criação manual de formulários HTML.

---

## 📌 Comandos essenciais

| Comando | Finalidade |
|---|---|
| `python -m venv .venv` | Criar o ambiente virtual |
| `python -m pip install django` | Instalar o Django |
| `django-admin startproject meu_projeto .` | Criar o projeto |
| `python manage.py startapp core` | Criar uma aplicação |
| `python manage.py makemigrations` | Gerar migrações |
| `python manage.py migrate` | Aplicar migrações |
| `python manage.py createsuperuser` | Criar usuário administrativo |
| `python manage.py runserver` | Iniciar o servidor |

---

## 🎯 Objetivo do repositório

Este repositório tem como objetivo consolidar os conhecimentos iniciais de desenvolvimento web com Django, praticando:

- Configuração de ambientes virtuais Python;
- Criação e organização de projetos e aplicações;
- Integração com banco de dados SQLite;
- Utilização de Models e migrações;
- Gerenciamento de dados pelo Django Admin;
- Compreensão da arquitetura MVT.

**Tecnologias utilizadas:** Python · Django · SQLite · HTML

---

⭐ *Repositório desenvolvido para fins de estudo e aprendizado em desenvolvimento web.*

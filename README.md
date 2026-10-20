# 🐍 Aula 3 — Views e URLs no Django

Este guia dá continuidade ao tutorial de introdução ao Django disponível no [README principal](./README.md). Nesta aula, vamos entender como o Django recebe uma requisição, encontra uma rota e executa uma **view** para devolver uma resposta.

Ao final, o projeto terá uma página inicial, uma listagem de itens feita de duas formas — **Function-Based View (FBV)** e **Class-Based View (CBV)** — e uma página de detalhes.

## 📚 Sumário

- [🎯 1. Objetivos da aula](#-1-objetivos-da-aula)
- [🔁 2. Fluxo de uma requisição](#-2-fluxo-de-uma-requisição)
- [🧭 3. Configurando as URLs](#-3-configurando-as-urls)
- [🧩 4. Criando as views](#-4-criando-as-views)
- [🖼️ 5. Criando os templates](#️-5-criando-os-templates)
- [▶️ 6. Executando e testando](#️-6-executando-e-testando)
- [⚖️ 7. FBV e CBV: diferença prática](#️-7-fbv-e-cbv-diferença-prática)
- [🧪 8. Exercícios para a turma](#-8-exercícios-para-a-turma)

---

## 🎯 1. Objetivos da aula

Nesta aula, vamos praticar:

- Como uma URL é associada a uma view;
- Como separar as rotas do projeto das rotas de uma aplicação;
- Como uma view recebe `request` e retorna uma resposta;
- Como ler parâmetros da URL, como o identificador de um item;
- Como renderizar um template e enviar dados em seu contexto;
- Como implementar a mesma listagem com FBV e CBV.

> **Pré-requisito:** este repositório já possui o projeto `meu_projeto`, o app `core`, o model `Item` e as migrações da aula anterior. Os comandos abaixo devem ser executados no diretório que contém `manage.py`.

---

## 🔁 2. Fluxo de uma requisição

O caminho de uma página no Django pode ser resumido assim:

1. O navegador envia uma requisição HTTP para um endereço, por exemplo `/itens/`.
2. O URLconf do projeto (`meu_projeto/urls.py`) procura uma rota correspondente.
3. A rota encaminha a requisição para uma view do app `core`.
4. A view pode consultar o model `Item` e preparar dados.
5. A view retorna uma resposta HTTP, frequentemente renderizando um template.
6. O Django envia a resposta ao navegador.

```text
Navegador → URL do projeto → URL do app → View → Model/Template → Resposta
```

**View não é o arquivo HTML.** A view coordena o processamento da requisição e escolhe a resposta. O template é usado para apresentar os dados.

---

## 🧭 3. Configurando as URLs

### 3.1. URLs do projeto

O arquivo `meu_projeto/urls.py` concentra as rotas de alto nível. Mantenha a rota administrativa e inclua as rotas do app:

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]
```

`include("core.urls")` delega para o app `core` a resolução das URLs da aplicação. Assim, as rotas não precisam ficar todas no arquivo do projeto.

### 3.2. URLs do app

Crie o arquivo `core/urls.py`:

```python
from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("itens/", views.lista_itens, name="lista_itens"),
    path("itens/cbv/", views.ItemListView.as_view(), name="lista_itens_cbv"),
    path("itens/<int:pk>/", views.detalhe_item, name="detalhe_item"),
]
```

**Elementos importantes:**

- `path()` associa um padrão de URL a uma view.
- `name` dá um nome reutilizável à rota.
- `<int:pk>` captura um número inteiro e passa seu valor para a view pelo argumento `pk`.
- `app_name` cria o namespace `core`, evitando colisões de nomes com outros apps.
- `ItemListView.as_view()` adapta uma CBV para que possa ser chamada como view pelo sistema de URLs.

Use os nomes das rotas em vez de repetir endereços escritos manualmente. Por exemplo, `reverse("core:lista_itens")` em Python ou `{% url 'core:lista_itens' %}` em um template.

---

## 🧩 4. Criando as views

Edite `core/views.py`:

```python
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from .models import Item


def inicio(request):
    return render(request, "core/inicio.html")


def lista_itens(request):
    itens = Item.objects.all().order_by("-criado_em", "-pk")
    return render(request, "core/item_list.html", {"itens": itens})


def detalhe_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, "core/item_detail.html", {"item": item})


class ItemListView(ListView):
    model = Item
    template_name = "core/item_list.html"
    context_object_name = "itens"
    ordering = ("-criado_em", "-pk")
```

### 4.1. Function-Based Views

Uma FBV é uma função Python. Ela recebe o objeto `request` e deve retornar uma resposta HTTP. A função `render()` combina uma requisição, um template e, opcionalmente, um contexto:

```python
def lista_itens(request):
    itens = Item.objects.all().order_by("-criado_em", "-pk")
    return render(request, "core/item_list.html", {"itens": itens})
```

Nesse exemplo, `itens` é disponibilizado no template com a chave `"itens"`. A consulta usa o ORM já introduzido na aula de Models e ORM.

Na página de detalhes, `get_object_or_404()` busca o registro pela chave primária. Se não houver um item correspondente, o Django retorna uma resposta **404 — Not Found**.

### 4.2. Class-Based Views

Uma CBV organiza o comportamento em uma classe. `ListView` é uma view genérica do Django que já implementa a lógica comum de listar objetos:

```python
class ItemListView(ListView):
    model = Item
    template_name = "core/item_list.html"
    context_object_name = "itens"
    ordering = ("-criado_em", "-pk")
```

Com poucas configurações, `ListView` consulta o model, escolhe o template e fornece a lista no contexto. Nesta aula, as rotas `/itens/` e `/itens/cbv/` renderizam a mesma tela e os mesmos dados; a primeira usa a FBV `lista_itens`, e a segunda usa `ItemListView`.

---

## 🖼️ 5. Criando os templates

Com `APP_DIRS = True` nas configurações do projeto, o Django procura templates dentro dos apps. Crie esta estrutura:

```text
core/
└── templates/
    └── core/
        ├── inicio.html
        ├── item_list.html
        └── item_detail.html
```

### `core/templates/core/inicio.html`

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Início | Aula Django</title>
</head>
<body>
    <h1>Views e URLs no Django</h1>
    <p>Esta página é atendida por uma Function-Based View.</p>
    <a href="{% url 'core:lista_itens' %}">Listar itens (FBV)</a>
    <a href="{% url 'core:lista_itens_cbv' %}">Listar itens (CBV)</a>
</body>
</html>
```

### `core/templates/core/item_list.html`

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Itens | Aula Django</title>
</head>
<body>
    <h1>Itens cadastrados</h1>
    <p>Esta página pode ser atendida por uma FBV ou por uma CBV.</p>

    <a href="{% url 'core:lista_itens' %}">Ver com FBV</a>
    <a href="{% url 'core:lista_itens_cbv' %}">Ver com CBV</a>
    <a href="{% url 'core:inicio' %}">Início</a>

    {% if itens %}
        <ul>
            {% for item in itens %}
                <li>
                    <a href="{% url 'core:detalhe_item' item.pk %}">{{ item.titulo }}</a>
                </li>
            {% endfor %}
        </ul>
    {% else %}
        <p>Nenhum item cadastrado. Crie um pelo painel administrativo.</p>
    {% endif %}
</body>
</html>
```

### `core/templates/core/item_detail.html`

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>{{ item.titulo }} | Aula Django</title>
</head>
<body>
    <h1>{{ item.titulo }}</h1>
    <p>{{ item.descricao|default:"Este item não possui descrição." }}</p>
    <p>Adicionado em: {{ item.criado_em|date:"d/m/Y H:i" }}</p>
    <a href="{% url 'core:lista_itens' %}">Voltar para a lista</a>
</body>
</html>
```

O conteúdo desses arquivos já está criado neste repositório. As tags `{% url %}` resolvem rotas pelo nome e as tags `{{ ... }}` exibem valores do contexto.

---

## ▶️ 6. Executando e testando

Se ainda não estiver com o ambiente virtual ativado, siga as instruções do [README principal](./README.md). No terminal, na pasta do projeto:

```bash
python manage.py migrate
python manage.py runserver
```

Abra as páginas:

| Funcionalidade | URL |
|---|---|
| Página inicial | [http://127.0.0.1:8000/](http://127.0.0.1:8000/) |
| Listagem com FBV | [http://127.0.0.1:8000/itens/](http://127.0.0.1:8000/itens/) |
| Listagem com CBV | [http://127.0.0.1:8000/itens/cbv/](http://127.0.0.1:8000/itens/cbv/) |
| Admin | [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) |

Cadastre um ou mais `Item` no Admin para visualizar registros nas listas. Clique em um título para abrir sua página de detalhes. Um identificador que não existe, como `/itens/9999/`, deve resultar em uma página 404.

Para executar os testes automatizados das rotas e views:

```bash
python manage.py test core
```

Os testes verificam as respostas HTTP, templates, itens apresentados pelas duas implementações da listagem e o caso de detalhe inexistente.

---

## ⚖️ 7. FBV e CBV: diferença prática

| Aspecto | FBV | CBV |
|---|---|---|
| Forma | Função que recebe `request` | Classe que herda de uma view |
| Entrada HTTP | A função controla explicitamente o fluxo | O método HTTP é encaminhado pela classe base |
| Melhor para | Lógica curta ou muito específica | Comportamentos comuns e reutilizáveis |
| Exemplo neste app | `lista_itens(request)` | `ItemListView(ListView)` |
| Rota | `path("itens/", views.lista_itens, ...)` | `path("itens/cbv/", ItemListView.as_view(), ...)` |

Nenhuma abordagem é sempre melhor. FBVs costumam ser diretas para iniciantes e para regras específicas. CBVs genéricas reduzem código repetitivo em operações comuns, como listar ou exibir um objeto. Escolha a abordagem que deixa o comportamento mais claro para o caso.

---

## 🧪 8. Exercícios para a turma

1. Adicione uma rota `/sobre/` com uma FBV e um template próprio.
2. Inclua na listagem a descrição de cada item.
3. Altere a view de detalhes para exibir uma mensagem amigável de retorno à lista.
4. Experimente acessar um identificador inexistente e observe o status 404.
5. Compare a quantidade de código necessária para acrescentar uma funcionalidade simples à FBV e à CBV.

---

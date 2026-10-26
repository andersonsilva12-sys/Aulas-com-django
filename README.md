# 🐍 Aula 3 — Views e URLs no Django

Este guia dá continuidade à sequência de estudos de Django. Nesta aula, vamos entender como o Django recebe uma requisição, encontra uma rota e executa uma **view** para devolver uma resposta.

No decorrer da prática, discutiremos acerca de **Class-Based Views (CBV)** e **Function-Based Views (FBV)**, criando uma versão primitiva da interface do gerenciador da biblioteca

## 📚 Sumário

- [1. Introdução e Atualização](#-1-introdução-e-atualização)
- [2. Teoria do fluxo de uma requisição](#-2-teoria-do-fluxo-de-uma-requisição)
- [3. Configurando as URLs](#-3-configurando-as-urls)
- [4. Construindo a aplicação passo a passo](#-4-construindo-a-aplicação-passo-a-passo)
- [5. Revisão](#️-5-revisão)
- [6. Exercício e exploração](#-6-exercício-e-exploração)

---

## 🎯 1. Introdução e Atualização

Nesta aula, vamos praticar:

- Como uma URL é associada a uma view;
- Como separar as rotas do projeto das rotas de uma aplicação;
- Como uma view recebe `request` e retorna uma resposta;
- Como ler parâmetros da URL, como o identificador de um livro;
- Como renderizar um template e enviar dados em seu contexto;
- Como implementar uma FBV e uma CBV em páginas com responsabilidades diferentes.

> **Importante — modelos usados nesta aula:** substituiremos as classes de modelo anteriores pelas classes `Livro` e `Autor`. Para esta aula, utilize **somente essas duas classes**: não mantenha nem acrescente o antigo model `Item` ao exemplo. `Livro` possui uma relação com `Autor`. Altere também o `admin.py` para que registre apenas essas classes.
> A migração altera a estrutura do banco e não transfere automaticamente dados antigos de `Item` para `Livro`; faça backup dos dados importantes antes de aplicá-la.

```python
from django.db import models


class Livro(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    autor = models.ForeignKey(
        "Autor",
        on_delete=models.CASCADE,
        related_name="livros",
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class Autor(models.Model):
    nome = models.CharField(max_length=100)
    registro = models.CharField(max_length=6, primary_key=True)

    def __str__(self):
        return self.nome
```

**Relembrando os models:**

- `models.Model` é a classe base dos models do Django.
- `CharField` armazena texto curto; `max_length=100` define o limite do título e do nome.
- `TextField` armazena texto longo; `blank=True` permite deixar a descrição vazia nos formulários.
- `ForeignKey` relaciona cada livro a um autor. `on_delete=models.CASCADE` faz com que a exclusão do autor também exclua seus livros; `related_name="livros"` permite acessar os livros de um autor como `autor.livros`.
- `DateTimeField(auto_now_add=True)` registra automaticamente a data e hora em que o livro foi criado.
- Em `Autor`, `primary_key=True` define `registro` como chave primária, em vez de usar um ID numérico gerado pelo Django.
- `__str__()` define a representação textual de cada registro, usada, por exemplo, no Admin.

Depois de substituir os models anteriores por `Livro` e `Autor`, gere e aplique as migrações antes de começar os testes com o servidor:

```bash
python manage.py makemigrations core
python manage.py migrate
```

---

## 🔁 2. Teoria do Fluxo de uma requisição

Anteriormente, com Node.js, compreendemos que a definição de cada rota era acompanhada com o req, res e as vezes next, processando tudo nela mesma.
```text
Navegador → URL com a Rota → Reconhecimento da rota → Processamento → Resposta
```
O caminho de uma página no Django pode ser resumido assim:

1. O navegador envia uma requisição HTTP para um endereço, por exemplo `/autores/`.
2. O configurador do projeto (`meu_projeto/urls.py`) procura uma rota correspondente.
3. A rota encaminha a requisição para uma view do app `core`.
4. A view pode consultar os models `Livro` e `Autor` e preparar dados.
5. A view retorna uma resposta HTTP.
6. O Django envia a resposta ao navegador.

```text
Navegador → URL do projeto → URL do app → View → Model/Template → Resposta
```

**View não é o arquivo HTML.** A view é um algorítimo que coordena o processamento da requisição e escolhe a resposta. O template é usado para apresentar os dados.

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

Vamos montar este arquivo por partes.

Comece por `core/urls.py` com a rota raiz:

```python
from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.inicio, name="inicio"),
]
```

- `from django.urls import path` importa a função que declara padrões de URL.
- `from . import views` importa o módulo `views.py`.
- `app_name = "core"` define o namespace das rotas, usado ao referenciá-las nos templates.
- `urlpatterns` é a lista que o Django percorre para encontrar uma rota.
- `path("", views.inicio, name="inicio")` associa a raiz do site (`""`, isto é, `/`) à view `inicio`.
- `name="inicio"` dá um nome estável à rota; os templates podem gerar seu endereço pelo nome.

---

## 🪜 4. Construindo a aplicação passo a passo

Faça os passos nesta ordem. Ao fim de cada etapa, teste no navegador antes de acrescentar a próxima parte.

### Passo 1 — Página inicial com uma FBV

#### 1.1. Crie a view inicial

Em `core/views.py`, comece somente com:

```python
from django.shortcuts import render


def inicio(request):
    return render(request, "core/inicio.html")
```

- `from django.shortcuts import render` importa o atalho que renderiza um template e devolve uma resposta HTTP.
- `def inicio(request):` declara uma função Python chamada `inicio` passando a requisição HTTP atual no parâmetro `request`.
- `render(request, "core/inicio.html")` procura e renderiza o template indicado, usando essa requisição.
- O retorno de `render()` é enviado pelo Django ao navegador como resposta.

Esta é uma **Function-Based View (FBV)** porque o comportamento está definido diretamente em uma função. Uma FBV é útil quando queremos controlar explicitamente o que acontece ao processar a requisição.

#### 1.2. Crie o template inicial

Crie `core/templates/core/inicio.html`:

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Início | Aula Django</title>
</head>
<body>
    <main>
        <h1>Views e URLs no Django</h1>
        <p>Esta página é atendida por uma Function-Based View.</p>
    </main>
</body>
</html>
```

O diretório `templates/core/` organiza os templates do app. Como `APP_DIRS = True` está habilitado nas configurações, o Django procura templates dentro dos apps.

#### 1.3. Teste

No terminal, na pasta que contém `manage.py`, inicie o servidor:

```bash
python manage.py runserver
```

A página deve exibir o título e a mensagem da FBV.

Se o servidor continuar aberto, o Django recarrega as alterações de código automaticamente. Interrompa-o com `Ctrl+C` apenas se precisar encerrar o processo.

---

### Passo 2 — Listagem de autores com uma CBV

Agora vamos acrescentar mais uma rota, view e seu template. Desta vez, não faremos a view do jeito anterior.

#### 2.1. Adicione a rota `autores/`

Atualize `core/urls.py`:

```python
from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("autores/", views.AutorListView.as_view(), name="lista_autores"),
]
```

`path("autores/", ...)` corresponde ao endereço `/autores/`. `views.AutorListView.as_view()` transforma a classe baseada em view numa chamada que o sistema de URLs pode executar. O nome `lista_autores` identifica a rota, e o namespace completo usado nos templates será `core:lista_autores`.

#### 2.2. Adicione a CBV

Atualize `core/views.py` para incluir a importação de `ListView` e `Autor`, e a classe:

```python
from django.shortcuts import render
from django.views.generic import ListView

from .models import Autor


def inicio(request):
    return render(request, "core/inicio.html")


class AutorListView(ListView):
    model = Autor
    template_name = "core/autor_list.html"
    context_object_name = "autores"
    ordering = ("nome", "registro")
```

- `ListView` é uma **Class-Based View (CBV)** genérica do Django para listar objetos.
- `class AutorListView(ListView):` cria uma classe de view especializada a partir de `ListView`.
- `model = Autor` informa qual model será consultado para montar a lista.
- `template_name` escolhe o template que exibirá a resposta.
- `context_object_name = "autores"` define o nome da variável que o template usará para percorrer a lista.
- `ordering` pede uma ordenação pelo nome e, em caso de empate, pelo registro.
- Diferente da FBV inicial, não escrevemos manualmente uma consulta nem chamamos `render()`: a classe genérica cuida do fluxo comum de listagem.

#### 2.3. Crie o template de autores

Crie `core/templates/core/autor_list.html`:

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Autores | Aula Django</title>
</head>
<body>
    <main>
        <h1>Autores cadastrados</h1>
        <p>Esta página é atendida por uma CBV.</p>
        <a href="{% url 'core:inicio' %}">Início</a>

        {% if autores %}
            <ul>
                {% for autor in autores %}
                    <li>
                        <strong>{{ autor.nome }}</strong> ({{ autor.registro }})
                        <ul>
                            {% for livro in autor.livros.all %}
                                <li>{{ livro.titulo }}</li>
                            {% empty %}
                                <li>Este autor ainda não possui livros cadastrados.</li>
                            {% endfor %}
                        </ul>
                    </li>
                {% endfor %}
            </ul>
        {% else %}
            <p>Nenhum autor cadastrado. Crie um pelo painel admin.</p>
        {% endif %}
    </main>
</body>
</html>
```

`{% if autores %}` verifica se a lista contém resultados. `{% for autor in autores %}` percorre-a; `{{ autor.nome }}` e `{{ autor.registro }}` exibem os campos. `autor.livros.all` segue a relação inversa `related_name="livros"` definida no model `Livro`. O bloco `{% empty %}` fornece uma alternativa quando aquele autor ainda não tem livros.

Repare que, por enquanto, `{{ livro.titulo }}` exibe apenas texto, mas futuramente podemos adicionar uma rota para acessar os detalhes do livro!

#### 2.4. Conecte a página inicial e teste

Agora que `lista_autores` existe, podemos acrescentar o link ao `core/templates/core/inicio.html`:

```html
<a href="{% url 'core:lista_autores' %}">Listar autores</a>
```

O `{% url 'core:lista_autores' %}` encontra o endereço pela combinação do namespace `core` com o nome da rota `lista_autores`.

Com o servidor em execução, atualize a página inicial e clique em **Listar autores**. Cadastre alguns autores e livros no Admin para observar a lista e a relação entre eles.

---

### Passo 3 — Detalhe do livro com uma FBV e parâmetro na URL

Por último, criaremos uma rota de detalhe sob o prefixo `livros/`. O identificador capturado na URL permite exibir um livro específico. Depois dessa rota existir, transformaremos o título na lista de autores em um link.

#### 3.1. Adicione a rota de detalhe

Inclua esta linha em `urlpatterns` de `core/urls.py`:

```python
path("livros/<int:pk>/", views.detalhe_livro, name="detalhe_livro"),
```

`<int:pk>` é um conversor de caminho: ele aceita um número inteiro e o passa à view como argumento `pk`. Por exemplo, `/livros/3/` chama `detalhe_livro` com `pk=3`. O `name` permite criar links para essa rota sem montar o endereço manualmente.

#### 3.2. Adicione a FBV de detalhe

Atualize `core/views.py` com a importação de `get_object_or_404` e `Livro`, além da função:

```python
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from .models import Autor, Livro


def inicio(request):
    return render(request, "core/inicio.html")


def detalhe_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    return render(request, "core/livro.html", {"livro": livro})


class AutorListView(ListView):
    model = Autor
    template_name = "core/autor_list.html"
    context_object_name = "autores"
    ordering = ("nome", "registro")
```

**O que foi acrescentado em relação à FBV `inicio`:**

- `get_object_or_404` busca um objeto e retorna uma resposta HTTP 404 se ele não existir.
- `Livro` é importado de `core.models`; `Autor` permanece importado porque a CBV continua listando esse model.
- O parâmetro `pk` recebe o inteiro capturado no padrão da URL.
- `Livro.objects` é o gerenciador de consultas do model `Livro`; `get_object_or_404(Livro, pk=pk)` procura o livro cuja chave primária corresponde ao valor recebido.
- `render()` continua gerando a resposta com um template, mas agora recebe um dicionário de contexto: `{"livro": livro}` disponibiliza o objeto no template com o nome `livro`.

#### 3.3. Crie o template do livro

Crie `core/templates/core/livro.html`:

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ livro.titulo }} | Aula Django</title>
</head>
<body>
    <main>
        <h1>{{ livro.titulo }}</h1>
        <p>{{ livro.descricao|default:"O livro não possui descrição." }}</p>
        <p>Autor: {{ livro.autor.nome }}</p>
        <p>Adicionado em: {{ livro.criado_em|date:"d/m/Y H:i" }}</p>
        <p>Esta página é atendida por uma Function-Based View.</p>
        <a href="{% url 'core:lista_autores' %}">Voltar para a lista de autores</a>
    </main>
</body>
</html>
```

`{{ livro.titulo }}` e as demais expressões acessam os valores enviados no contexto. O filtro `default` fornece um texto caso a descrição esteja vazia. O filtro `date` formata a data de criação.

#### 3.4. Transforme o título em link e teste

Volte a `core/templates/core/autor_list.html` e substitua:

```html
{{ livro.titulo }}
```

por:

```html
<a href="{% url 'core:detalhe_livro' livro.pk %}">{{ livro.titulo }}</a>
```

Agora o nome da rota `core:detalhe_livro` gera o endereço do detalhe e `livro.pk` fornece o identificador do livro atual do loop. Clique em um título na lista de autores; a página de detalhes deve mostrar título, descrição, autor e data. Acesse também um ID inexistente, como `/livros/9999/`, e confirme que o Django responde com 404.

---

## ⚖️ 5. Revisão: FBV e CBV

| Aspecto | FBV | CBV |
|---|---|---|
| Forma | Função Python que recebe `request` | Classe que herda de uma view |
| Exemplo desta aula | `inicio(request)` e `detalhe_livro(request, pk)` | `AutorListView(ListView)` |
| Como definimos o comportamento | Escrevemos explicitamente a busca, o contexto e a resposta | Configuramos atributos; a classe genérica executa a listagem |
| Rota | `path("livros/<int:pk>/", views.detalhe_livro, ...)` | `path("autores/", views.AutorListView.as_view(), ...)` |

Uma FBV não é necessariamente melhor ou pior que uma CBV. A FBV deixa explícita a sequência de passos e é conveniente para comportamentos específicos. A CBV genérica reduz código repetitivo quando a operação corresponde a um padrão comum, como listar objetos. Neste exemplo, as duas abordagens atendem páginas diferentes para manter a aula objetiva; compare como cada tipo é declarado e conectado à URL.

---

## 🧪 6. Exercício e exploração

1. Crie uma rota da forma que preferir e escolha se será uma view FBV ou CBV.
2. Agora crie uma segunda rota replicando a anterior mas sendo do tipo de view não escolhido. Compare os usos
3. Altere a ordenação de autores e ou dos livros.

---

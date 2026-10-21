from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from .models import Autor, Livro


def inicio(request):
    # Mostra a página inicial da aplicação.
    return render(request, "core/inicio.html")


def detalhe_livro(request, pk):
    # Mostra um livro ou retorna 404 quando ele não existe.
    livro = get_object_or_404(Livro, pk=pk)
    return render(request, "core/livro.html", {"livro": livro})


class AutorListView(ListView):
    # Lista os autores usando uma Class-Based View genérica.

    model = Autor
    template_name = "core/autor_list.html"
    context_object_name = "autores"
    ordering = ("nome", "registro")

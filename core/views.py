from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

from .models import Autor, Livro

@login_required(login_url="core:login")
def inicio(request):#type:ignore
    # Mostra a página inicial da aplicação.
    return render(request, "core/inicio.html")#type:ignore

@login_required(login_url="core:login")
def area_restrita(request):#type:ignore
    return render(request, "core/area_restrita.html")#type:ignore

def detalhe_livro(request, pk):#type:ignore
    # Mostra um livro ou retorna 404 quando ele não existe.
    livro = get_object_or_404(Livro, pk=pk)
    return render(request, "core/livro.html", {"livro": livro})#type:ignore


class AutorListView(ListView):
    # Lista os autores usando uma Class-Based View genérica.

    model = Autor
    template_name = "core/autor_list.html"
    context_object_name = "autores"
    ordering = ("nome", "registro")

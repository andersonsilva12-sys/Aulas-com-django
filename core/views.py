from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from .models import Item


def inicio(request):
    # Mostra a página inicial da aplicação.
    return render(request, "core/inicio.html")


def lista_itens(request):
    # Lista os itens usando uma Function-Based View.
    itens = Item.objects.all().order_by("-criado_em", "-pk")
    return render(request, "core/item_list.html", {"itens": itens})


def detalhe_item(request, pk):
    # Mostra um item ou retorna 404 quando ele não existe.
    item = get_object_or_404(Item, pk=pk)
    return render(request, "core/item_detail.html", {"item": item})


class ItemListView(ListView):
    # Lista os mesmos itens usando uma Class-Based View genérica.

    model = Item
    template_name = "core/item_list.html"
    context_object_name = "itens"
    ordering = ("-criado_em", "-pk")

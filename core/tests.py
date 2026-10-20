from django.test import TestCase
from django.urls import reverse

from .models import Item


class ViewsTests(TestCase):
    def setUp(self):
        self.item = Item.objects.create(
            titulo="Primeiro item",
            descricao="Item criado para testar as views.",
        )

    def test_pagina_inicial(self):
        response = self.client.get(reverse("core:inicio"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/inicio.html")

    def test_lista_fbv_exibe_itens(self):
        response = self.client.get(reverse("core:lista_itens"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/item_list.html")
        self.assertContains(response, self.item.titulo)
        self.assertIn(self.item, response.context["itens"])

    def test_lista_cbv_exibe_itens(self):
        response = self.client.get(reverse("core:lista_itens_cbv"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/item_list.html")
        self.assertContains(response, self.item.titulo)
        self.assertIn(self.item, response.context["itens"])

    def test_detalhe_fbv_exibe_item(self):
        response = self.client.get(
            reverse("core:detalhe_item", args=[self.item.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/item_detail.html")
        self.assertContains(response, self.item.titulo)

    def test_detalhe_de_item_inexistente_retorna_404(self):
        response = self.client.get(reverse("core:detalhe_item", args=[9999]))

        self.assertEqual(response.status_code, 404)

from django.test import TestCase
from django.urls import reverse

from .models import Autor, Livro


class ViewsTests(TestCase):
    def setUp(self):
        self.autor = Autor.objects.create(
            registro="A00001",
            nome="Ada Lovelace",
        )
        self.livro = Livro.objects.create(
            titulo="Introdução ao Django",
            descricao="Livro criado para testar as views.",
            autor=self.autor,
        )

    def test_pagina_inicial(self):
        response = self.client.get(reverse("core:inicio"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/inicio.html")

    def test_detalhe_livro_exibe_titulo_e_autor(self):
        response = self.client.get(
            reverse("core:detalhe_livro", args=[self.livro.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/livro.html")
        self.assertContains(response, self.livro.titulo)
        self.assertContains(response, self.autor.nome)

    def test_detalhe_de_livro_inexistente_retorna_404(self):
        response = self.client.get(reverse("core:detalhe_livro", args=[9999]))

        self.assertEqual(response.status_code, 404)

    def test_lista_autores_exibe_autor_e_livros(self):
        response = self.client.get(reverse("core:lista_autores"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/autor_list.html")
        self.assertContains(response, self.autor.nome)
        self.assertContains(response, self.livro.titulo)
        self.assertIn(self.autor, response.context["autores"])

    def test_lista_autor_sem_livros_exibe_mensagem(self):
        Autor.objects.create(
            registro="A00002",
            nome="Grace Hopper",
        )

        response = self.client.get(reverse("core:lista_autores"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Este autor ainda não possui livros cadastrados.")

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
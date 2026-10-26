from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("autores/", views.AutorListView.as_view(), name="lista_autores"),
    path("livros/<int:pk>/", views.detalhe_livro, name="detalhe_livro"),
]

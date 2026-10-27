from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.inicio, name="inicio"),#type:ignore
    path("autores/", views.AutorListView.as_view(), name="lista_autores"),
    path("livros/<int:pk>/", views.detalhe_livro, name="detalhe_livro"),#type:ignore
    
    path("login/", auth_views.LoginView.as_view(template_name="core/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("area_restrita", views.area_restrita, name="area_restrita")#type:ignore
]

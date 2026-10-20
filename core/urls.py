from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("itens/", views.lista_itens, name="lista_itens"),
    path("itens/cbv/", views.ItemListView.as_view(), name="lista_itens_cbv"),
    path("itens/<int:pk>/", views.detalhe_item, name="detalhe_item"),
]

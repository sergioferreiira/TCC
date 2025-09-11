from django.urls import path
from . import views

app_name = "financas"

urlpatterns = [
    path("", views.transacao_list, name="lista"),
    path("nova/", views.transacao_create, name="transacao_create"),
    path("editar/<int:pk>/", views.transacao_update, name="transacao_update"),
    path("deletar/<int:pk>/", views.transacao_delete, name="transacao_delete"),
    path("conta/", views.conta_edit, name="conta_edit"),
]

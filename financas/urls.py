from django.urls import path
from . import views

app_name = 'financas'

urlpatterns = [
    path('', views.transacao_list, name='lista'),
    path('nova/', views.transacao_create, name='criar'),
    path('<int:pk>/editar/', views.transacao_update, name='editar'),
    path('<int:pk>/excluir/', views.transacao_delete, name='excluir'),

    path('conta/', views.conta_edit, name='conta'),

    path('recorrencias/', views.recorrencia_list, name='recorrencias'),
    path('recorrencias/nova/', views.recorrencia_create, name='recorrencia_nova'),
    path('recorrencias/<int:pk>/editar/', views.recorrencia_update, name='recorrencia_editar'),
    path('recorrencias/<int:pk>/toggle/', views.recorrencia_toggle, name='recorrencia_toggle'),
]

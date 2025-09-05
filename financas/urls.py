from django.urls import path
from . import views

app_name = 'financas'

urlpatterns = [
    path('', views.transacao_list, name='lista'),
    path('nova/', views.transacao_create, name='criar'),
    path('<int:pk>/editar/', views.transacao_update, name='editar'),
    path('<int:pk>/excluir/', views.transacao_delete, name='excluir'),
    path('conta/', views.conta_edit, name='conta'),
]

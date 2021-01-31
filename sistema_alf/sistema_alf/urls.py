from django.contrib import admin
from django.urls import path, include
from app_alf.api import viewsets
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = format_suffix_patterns([
    # path('admin/', admin.site.urls),
    # rotas para inserção de dados
    path('SistemaALF/adicionarQuestaoProva', viewsets.adicionarQuestaoProva),
    path('SistemaALF/adicionarNovaProva', viewsets.adicionarNovaProva),
    path('SistemaALF/adicionarRespostaQuestao', viewsets.adicionarRespostaQuestao),
    path('SistemaALF/adicionarNovoAluno', viewsets.adicionarNovoAluno),
    path('SistemaALF/adicionarAlunoProva', viewsets.adicionarAlunoProva),
    # rotas para pesquisa, alteração e exclusão
    path('SistemaALF/Aluno/<int:pk>', viewsets.Aluno),
    path('SistemaALF/Prova/<int:pk>', viewsets.Prova),
    path('SistemaALF/Questao/<int:pk>', viewsets.Questao),
    path('SistemaALF/Resposta/<int:pk>', viewsets.Resposta),
    # rotas para obtenção de dados
    path('SistemaALF/verAlunosAprovados', viewsets.verAlunosAprovados),
    path('SistemaALF/verProvasSemGabarito', viewsets.verProvas),
    path('SistemaALF/verProvasComGabarito', viewsets.verProvasGabarito),
    path('SistemaALF/verNotas', viewsets.verNotas),
    path('SistemaALF/verRespostas', viewsets.verRespostas)
])
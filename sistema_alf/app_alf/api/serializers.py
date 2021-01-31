from rest_framework import serializers
from app_alf import models
from django.db.models import Sum

# Serializador para POST, PUT e DELETE de Prova
class ProvaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Prova
        fields = '__all__'

# Serializador para POST, PUT e DELETE de Aluno
class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Aluno
        fields = '__all__'

# Serializador para POST e DELETE de Questao
class QuestaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Questao
        fields = '__all__'

# Serializador para POST e DELETE de Resposta
class RespostaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Resposta
        fields = '__all__'

# Serializador para POST e DELETE de AlunosProva
class AlunosProvaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AlunosProva
        fields = '__all__'

# Serializador para GET de Alunos
class DetalhesAlunoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Aluno
        fields = ('aluno_id', 'nome')

# Serializador para GET de Questoes sem mostrar o gabarito
class DetalhesQuestaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Questao
        fields = ('questao_id','descricao','peso')

# Serializador para GET de Respostas
class DetalhesRespostaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Resposta
        fields = ('resposta_id', 'resposta')

# Serializador para GET de Provas com as Questoes com gabarito
class ProvaComGabaritoSerializer(serializers.HyperlinkedModelSerializer):
    questoes = QuestaoSerializer(many=True, read_only=True)

    class Meta:
        model = models.Prova
        fields = ('prova_id', 'assunto', 'questoes')

# Serializador para GET de Provas com as Questoes sem gabarito
class ProvaSemGabaritoSerializer(serializers.HyperlinkedModelSerializer):
    questoes = DetalhesQuestaoSerializer(many=True, read_only=True)

    class Meta:
        model = models.Prova
        fields = ('prova_id', 'assunto', 'questoes')

# Serializador para GET de Respostas com Aluno
class DetalhesRespostaComAlunoSerializer(serializers.ModelSerializer):
    aluno = AlunoSerializer(read_only=True)

    class Meta:
        model = models.Resposta
        fields = ('resposta_id', 'resposta', 'aluno')

# Serializador para GET de Questao com as respostas
class DetalhesQuestaoComRespostaSerializer(serializers.ModelSerializer):
    respostas = DetalhesRespostaComAlunoSerializer(many=True, read_only=True)

    class Meta:
        model = models.Questao
        fields = ('questao_id','descricao','peso', 'respostas')

# Serializador para GET de Provas com as Questoes e suas respostas
class RespostasAlunosSerializer(serializers.HyperlinkedModelSerializer):
    questoes = DetalhesQuestaoComRespostaSerializer(many=True, read_only=True)

    class Meta:
        model = models.Prova
        fields = ('prova_id', 'assunto', 'questoes')

# Serializador para GET de Provas dos Alunos com as notas
class ProvasAlunoSerializer(serializers.HyperlinkedModelSerializer):
    prova = ProvaSerializer(read_only=True)

    class Meta:
        model = models.AlunosProva
        fields = ('prova', 'nota')

# Serializador para GET de Alunos com suas Provas e suas notas
class NotasAlunoSerializer(serializers.HyperlinkedModelSerializer):
    notas = ProvasAlunoSerializer(many=True, read_only=True)
    aprovado = serializers.SerializerMethodField()

    class Meta:
        model = models.Aluno
        fields = ('aluno_id', 'nome', 'notas', 'media', 'aprovado')

    def get_aprovado(self, obj):
        a = False
        aluno = models.Aluno.objects.get(aluno_id = obj.aluno_id)
        if aluno.media > 7 :
            a = True
        return a
from app_alf.api import serializers
from app_alf import models
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import Sum

# Método para adicionar nova prova
@api_view(['POST'])
def adicionarNovaProva(request, format=None):
    serializer = serializers.ProvaSerializer(data=request.data)
    # Verificar se os dados são válidos
    if serializer.is_valid():
        # Salvar a nova prova
        serializer.save()
        return Response({"resultado": "ok", "detalhes": "Prova adicionada com sucesso!"}, status=status.HTTP_201_CREATED)     
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Método para adicionar Questão a prova
@api_view(['POST'])
def adicionarQuestaoProva(request, format=None):
    serializer = serializers.QuestaoSerializer(data=request.data)
    # Verificar se os dados são válidos
    if serializer.is_valid():
        #notaMaxProva = int(serializer.validated_data.get('peso'))
        # Buscar todas as questões da prova referente a nova questão
        questoesProva = models.Questao.objects.filter(prova = serializer.validated_data.get('prova'))
        # Verificar se a prova possui questões
        #   Se não tiver, a questão poderá ser salva
        if questoesProva.exists():
            # Se sim, deverá ser analisado se a nota da prova ultrapasse o limite de 10
            # Somar os pesos das questões para encontrar a nota final da prova
            notaProva = questoesProva.aggregate(Sum('peso'))
            # Somar a nota final da prova com o peso da nova questão
            notaMaxProva = notaProva['peso__sum'] + int(serializer.validated_data.get('peso'))
            # Verificar se a nova questão deixará a prova com uma nota final maior que 10
            #   Se não, a questão poderá ser salva
            if notaMaxProva > 10:
                # Se sim, impedir que a nova questão seja salva
                return Response({"resultado": "erro", "detalhes": "Não é possível adicionar esta questão à prova pois seu peso irá deixar a prova com nota superior a 10!"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        # Salvar a nova questão
        serializer.save()
        return Response({"resultado": "ok", "detalhes": "Questão adicionada com sucesso!"}, status=status.HTTP_201_CREATED)     
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Método para adicionar uma Resposta à Questão
@api_view(['POST'])
def adicionarRespostaQuestao(request, format=None):
    serializer = serializers.RespostaSerializer(data=request.data)
    # Verificar se os dados são válidos
    if serializer.is_valid():
        # Verificar se a Questao já foi respondida
        #   Se não, a resposta pode ser salva
        respostaSalva = models.Resposta.objects.filter(questao = serializer.validated_data.get('questao')).filter(aluno = serializer.validated_data.get('aluno'))
        if respostaSalva.exists() :
            # Se sim, impedir que a questão seja respondida novamente
            return Response({"resultado": "erro", "detalhes": "Questão já respondida!"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        # Salvar a resposta
        serializer.save()
        # Realizar operações para atualizar a nota do Aluno na prova
        # Buscar o Aluno da resposta
        alunoResposta = models.Aluno.objects.get(aluno_id = serializer.data.get('aluno'))
        # Buscar a questao respondida
        questaoRespondida = models.Questao.objects.get(questao_id = serializer.data.get('questao'))
        # Buscar a prova analisada
        provaAnalisada = questaoRespondida.prova
        # Buscar a resposta do aluno na prova
        respostaAluno = serializer.data
        # Verificar a resposta
        # Se o aluno não acertou a questão, apenas será salvo a resposta
        if respostaAluno.get('resposta') == questaoRespondida.gabarito :
            # Se o aluno acertou a questão, deverá ser atualizado sua nota e sua média
            # Verificar se o aluno está cadastrado na prova
            provaAluno = models.AlunosProva.objects.filter(aluno = alunoResposta.aluno_id).filter(prova = provaAnalisada)
            if provaAluno.exists() :
                # Se ele estiver, deverá ser atualizado sua nota na prova
                provaAluno = models.AlunosProva.objects.filter(aluno = alunoResposta.aluno_id).get(prova = provaAnalisada)
                provaAluno.nota += questaoRespondida.peso
                provaAluno.save()
            else:
                # Se ele não estiver, deverá ser cadastrado na Prova
                NovoProvaAluno = models.AlunosProva(aluno = alunoResposta, prova = provaAnalisada)
                NovoProvaAluno.save()
                # Salvar a nota do aluno na prova
                NovoProvaAluno.nota = questaoRespondida.peso
                NovoProvaAluno.save()
            # Realizar operações para calcular a média do Aluno
            # Buscar as provas do Aluno
            provasAluno = models.AlunosProva.objects.filter(aluno = alunoResposta)
            # Somar as notas das provas
            notaTotal = provasAluno.aggregate(Sum('nota'))
            # Somar o total de provas que o aluno está cadastrado
            totalProvas = provasAluno.count()
            # Calcular a média do aluno
            media = notaTotal['nota__sum']/totalProvas
            # Salvar o aluno com a média atualizada
            alunoResposta.media = media
            alunoResposta.save()
        return Response({"resultado": "ok", "detalhes": "Resposta adicionada com sucesso!"}, status=status.HTTP_201_CREATED)     
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Método para adicionar um novo Aluno
@api_view(['POST'])
def adicionarNovoAluno(request, format=None):
    serializer = serializers.AlunoSerializer(data=request.data)
    # Verificar se os dados são válidos
    if serializer.is_valid():
        # Somar a quantidade de alunos cadastrados
        totalAlunos = models.Aluno.objects.all().count()
        # Verificar se já existem 100 alunos cadastrados
        #   Se não, o aluno poderá ser salvo
        if totalAlunos == 100:
            # Se sim, impedir que o aluno seja salvo
            return Response({"resultado": "erro", "detalhes": "Limite de alunos cadastrados alcançado!"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        # Salvar o novo aluno
        serializer.save()
        return Response({"resultado": "ok", "detalhes": "Aluno adicionado com sucesso!"}, status=status.HTTP_201_CREATED)     
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Método para adicionar Aluno na Prova
@api_view(['POST'])
def adicionarAlunoProva(request, format=None):
    serializer = serializers.AlunosProvaSerializer(data=request.data)
    # Verificar se os dados são válidos
    if serializer.is_valid():
        # Salvar o aluno na prova
        serializer.save()
        return Response({"resultado": "ok", "detalhes": "Aluno adicionado na Prova com sucesso!"}, status=status.HTTP_201_CREATED)     
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Método para pesquisar, alterar ou excluir uma Prova
@api_view(['GET', 'PUT', 'DELETE'])
def Prova(request, pk, format=None):
    try:
        # Verificar se a prova consultada existe
        #   Se sim, os métodos poderão ser executados
        provaSelecionada = models.Prova.objects.get(prova_id=pk) 
    except models.Prova.DoesNotExist:
        #   Se não, impedir que os métodos sejam executados
        return Response({"resultado": "erro", "detalhes": "Esta prova não existe!"}, status=status.HTTP_404_NOT_FOUND) 
    # Verificar se a requisição é do tipo GET
    if request.method == 'GET':
        # Se sim, retornar os dados da prova selecionada
        serializer = serializers.ProvaSerializer(provaSelecionada) 
        return Response(serializer.data, status=status.HTTP_200_OK) 
    # Verificar se a requisição é do tipo PUT 
    elif request.method == 'PUT': 
        serializer = serializers.ProvaSerializer(provaSelecionada, data=request.data)
        # Se sim, verificar se os dados são válidos
        if serializer.is_valid():
            # Se sim, alterar os dados da prova
            serializer.save() 
            return Response({"resultado": "ok", "detalhes": "Esta prova foi atualizada!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    # Verificar se a requisição é do tipo DELETE
    elif request.method == 'DELETE':
        # Se sim, realizar operações para recalcular as médias dos Alunos
        # Buscar os alunos que responderam esta prova
        alunosProva = models.AlunosProva.objects.filter(prova = provaSelecionada)
        #   Se nenhum aluno respondeu esta prova, ela poderá ser excluída
        #   Se já houver respostas para a prova, deverá ser recalculadas as médias dos alunos
        for a in alunosProva:
            # Buscar as provas do Aluno sem a que será excluída
            provasAluno = models.AlunosProva.objects.filter(aluno = a.aluno).exclude(prova = provaSelecionada)
            # Buscar o aluno da prova
            aluno = a.aluno
            # Definir a média como 0, caso o aluno não tenha respondido outra prova além da que será excluída
            media = 0.0
            # Verificar se o aluno respondeu outras provas
            #   Se não, a média do aluno será 0
            if provasAluno.exists() :
                # Se sim, deverá ser calculado a média
                # Somar as notas das provas
                notaTotal = provasAluno.aggregate(Sum('nota'))
                # Somar o total de provas que o aluno está cadastrado
                totalProvas = provasAluno.count()
                # Calcular a média do aluno
                media = notaTotal['nota__sum']/totalProvas
            # Salvar o aluno com a média atualizada
            aluno.media = media
            aluno.save()
        # Excluir a prova selecionada
        provaSelecionada.delete()
        return Response({"resultado": "ok", "detalhes": "Esta prova foi excluída!"}, status=status.HTTP_200_OK)

# Método para pesquisar, alterar ou excluir um Aluno
@api_view(['GET', 'PUT', 'DELETE'])
def Aluno(request, pk, format=None):
    try:
        # Verificar se o aluno consultado existe
        #   Se sim, os métodos poderão ser executados
        aluno = models.Aluno.objects.get(aluno_id=pk) 
    except models.Aluno.DoesNotExist:
        #   Se não, impedir que os métodos sejam executados
        return Response({"resultado": "erro", "detalhes": "Este Aluno não existe!"}, status=status.HTTP_404_NOT_FOUND) 
    # Verificar se a requisição é do tipo GET
    if request.method == 'GET':
        # Se sim, retornar os dados do aluno selecionado
        serializer = serializers.AlunoSerializer(aluno) 
        return Response(serializer.data, status=status.HTTP_200_OK) 
    # Verificar se a requisição é do tipo PUT
    elif request.method == 'PUT':
        serializer = serializers.AlunoSerializer(aluno, data=request.data)
        # Se sim, verificar se os dados são válidos
        if serializer.is_valid(): 
            # Se sim, alterar os dados do aluno
            serializer.save() 
            return Response({"resultado": "ok", "detalhes": "Este Aluno foi atualizado!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    # Verificar se a requisição é do tipo DELETE
    elif request.method == 'DELETE':
        # Se sim, excluir o aluno selecionado
        aluno.delete() 
        return Response({"resultado": "ok", "detalhes": "Este aluno foi excluído!"}, status=status.HTTP_200_OK)

# Método para pesquisar ou excluir uma Questão
@api_view(['GET', 'DELETE'])
def Questao(request, pk, format=None):
    try:
        # Verificar se a questao consultada existe
        #   Se sim, os métodos poderão ser executados
        questaoSelecionada = models.Questao.objects.get(questao_id=pk)
    except models.Questao.DoesNotExist:
        #   Se não, impedir que os métodos sejam executados
        return Response({"resultado": "erro", "detalhes": "Esta questão não existe!"}, status=status.HTTP_404_NOT_FOUND) 
    # Verificar se a requisição é do tipo GET
    if request.method == 'GET':
        # Se sim, retornar os dados da questão selecionada
        serializer = serializers.QuestaoSerializer(questaoSelecionada) 
        return Response(serializer.data, status=status.HTTP_200_OK) 
    # Verificar se a requisição é do tipo DELETE
    elif request.method == 'DELETE':
        # Se sim, deverá ser recalculada a nota dos alunos na prova
        # Buscar as respostas da questão
        respostasQuestao = models.Resposta.objects.filter(questao = questaoSelecionada)
        # Verificar se a questão já foi respondida
        #   Se não foi, a questão poderá ser excluída
        if respostasQuestao.exists() :
            # Se já foi respondida, realizar operações para atualizar as notas dos Alunos na prova
            # Buscar todas as provas respondidas que possuem a questao selecionada
            provasAluno = models.AlunosProva.objects.filter(prova = questaoSelecionada.prova)
            # Atualizar as notas dos alunos na prova
            for p in provasAluno :
                # Buscar a resposta do aluno na prova, se ele chegou a responder a questão
                try:
                    respostaQuestao = models.Resposta.objects.filter(aluno = p.aluno).get(questao = questaoSelecionada)
                    # Verificar se o aluno acertou a resposta
                    if respostaQuestao.resposta == questaoSelecionada.gabarito :
                        # Se sim, atualizar a nota
                        p.nota -= questaoSelecionada.peso
                        p.save()
                except models.Resposta.DoesNotExist:
                    pass
            # Atualizar a média dos alunos
            for r in respostasQuestao :
                # Buscar o Aluno da resposta
                alunoResposta = models.Aluno.objects.get(aluno_id = r.aluno_id)
                # Buscar as provas do Aluno
                provasAluno = models.AlunosProva.objects.filter(aluno = alunoResposta)
                # Somar as notas das provas
                notaTotal = provasAluno.aggregate(Sum('nota'))
                # Somar o total de provas que o aluno está cadastrado
                totalProvas = provasAluno.count()
                # Calcular a média do aluno
                media = notaTotal['nota__sum']/totalProvas
                # Salvar o aluno com a média atualizada
                alunoResposta.media = media
                alunoResposta.save()
        # Excluir a questão selecionada
        questaoSelecionada.delete()
        return Response({"resultado": "ok", "detalhes": "Esta questão foi excluída!"}, status=status.HTTP_200_OK)

# Método para pesquisar ou excluir uma Resposta
@api_view(['GET', 'DELETE'])
def Resposta(request, pk, format=None):
    try:
        # Verificar se a resposta consultada existe
        #   Se sim, os métodos poderão ser executados
        respostaSelecionada = models.Resposta.objects.get(resposta_id=pk) 
    except models.Resposta.DoesNotExist:
        #   Se não, impedir que os métodos sejam executados
        return Response({"resultado": "erro", "detalhes": "Esta resposta não existe!"}, status=status.HTTP_404_NOT_FOUND) 
    # Verificar se a requisição é do tipo GET
    if request.method == 'GET':
        # Se sim, retornar os dados da resposta selecionada
        serializer = serializers.RespostaSerializer(respostaSelecionada) 
        return Response(serializer.data, status=status.HTTP_200_OK) 
    # Verificar se a requisição é do tipo DELETE
    elif request.method == 'DELETE':
        # Realizar operações para atualizar a nota do Aluno na prova
        # Buscar o aluno que fez a resposta
        alunoResposta = respostaSelecionada.aluno
        # Buscar a prova respondida
        provaRespondida = respostaSelecionada.questao.prova
        # Verificar se o aluno acertou a questão
        #   Se não, a resposta pode ser excluída
        if respostaSelecionada.resposta == respostaSelecionada.questao.gabarito :
            # Se sim, atualizar a nota do aluno
            # Buscar a nota do aluno na prova
            try:
                provaAluno = models.AlunosProva.objects.filter(aluno = alunoResposta).get(prova = provaRespondida)
                provaAluno.nota -= respostaSelecionada.questao.peso
                provaAluno.save()
            except models.AlunosProva.DoesNotExist:
                pass
            # Realizar operações para atualizar a média do aluno
            # Buscar as provas do aluno
            provasAluno = models.AlunosProva.objects.filter(aluno = alunoResposta)
            # Somar as notas das provas
            notaTotal = provasAluno.aggregate(Sum('nota'))
            # Somar o total de provas que o aluno está cadastrado
            totalProvas = provasAluno.count()
            # Calcular a média do aluno
            media = notaTotal['nota__sum']/totalProvas
            # Salvar o aluno com a média atualizada
            alunoResposta.media = media
            alunoResposta.save()
        # Excluir a resposta selecionada
        respostaSelecionada.delete()
        return Response({"resultado": "ok", "detalhes": "Esta resposta foi excluída!"}, status=status.HTTP_200_OK)

# Método para retornar todos os Alunos com Media maior que 7
@api_view(['GET'])
def verAlunosAprovados(format=None):
    alunos = models.Aluno.objects.filter(media__gt = 7.0)
    serializer = serializers.AlunoSerializer(alunos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Método para retornar todas as Provas sem o gabarito
@api_view(['GET'])
def verProvas(format=None):
    provas = models.Prova.objects.all()
    serializer = serializers.ProvaSemGabaritoSerializer(provas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Método para retornar todas as Provas com o gabarito
@api_view(['GET'])
def verProvasGabarito(format=None):
    provas = models.Prova.objects.all()
    serializer = serializers.ProvaComGabaritoSerializer(provas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Método para retornar todas os Alunos com suas médias e notas de prova
@api_view(['GET'])
def verNotas(format=None):
    alunos = models.Aluno.objects.select_related().all()
    serializer = serializers.NotasAlunoSerializer(alunos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Método para retornar todas as Provas com suas Questões e suas Respostas
@api_view(['GET'])
def verRespostas(format=None):
    provas = models.Prova.objects.select_related().all()
    serializer = serializers.RespostasAlunosSerializer(provas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
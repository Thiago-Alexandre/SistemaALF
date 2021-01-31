from django.db import models

# Modelo da classe Prova
class Prova(models.Model):
    prova_id = models.IntegerField(primary_key=True, editable= False)
    assunto = models.CharField(max_length=255, null=False)

    def __unicode__(self):
        return self.assunto

# Modelo da classe Aluno
class Aluno(models.Model):
    aluno_id = models.IntegerField(primary_key=True, editable= False)
    nome = models.CharField(max_length=100, null=False)
    media = models.DecimalField(max_digits=3, decimal_places=1, default=0, editable=False)

    def __unicode__(self):
        return self.nome

# Modelo da classe Questao
class Questao(models.Model):
    GABARITO_CHOICES = (
        ("A", "Letra A"),
        ("B", "Letra B"),
        ("C", "Letra C"),
        ("D", "Letra D"),
        ("E", "Letra E")
    )
    questao_id = models.IntegerField(primary_key=True, editable= False)
    descricao = models.CharField(max_length=255, null=False)
    gabarito = models.CharField(max_length=1, choices=GABARITO_CHOICES, null=False)
    peso = models.IntegerField(null=False)
    prova = models.ForeignKey("Prova", on_delete=models.CASCADE, related_name='questoes', null=False)

    def __unicode__(self):
        return self.descricao

# Modelo da classe Resposta
class Resposta(models.Model):
    RESPOSTA_CHOICES = (
        ("A", "Letra A"),
        ("B", "Letra B"),
        ("C", "Letra C"),
        ("D", "Letra D"),
        ("E", "Letra E")
    )
    resposta_id = models.IntegerField(primary_key=True, editable= False)
    resposta = models.CharField(max_length=1, choices=RESPOSTA_CHOICES, null=False)
    questao = models.ForeignKey("Questao", on_delete=models.CASCADE, related_name='respostas', null=False)
    aluno = models.ForeignKey("Aluno", on_delete=models.CASCADE, related_name='respostas', null=False)

    def __unicode__(self):
        return self.resposta

# Modelo da classe AlunosProva
class AlunosProva(models.Model):
    aluno = models.ForeignKey("Aluno", on_delete=models.CASCADE, related_name='notas', null=False)
    prova = models.ForeignKey("Prova", on_delete=models.CASCADE, related_name='notas', null=False)
    nota = models.IntegerField(default=0, editable=False)

    def __unicode__(self):
        return self.nota
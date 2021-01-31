# SistemaALF

## API Rest para Gerenciamento Escolar

### Problema

A escola Alf aplica provas de múltipla escolha para os alunos. A nota do aluno na prova é determinada pela média ponderada das questões com os pesos de cada questão. Cada questão correta soma 1 ponto multiplicada pelo peso e cada questão errada 0. A nota final é a média aritmética das notas de todas as provas.

#### Requisitos obrigatórios:

Uma API HTTP que permita à escola:

* Cadastrar o gabarito de cada prova;
* Cadastrar as respostas de cada aluno para cada prova;
* Verificar a nota final de cada aluno;
* Listar os alunos aprovados;

#### Restrições

* A nota total da prova é sempre maior que 0 e menor que 10.
* A quantidade máxima de alunos é 100.
* O peso de cada questão é sempre um inteiro maior que 0.
* Os alunos aprovados tem média de notas maior do que 7.
* A entrada e saída de dados deverá ser em JSON.

### Implementação

O Sistema ALF foi desenvolvido na linguagem Python, versão 3.9, utilizando Django RestFramework. A modelagem de dados foi projetada conforme o Diagrama de Classes a seguir:

<img src="DiagramaClassesSistemaALF.PNG" heigth="500" width="300">

As rotas criadas para consumir a API utilizam visualizações baseadas em funções, através do decorador *api_view*, que, por sua vez, utilizam serializadores baseados nos modelos definidos. Estes serializadores realizam a vailidação dos dados enviados nas requisições, permitindo assim salvar, alterar, listar e excluir dados do banco.

* O método *adicionarNovaProva()* apenas salva os dados da Prova (assunto), para ser possível salvar as questões dela;
* O método *adicionarNovoAluno()* verifica se o limite de 100 alunos cadastrados foi atingido, para então poder salvar o novo Aluno;
* O método *adicionarQuestaoProva()* verifica se a prova já possui questões suficientes para gerar a nota máxima de 10 pontos, com base nos pesos das questões. Caso seja possível adicionar mais questões, é verificado se a nova questão informada apresenta um peso válido, ou seja, se a soma dos pesos das questões da prova junto com o novo peso não ultrapasse o limite de 10 pontos. Dessa forma, é possível gerar provas flexíveis, como 2 questões com peso 5 ou 5 questões com peso 2, por exemplo;
* O método *adicionarAlunoProva()* salva a relação do Aluno com a Prova. Assim, se o aluno não possuir respostas para as questões da prova que está vinculado, sua nota será 0 automaticamente, o que irá afetar na sua média;
* O método *adicionarRespostaQuestao()* verifica primeiramente se a questão já foi respondida, impedindo uma nova resposta. Caso ainda não foi, a resposta será salva e analisada se está correta, sendo recalculada a nota do aluno na prova da questão e atualizada a média do aluno. Caso o aluno não estiver cadastrado na prova, este método já fará o cadastro, não havendo necessidade de realizar o método anterior;
* O método *Aluno()* é utilizado para pesquisar um aluno pelo seu id, alterar (somente) o nome do aluno e excluir o Aluno. Excluir um aluno irá excluir todas as respostas vinculadas a ele;
* O método *Resposta()* é utilizado para pesquisar uma resposta pelo seu id e excluir uma Resposta. Excluir uma resposta irá resultar na atualização da nota do aluno na prova e da sua média. Não é possível alterar uma resposta;
* O método *Questao()* é utilizado para pesquisar uma questão pelo seu id e excluir uma Questão. Excluir uma questão irá excluir as respostas salvas da questão e resultar na atualização das notas dos alunos na prova e das suas médias. Não é possível alterar uma questão;
* O método *Prova()* é utilizado para pesquisar uma prova pelo seu id, alterar (somente) o assunto da prova e excluir uma prova. Excluir uma prova irá excluir as questões, suas respostas e resultar na atualização da média dos alunos;
* O método *verAlunosAprovados()* irá retornar todos os alunos que possuírem uma média maior que 7.0;
* O método *verProvas()* irá retornar todas as provas salvas, junto com suas questões sem mostrar o gabarito;
* O método *verProvasGabarito()* irá retornar todas as provas salvas, junto com suas questões e mostrando o gabarito;
* O método *vernotas()* irá mostrar todos os alunos com suas médias e suas provas, juntamente com as notas de cada uma;
* O método *verRespostas()* irá mostrar todas as provas com suas questões, mostrando qual aluno respondeu e a resposta enviada.

### Uso da API

Para utilizar a API é necessário ter o projeto salvo no computador, ter o Python instalado (junto com as bibliotecas mostradas no arquivo *requirements.txt*) e executar o seguinte comando na pasta *sistema_alf*:

```
python manage.gy runserver
```

Com o servidor em execução, basta acessar os urls a seguir para consumir a API:

<table>
	<thead>
		<th>URL</th>
		<th>Formato JSON para envio</th>
		<th>Resultado</th>
	</thead>
	<tbody>
		<tr>
			<td>"http://127.0.0.1:8000/SistemaALF/adicionarNovaProva"</td>
			<td>{"assunto":"(Texto)"}</td>
			<td>Irá salvar uma nova Prova</td>
		</tr>
		<tr>
			<td>"http://127.0.0.1:8000/SistemaALF/adicionarNovoAluno"</td>
			<td>{"nome":"(Texto)"}</td>
			<td>Irá salvar um novo Aluno</td>
		</tr>
		<tr>
			<td>"http://127.0.0.1:8000/SistemaALF/adicionarQuestaoProva"</td>
			<td>{"descricao":"(Texto)","gabarito":"(letras A,B,C,D ou E)","peso":(Numero Inteiro),"prova":(Numero Inteiro)}</td>
			<td>Irá salvar uma nova Questão</td>
		</tr>
		<tr>
			<td>"http://127.0.0.1:8000/SistemaALF/adicionarRespostaQuestao"</td>
			<td>{"resposta":"(letras A,B,C,D ou E)","questao":(Numero Inteiro),"aluno":(Numero Inteiro)}</td>
			<td>Irá salvar uma nova Resposta</td>
		</tr>
		<tr>
			<td>"http://127.0.0.1:8000/SistemaALF/adicionarAlunoProva"</td>
			<td>{"aluno":(Numero Inteiro),"prova":(Numero Inteiro)}</td>
			<td>Irá cadastrar o aluno na prova</td>
		</tr>
		<tr>
			<td>"http://127.0.0.1:8000/SistemaALF/Prova/ + (Numero Inteiro)"</td>
			<td>*Para 'PUT'*: {"prova_id":(Numero Inteiro),"assunto":"(Texto)"}</td>
			<td>Se for 'GET', irá retornar um JSON da prova pesquisada (ou um JSON vazio).<br>
				Se for 'PUT', irá atualizar a prova pesquisada.<br>
				Se for 'DELETE', irá excluir a prova pesquisada.
			</td>
		</tr>
		<tr>
			<td>"http://127.0.0.1:8000/SistemaALF/Aluno/ + (Numero Inteiro)"</td>
			<td>*Para 'PUT'*: {"aluno_id":(Numero Inteiro),"nome":"(Texto)"}</td>
			<td>Se for 'GET', irá retornar um JSON do aluno pesquisado (ou um JSON vazio).<br>
				Se for 'PUT', irá atualizar o aluno pesquisado.<br>
				Se for 'DELETE', irá excluir o aluno pesquisado.
			</td>
		</tr>
		<tr>
			<td>"http://127.0.0.1:8000/SistemaALF/Questao/ + (Numero Inteiro)"</td>
			<td>Não há</td>
			<td>Se for 'GET', irá retornar um JSON da questão pesquisada (ou um JSON vazio).<br>
				Se for 'DELETE', irá excluir a questão pesquisada.
			</td>
		</tr>
		<tr>
			<td>"http://127.0.0.1:8000/SistemaALF/Resposta/ + (Numero Inteiro)"</td>
			<td>Não há</td>
			<td>Se for 'GET', irá retornar um JSON da resposta pesquisada (ou um JSON vazio).<br>
				Se for 'DELETE', irá excluir a resposta pesquisada.
			</td>
		</tr>
		<tr>
			<td>"http://127.0.0.1:8000/SistemaALF/verNotas"</td>
			<td>Não há</td>
			<td>Irá retornar um JSON de todos os alunos e suas médias junto com suas provas e notas (ou um JSON vazio).</td>
		</tr>
		<tr>
			<td>"http://127.0.0.1:8000/SistemaALF/verAlunosAprovados"</td>
			<td>Não há</td>
			<td>Irá retornar um JSON de todos os alunos com média maior que 7.0 (ou um JSON vazio).</td>
		</tr>
		<tr>
			<td>"http://127.0.0.1:8000/SistemaALF/verProvas"</td>
			<td>Não há</td>
			<td>Irá retornar um JSON de todas as provas com suas questões sem mostrar o gabarito delas. (ou um JSON vazio).</td>
		</tr>
		<tr>
			<td>"http://127.0.0.1:8000/SistemaALF/verProvasGabarito"</td>
			<td>Não há</td>
			<td>Irá retornar um JSON de todas as provas com suas questões mostrando seu gabarito. (ou um JSON vazio).</td>
		</tr>
		<tr>
			<td>"http://127.0.0.1:8000/SistemaALF/verRespostas"</td>
			<td>Não há</td>
			<td>Irá retornar um JSON de todas as provas com suas questões e suas respostas. (ou um JSON vazio).</td>
		</tr>
	</tbody>
</table>
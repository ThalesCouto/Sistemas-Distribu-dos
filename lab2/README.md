O dicionário fica salvo no disco em um arquivo do formato json `dict.json`, o que nos poupa de implementar os métodos de parsing para salvar e carregar o arquivo do disco, uma vez que já temos tudo implementado na biblioteca `json`do python

### Atividade 1
Objetivo: Projetar a arquitetura de software da solução. A arquitetura de software deverá conter, no mínimo, três componentes distintos:
(i) acesso e persistência de dados:
	
 - Realizado na camada que contem a classe do `Dictionary` e fazendo uso a biblioteca `json`, o que nos poupa de reimplementar todas as operações de parsing.
	
(ii) processamento das requisições:
	
- Processamento realizado pelo servidor.

(iii) interface com o usuário:
	
- Interface implementada no cliente.

Roteiro:
1. Escolha o estilo arquitetural para servir de base para o desenho da arquitetura de software.
	- Cliente e Servidor dividido em camadas

2. Descreva os componentes, com suas funcionalidades (providas e utilizadas) e modo de conexão entre eles.
	
	- server.py: 
		- Atende multiplos clientes com uso de multithreading;
		- trata entradas de todos os clientes e do stdin com uso do método `select`;
		- acessa a camada do dicionário.
	- dict_layer.py:
		- faz acesso e manutenção do dicionário;
		- salva alterações em disco.
	- client.py:
		- oferece interface ao usuário;
		- se comunica com o servidor para realizar operações do usuário.

### Atividade 2:

Objetivo: Implementar a arquitetura de software da aplicação (definida na Atividade 1) em uma arquitetura de sistema cliente/servidor de dois níveis, com um servidor e um cliente. O lado servidor abrigará o dicionário remoto, enquanto o lado cliente ficará responsável pela interface com o usuário.

Roteiro:

1. Defina quais componentes ficarão do lado do cliente.
- (iii) interface com o usuário.

2. Defina quais componentes ficarão do lado do servidor.
-  (ii) processamento das requisições.

3. Defina o conteúdo e a ordem das mensagens que serão trocadas entre cliente e servidor, e quais ações cada lado deverá tomar quando receber uma mensagem. Essa comunicação ficará responsável por fazer a "cola" entre os componentes instanciados em máquinas distintas.
- Cliente envia código da operação e argumentos;
- Servidor processa a operação e encaminha a resposta.


### Atividade 3

Objetivo: Implementar e avaliar a aplicação distribuída proposta, seguindo as definições da Atividade 2.

Roteiro:

1. Implementar o código do lado cliente e do lado servidor.
2. Modularizar e documentar o código de forma concisa e clara.
3. Experimentar a aplicação usando diferentes casos de teste.
4. Reportar as decisões tomadas em todas as atividades no README do repositório do código.
5. 
O servidor deverá ser multiplexado, ou seja, capaz de receber comandos básicos da entrada padrão (incluindo comandos para permitir finalizar o servidor quando não houver clientes ativos e remover uma entrada do dicionário) utilizando a função "select".

O servidor deverá ser concorrente, ou seja, tratar cada nova conexão de cliente como um novo fluxo de execução e atender as requisições desse cliente dentro do novo fluxo de execução. Para isso, serão criadas threads ou processos filhos.

Disponibilize seu código da aplicação em um ambiente de acesso remoto, como o GitHub ou GitLab, e envie o link para a professora, utilizando o formulário de entrega desse laboratório.

`Senha: silvana123`

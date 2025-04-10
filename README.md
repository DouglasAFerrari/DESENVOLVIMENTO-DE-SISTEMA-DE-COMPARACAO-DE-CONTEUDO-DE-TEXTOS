# DESENVOLVIMENTO-DE-SISTEMA-DE-COMPARACAO-DE-CONTEUDO-DE-TEXTOS

 Projeto Final de Curso - BACHARELADO EM ENGENHARIA DE SOFTWARE

## Instruções para Execução:

Pré-requisitos:

Tenha o Python 3.7 ou superior instalado.

Tenha o pip (gerenciador de pacotes do Python) instalado e atualizado.

Crie a Estrutura de Pastas: Crie uma pasta principal (ex: text-comparison-system) e, dentro dela, a subpasta app com as subpastas static/css, static/js e templates.

Salve os Arquivos: Salve cada bloco de código acima no arquivo correspondente dentro da estrutura de pastas criada.

## Crie um Ambiente Virtual (Recomendado):

Abra o terminal ou prompt de comando na pasta principal (text-comparison-system).

Execute: python -m venv venv

## Ative o ambiente virtual:

Windows: .\venv\Scripts\activate

macOS/Linux: source venv/bin/activate

## Instale as Dependências:   

Com o ambiente virtual ativado, execute: pip install -r requirements.txt

## Execute a Aplicação:

Ainda no terminal, na pasta principal e com o ambiente ativado, execute: python run.py

O terminal deverá indicar que o servidor Flask está rodando (geralmente em http://127.0.0.1:5000/ ou http://0.0.0.0:5000/). 

A primeira execução pode demorar um pouco mais enquanto baixa os dados do NLTK, se necessário (verifique os logs no terminal).

## Acesse no Navegador:

Abra seu navegador web e acesse o endereço indicado no terminal (normalmente http://127.0.0.1:5000/).

A interface do comparador deverá aparecer. 

Selecione dois arquivos e clique em "Comparar Arquivos".

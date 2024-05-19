# Sistema de Geração de Relatório com Gemini e MQTT

Este projeto é um sistema que gera relatórios de paradas de máquinas a partir de um banco de dados SQLite, utilizando a biblioteca Gemini para a geração do conteúdo do relatório e MQTT para a comunicação de comando e status.

## Índice

- [Descrição](#descrição)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Execução](#execução)
- [Funcionamento](#funcionamento)

## Descrição

Este sistema monitora um tópico MQTT para receber comandos de geração de relatório. Quando um comando é recebido, o sistema extrai os dados de paradas de máquinas de um banco de dados SQLite, formata os dados, gera um relatório detalhado usando o modelo generativo Gemini, e publica o relatório em formato HTML.

## Requisitos

- Python 3.x
- Bibliotecas Python:
  - `sqlite3`
  - `google-generativeai`
  - `paho-mqtt`
- Servidor MQTT configurado e em execução
- Banco de dados SQLite com os dados de paradas de máquinas

## Instalação

1. Clone este repositório:
    ```bash
    git clone https://github.com/seu-usuario/sistema-geracao-relatorio.git
    ```

2. Navegue até o diretório do projeto:
    ```bash
    cd sistema-geracao-relatorio
    ```

3. Crie um ambiente virtual (opcional, mas recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate   # No Windows: venv\Scripts\activate
    ```

4. Instale as dependências:
    ```bash
    pip install google-generativeai paho-mqtt
    ```

## Configuração

1. Configure a chave de API do Gemini:
    ```python
    genai.configure(api_key='sua_api_key')
    ```

2. Defina o caminho para o banco de dados SQLite e o arquivo HTML de saída no código:
    ```python
    caminho_banco_dados = 'caminho_do_banco_de_dados'
    caminho_arquivo_html = 'caminho_do_arquivo_html'
    ```

3. Configure o endereço e a porta do broker MQTT:
    ```python
    broker_address = "localhost"
    broker_port = 1883
    ```

## Execução

Para iniciar o sistema, execute o script principal:
```bash
python seu_script.py


## Funcionamento
Conexão ao Broker MQTT:

O cliente MQTT conecta-se ao broker especificado e se inscreve no tópico de comando.
Recebimento de Comando:

Quando uma mensagem com o comando "gerar" é recebida no tópico de comando, a função main() é chamada.
Geração do Relatório:

Conecta ao banco de dados SQLite e obtém os dados de paradas de máquinas.
Formata os dados e gera um relatório detalhado usando o modelo Gemini.
Cria um arquivo HTML com o conteúdo do relatório.
Publicação do Status:

Publica uma mensagem de status indicando que o relatório foi concluído.
Contato
Para mais informações, entre em contato com:

Nome: Fabio Machado
Email: fabio.machado@example.com
GitHub: seu-usuario


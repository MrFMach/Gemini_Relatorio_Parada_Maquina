# Relatório de Paradas de Máquinas com Gemini

Este projeto consiste em uma aplicação Python que gera relatórios concisos e detalhados sobre as paradas de máquinas industriais, utilizando a tecnologia de inteligência artificial fornecida pelo Gemini. O relatório é gerado a partir dos registros de uma tabela em um banco de dados SQLite.

## Funcionalidades

- Conexão com um banco de dados SQLite para obter dados de paradas de máquinas.
- Integração com o Node-RED para registro de paradas de máquinas através de uma interface de dashboard.
- Utilização do Gemini para gerar um relatório detalhado com base nos dados fornecidos.
- Comunicação via MQTT para disparar a geração do relatório e obter o status do processo.

## Requisitos

- Python 3.x
- Bibliotecas Python: `sqlite3`, `datetime`, `paho-mqtt`, `google-generativeai`
- Ambiente Node-RED configurado e em execução

## Instalação

1. Clone este repositório para o seu ambiente local:

    ```bash
    git clone https://github.com/seuusuario/seuprojeto.git
    ```

2. Instale as dependências Python:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure as variáveis de ambiente necessárias para os dados sensíveis, como as informações de conexão MQTT e o caminho para o banco de dados SQLite. Por exemplo:

    ```bash
    export MQTT_BROKER_ADDRESS="localhost"
    export MQTT_BROKER_PORT="1883"
    export MQTT_TOPIC_COMMAND="comando"
    export MQTT_TOPIC_STATUS="status"
    export DATABASE_PATH="/caminho/para/seu/banco/db_producao.db"
    export REPORT_PATH="/caminho/para/seu/relatorio/relatorio.html"
    ```

4. Importe o fluxo Node-RED fornecido (`node-red-flow.json`) para o seu ambiente Node-RED.

## Uso

1. Inicie a execução do Node-RED e importe o fluxo fornecido.

2. Utilize a interface de dashboard do Node-RED para registrar paradas de máquinas.

3. Execute o script Python `main.py`:

    ```bash
    python main.py
    ```

4. Aguarde o processo de geração do relatório.

5. O relatório será gerado e salvo no caminho especificado.

## Trechos de Código Importantes

### Conexão com o Banco de Dados SQLite

```python
def conectar_banco_dados(caminho):
    """Estabelece conexão com o banco de dados SQLite."""
    return sqlite3.connect(caminho)

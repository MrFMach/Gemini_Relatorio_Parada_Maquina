# Sistema de Geração de Relatório com Gemini e MQTT

Este projeto é um sistema que gera relatórios de paradas de máquinas a partir de um banco de dados SQLite, utilizando a biblioteca Gemini para a geração do conteúdo do relatório e MQTT para a comunicação de comando e status.

## Índice

- [Descrição](#descrição)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Execução](#execução)
- [Funcionamento](#funcionamento)
- [Pontos importantes do código](#pontos importantes do código)

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
```

## Funcionamento

1. Conexão ao Broker MQTT:
 - O cliente MQTT conecta-se ao broker especificado e se inscreve no tópico de comando.

2. Recebimento de Comando:
 - Quando uma mensagem com o comando "gerar" é recebida no tópico de comando, a função main() é chamada.

3. Geração do Relatório:
 - Conecta ao banco de dados SQLite e obtém os dados de paradas de máquinas.
 - Formata os dados e gera um relatório detalhado usando o modelo Gemini.
 - Cria um arquivo HTML com o conteúdo do relatório.

4. Publicação do Status:
 - Publica uma mensagem de status indicando que o relatório foi concluído.

## Pontos Importantes do Código

1. Função para obter os últimos registros de paradas de máquinas:
    ```python
    def obter_ultimas_paradas(cursor):
        """Obtém os últimos registros de paradas de máquinas."""
        cursor.execute("SELECT * FROM tab_relat_maquina ORDER BY PARADA DESC LIMIT 15")
        return cursor.fetchall()
    ```
    - **Importância:** Esta função é crucial porque é responsável por recuperar os dados mais recentes das paradas de máquinas do banco de dados. Esses dados são a base para a geração do relatório. A eficiência e a precisão desta função garantem que o relatório seja atualizado e reflita a situação atual das máquinas, permitindo análises precisas e decisões informadas.

2. Função para gerar o relatório de paradas de máquinas:
    ```python
    def gerar_relatorio_paradas(dados_paradas):
        """Gera um relatório sobre as paradas de máquinas."""
        data_hora_atual = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        prompt = f"""
        Você é um especialista em manutenção de máquinas industriais. 
        Analise os seguintes dados de paradas e gere um relatório conciso e detalhado:

        {chr(10).join(dados_paradas)}

        Seu relatório deve incluir (nessa ordem):
        - Tabela com as principais causas de parada, quantidade e porcentagem, em ordem descescente.
        - Exposição de valores atípicos, usando minutos e horas.
        - Quaisquer padrões ou tendências observadas.
        - Sugestões para reduzir o tempo de parada das máquinas.
        - Rodapé com:
            - Data e hora: {data_hora_atual}
            - Autor: Fabio Machado - Gemini
        
        Formato do relatório:
        - formato HTML, para exibição no navegador.
        - fontes Arial.
        - codificação UTF-8.
        """
    ```
    - **Importância:** Esta função é essencial porque utiliza a tecnologia Gemini para transformar dados brutos em um relatório detalhado e bem estruturado. O uso de um modelo generativo permite a criação de relatórios que não só apresentam os dados, mas também oferecem análises e sugestões práticas. Isso é fundamental para identificar causas recorrentes de paradas, tendências e possíveis melhorias, facilitando a tomada de decisões estratégicas para a manutenção e operação das máquinas.


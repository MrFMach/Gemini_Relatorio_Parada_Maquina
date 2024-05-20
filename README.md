# Relatório de Parada de Máquinas com Gemini

Este projeto é um sistema que gera relatórios de paradas de máquinas a partir de um banco de dados SQLite, utilizando a biblioteca Gemini para a geração do conteúdo do relatório.

![capa](https://github.com/MrFMach/Gemini_Relatorio_Parada_Maquina/blob/master/images/capa.png)

## Índice

- [Descrição](#descrição)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [API-Key](#api-key)
- [Configuração](#configuração)
- [Execução](#execução)
- [Funcionamento](#funcionamento)
- [Prompt](#prompt)

## Descrição

Este sistema monitora um tópico MQTT para receber comandos de geração de relatório. Quando um comando é recebido, o sistema extrai os dados de paradas de máquinas de um banco de dados SQLite, formata os dados, gera um relatório detalhado usando o modelo generativo Gemini, e publica o relatório em formato HTML.

![arquitetura](https://github.com/MrFMach/Gemini_Relatorio_Parada_Maquina/blob/master/images/arquitetura.png)

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

## API-Key

Para utilizar este projeto, você precisará de uma API Key do Google Gemini. Siga os passos abaixo para gerar a sua chave:

1. **Acesse o Google Cloud Console:** Acesse o console do Google Cloud através do link: [https://console.cloud.google.com/](https://console.cloud.google.com/)

2. **Crie um projeto (se ainda não tiver um):** Clique em "Select a project" e siga as instruções para criar um novo projeto.

3. **Habilite a API Gemini:**
   - No menu de navegação (três linhas horizontais no canto superior esquerdo), selecione "APIs & Services" -> "Library".
   - Busque por "Gemini API" e selecione o resultado da pesquisa.
   - Clique no botão "Enable" para habilitar a API no seu projeto.

4. **Crie uma credencial de API:**
   - No menu de navegação, selecione "APIs & Services" -> "Credentials".
   - Clique em "Create Credentials" e escolha "API key".
   - Uma nova API Key será gerada e exibida na tela. **Copie a chave para um local seguro!**

5. **Configure a API Key no código:**
   - Abra o arquivo `relatorio.py`.
   - Na linha `genai.configure(api_key='SUA_API_KEY')`, substitua `SUA_API_KEY` pela sua API Key gerada no passo anterior.

**Pronto!** Agora você pode executar o script Python e utilizar o Google Gemini para gerar relatórios de paradas de máquinas. 

---

**Documentação do Google Gemini:**

Para mais informações sobre a API do Google Gemini, consulte a documentação oficial: [https://developers.generativeai.google/](https://developers.generativeai.google/)

**Custos:**

O uso da API do Google Gemini pode gerar custos. Consulte a página de preços para obter informações detalhadas sobre os custos: [https://cloud.google.com/ai-platform/pricing](https://cloud.google.com/ai-platform/pricing)

**Limites de uso:**

A API Key do Google Gemini pode ter limites de uso. Consulte a documentação para obter informações sobre os limites e como aumentá-los, se necessário.

**Segurança:**

Mantenha sua API Key segura e nunca a compartilhe publicamente. Armazene-a em um local seguro e utilize variáveis de ambiente no seu código para evitar expô-la no código-fonte. 


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

## Prompt

1. Função para obter os últimos registros de paradas de máquinas, que fará parte do prompt:
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
    - **Importância:** Em resumo, esse trecho de código define o "contrato" entre o seu script Python e o Google Gemini, especificando o que o Gemini deve fazer (analisar dados e gerar relatório) e como o relatório deve ser estruturado e formatado.
      1. Definição do Prompt:
      - A variável prompt contém a instrução que será enviada para o Google Gemini.
      - O prompt define a "persona" do Gemini ("especialista em manutenção"), descreve a tarefa a ser realizada ("analisar dados de parada e gerar relatório") e fornece as informações necessárias para a análise (dados_paradas).
      2. Importância da clareza e precisão no prompt:
      - Um prompt bem definido é crucial para que o Gemini gere um relatório útil e informativo.
      - Clareza e precisão nas instruções ajudam o Gemini a entender a tarefa e a produzir resultados relevantes.
      - A formatação detalhada garante que o relatório seja apresentado de forma adequada.
      Ao dedicar tempo e atenção na elaboração do prompt, você garante que o Gemini gere relatórios de alta qualidade que atendam às suas necessidades.

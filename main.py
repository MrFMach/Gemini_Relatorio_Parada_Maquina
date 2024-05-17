import sqlite3
import google.generativeai as genai
import paho.mqtt.client as mqtt
import datetime

# --- Configuração MQTT ---
broker_address = "localhost"
broker_port = 1883
topico_comando = "comando"
topico_status = "status"

# --- Funções auxiliares MQTT ---
def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker MQTT com código de resultado: " + str(rc))
    client.subscribe(topico_comando)

def on_message(client, userdata, message):
    print(f"Mensagem recebida no tópico: {message.topic}")
    if message.topic == topico_comando:
        if message.payload.decode() == "gerar":
            main()

def publicar_status(status):
    client.publish(topico_status, status)

# --- Funções do Relatório ---

def conectar_banco_dados(caminho):
    """Estabelece conexão com o banco de dados SQLite."""
    return sqlite3.connect(caminho)


def obter_ultimas_paradas(cursor):
    """Obtém os últimos registros de paradas de máquinas."""
    cursor.execute("SELECT * FROM tab_relat_maquina ORDER BY PARADA DESC LIMIT 15")
    return cursor.fetchall()


def formatar_paradas(paradas):
    """Formata os dados de paradas de máquinas."""
    dados_formatados = []
    for parada in paradas:
        if any(valor is None for valor in parada):
            continue
        id, maquina, causa, parada_dt, resp_p, retomada_dt, resp_r, minutos = parada
        parada_dt = datetime.datetime.strptime(parada_dt, '%Y-%m-%d %H:%M:%S')
        print(
            f"Máquina: {maquina}, Causa: {causa}, Parada: {parada_dt.strftime('%Y-%m-%d %H:%M:%S')}, Tempo Parada (min): {minutos}")
        dados_formatados.append(
            f"Máquina: {maquina}, Causa: {causa}, Parada: {parada_dt.strftime('%Y-%m-%d %H:%M:%S')}, Tempo Parada (min): {minutos}")
    return dados_formatados


def gerar_relatorio_paradas(dados_paradas):
    """Gera um relatório sobre as paradas de máquinas."""
    data_hora_atual = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    prompt = f"""
    Você é um especialista em manutenção de máquinas industriais. 
    Analise os seguintes dados de paradas e gere um relatório conciso e detalhado:

    {chr(10).join(dados_paradas)}

    Seu relatório deve incluir (nessa ordem):
    - Tabela com as principais causas de parada, quantidade e porcentagem, em ordem descescente .
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

    # Cria o modelo Gemini
    model = genai.GenerativeModel('gemini-1.0-pro-latest')

    # Geração do relatório com o Gemini
    return model.generate_content(prompt)


def criar_arquivo_html_conteudo(conteudo_html, caminho_arquivo):
    """Cria um arquivo HTML com o conteúdo fornecido."""
    with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo_html:
        arquivo_html.write(conteudo_html)

# --- Função principal ---

def main():

    caminho_banco_dados = 'C:/Users/f107051/OneDrive - WICKBOLD/_Node-RED/di-L1/1887-ai/minha pasta/banco/db_producao.db'
    caminho_arquivo_html = 'C:/Users/f107051/OneDrive - WICKBOLD/_Node-RED/di-L1/1887-ai/minha pasta/relatorio/relatorio.html'

    # Conexão com o banco de dados
    conn = conectar_banco_dados(caminho_banco_dados)
    cursor = conn.cursor()

    # Obter e formatar os dados de paradas
    paradas = obter_ultimas_paradas(cursor)
    dados_paradas = formatar_paradas(paradas)

    # Geração do relatório
    relatorio = gerar_relatorio_paradas(dados_paradas)

    # Cria o arquivo HTML com o conteúdo gerado pelo Gemini
    criar_arquivo_html_conteudo(relatorio.text, caminho_arquivo_html)
    print(relatorio.text)
    print(f"Arquivo HTML '{caminho_arquivo_html}' criado com sucesso.")

    # Fechamento da conexão com o banco de dados
    conn.close()

    publicar_status("Concluído!")

# --- Configuração do Gemini ---
genai.configure(api_key='AIzaSyDJzzgKSfv_FDSgUs0Ec8czfXHhnjtJVgU')
model = genai.GenerativeModel('gemini-1.0-pro-latest')

# --- Configuração do cliente MQTT ---
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, broker_port, 60)

# Inicia o loop do cliente MQTT (bloqueante)
client.loop_forever()
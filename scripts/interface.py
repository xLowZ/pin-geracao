import os
import webbrowser
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
# from ttkbootstrap.constants import *
import json

# Obtém o diretório do script atual
script_dir = os.path.dirname(os.path.abspath(__file__)) 


# Função que mostra os resultados da análise dos painéis solares
def solar_resultados():
    # Caminho para o arquivo JSON que contém os dados dos painéis solares
    caminho_arquivo_json = os.path.join(script_dir, '..', 'config', 'param.json')
    with open(caminho_arquivo_json, 'r') as file:
        config = json.load(file)
    dados_solar = config.get('Dados_Solar', {})
    
    # Extrai os dados dos painéis solares do arquivo JSON
    painel_selecionado = dados_solar.get('painel_selecionado') 
    quantidade_paineis_necessarios = dados_solar.get('qtd_paineis_necessarios')
    potencia_final = dados_solar.get('capacidade_total')
    preco_final = dados_solar.get('preco_instalacao')

    # Cria a string com os resultados e exibe em uma messagebox
    resultado_str = f'Painel Selecionado: {painel_selecionado}\n' \
                    f'Quantidade de painéis necessários: {quantidade_paineis_necessarios}\n' \
                    f'Capacidade ao instalar: {potencia_final:.3f} kW\n' \
                    f'Preço final: R${preco_final}'

    messagebox.showinfo("Resultados da Análise", resultado_str)

# Função que mostra os resultados do consumo de energia
def consumo_resultados():
    # Caminho para o arquivo JSON que contém os dados do consumo de energia
    caminho_arquivo_json = os.path.join(script_dir, '..', 'config', 'param.json')
    with open(caminho_arquivo_json, 'r') as file:
        config = json.load(file)
    dados_consumo = config.get('Dados_Consumo_Bruto', {})
    
    # Extrai os dados do consumo de energia do arquivo JSON
    media_mensal = dados_consumo.get('media_mensal')
    consumo_diario_medio = dados_consumo.get('consumo_diario_medio')

    # Cria a string com os resultados e exibe em uma messagebox
    resultado_str = f'Média Mensal: {media_mensal} kWh\n' \
                    f'Consumo Diário Médio: {consumo_diario_medio} kWh'
    
    messagebox.showinfo("Resultados do Consumo de Energia", resultado_str)

# Função que mostra os resultados do inversor
def inversor_resultados():
    # Caminho para o arquivo JSON que contém os dados do inversor
    caminho_arquivo_json = os.path.join(script_dir, '..', 'config', 'param.json')
    with open(caminho_arquivo_json, 'r') as file:
        config = json.load(file)
    dados_inversor = config.get('Dados_Inversor', {})

    # Extrai os dados do inversor do arquivo JSON
    maxPS = dados_inversor.get('maximo_de_paineis_em_serie')
    maxPP = dados_inversor.get('maximo_de_paineis_em_paralelo')
    fator_dimens = dados_inversor.get('fator_de_dimensionamento')
    max_tensao = dados_inversor.get('maxima_tensao_de_entrada')
    max_corrente = dados_inversor.get('maxima_corrente_de_entrada')
    instalacao_status = dados_inversor.get('instalacao')

    # Cria a string com os resultados e exibe em uma messagebox
    resultado_str = f'Máximo de Painéis em Série: {maxPS}\n' \
                    f'Máximo de Painéis em Paralelo: {maxPP}\n' \
                    f'Fator de Dimensionamento: {fator_dimens}\n' \
                    f'Máxima Tensão de Entrada: {max_tensao} V\n' \
                    f'Máxima Corrente de Entrada: {max_corrente} A\n' \
                    f'Status da Instalação: {instalacao_status}\n' \
    
    messagebox.showinfo("Resultados do Inversor", resultado_str)

# Função que mostra as informações sobre o aplicativo
def mostrar_sobre():
    sobre = "Proteus Analyzer™ v1.0\n\nEste aplicativo criado pelo grupo Proteus, ajuda a simplificar a análise e cálculos relacionados à instalação de geração distribuída fotovoltaica residencial.\n\n\nGostaria de acessar o nosso repositório no GitHub?"
    resposta = messagebox.askyesno("Sobre", sobre)  # Exibe a mensagem com um botão de confirmação
    if resposta:
        webbrowser.open_new_tab("https://github.com/xLowZ/pin-geracao") 

# Função que cria a interface gráfica
def criar_interface():
    root = tb.Window(themename="darkly")
    root.title("Proteus Analyzer")
    root.geometry('500x400')

    titulo = tb.Label(text="Proteus Analyzer", font=("Bahnschrift", 28), bootstyle="warning")
    titulo.pack(pady=30)

    # Botões para acionar as diferentes análises
    button_analisar0 = tb.Button(text="Consumo", bootstyle="success, outline", command=consumo_resultados)
    button_analisar0.pack(pady=20, padx=50)

    button_analisar1 = tb.Button(text="Realizar Análise das Placas", bootstyle="success, outline", command=solar_resultados)
    button_analisar1.pack(pady=20, padx=50)

    button_analisar2 = tb.Button(text="Realizar Análise do Inversor", bootstyle="success, outline", command=inversor_resultados)
    button_analisar2.pack(pady=20, padx=50)

    # Botão "Sobre" no canto inferior direito da janela
    button_sobre = tb.Button(text="Sobre", bootstyle="info", command=mostrar_sobre)
    button_sobre.pack(side=tk.RIGHT, anchor=tk.SE, padx=10, pady=10)
    
    # Inicia o loop principal da interface gráfica
    root.mainloop()

if __name__ == "__main__":
    criar_interface() # Chama a função para criar a interface ao iniciar o programa


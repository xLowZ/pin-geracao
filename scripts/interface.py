import os
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import json

script_dir = os.path.dirname(os.path.abspath(__file__)) 

def solar_resultados():
    caminho_arquivo_json = os.path.join(script_dir, '..', 'config', 'param.json')
    with open(caminho_arquivo_json, 'r') as file:
        config = json.load(file)
    dados_solar = config.get('Dados_Solar', {})
    

    painel_selecionado = dados_solar.get('painel_selecionado') 
    quantidade_paineis_necessarios = dados_solar.get('qtd_paineis_necessarios')
    potencia_final = dados_solar.get('capacidade_total')
    preco_final = dados_solar.get('preco_instalacao')

    resultado_str = f'Painel Selecionado: {painel_selecionado}\n' \
                    f'Quantidade de painéis necessários: {quantidade_paineis_necessarios}\n' \
                    f'Capacidade ao instalar: {potencia_final:.3f} kW\n' \
                    f'Preço final: R${preco_final}'

    messagebox.showinfo("Resultados da Análise", resultado_str)

def consumo_resultados():
    caminho_arquivo_json = os.path.join(script_dir, '..', 'config', 'param.json')
    with open(caminho_arquivo_json, 'r') as file:
        config = json.load(file)
    dados_consumo = config.get('Dados_Consumo_Bruto', {})

    media_mensal = dados_consumo.get('media_mensal')
    consumo_diario_medio = dados_consumo.get('consumo_diario_medio')

    resultado_str = f'Média Mensal: {media_mensal} kWh\n' \
                    f'Consumo Diário Médio: {consumo_diario_medio} kWh'

    messagebox.showinfo("Resultados do Consumo de Energia", resultado_str)

def criar_interface():
    root = tb.Window(themename="vapor")
    root.title("Análise de Placa Solar")
    root.geometry('500x350')

    titulo = tb.Label(text="Proteus Analyzer", font=("Helvetica", 28), bootstyle="light")
    titulo.pack(pady=50)

    button_analisar0 = tb.Button(text="Consumo", bootstyle="success, outline", command=consumo_resultados)
    button_analisar0.pack(pady=20)

    button_analisar1 = tb.Button(text="Realizar Análise", bootstyle="success, outline", command=solar_resultados)
    button_analisar1.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    criar_interface()
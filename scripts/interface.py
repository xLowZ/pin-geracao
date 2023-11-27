import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import numpy as np
import analise_consumo
import analise_solar



def solar_resultados():
    media_mensal = analise_solar.get_dados_consumo()
    Potencia = analise_solar.calculo_potencia(media_mensal)
    qtd_painel1, qtd_painel2, qtd_painel3, qtd_painel4 = analise_solar.get_numero_de_paineis(Potencia)
    quantidade_paineis = np.array([qtd_painel1, qtd_painel2, qtd_painel3, qtd_painel4])
    painel_final = analise_solar.decidir_painel(qtd_painel1, qtd_painel2, qtd_painel3, qtd_painel4)
    potencia_final = quantidade_paineis[painel_final] * analise_solar.PAINEIS_SOLARES[painel_final, 0]
    preco_final = analise_solar.precos[painel_final]

    painel_selecionado = analise_solar.NOMES_PAINEIS[painel_final]
    quantidade_paineis_necessarios = quantidade_paineis[painel_final]

    resultado_str = f'Painel Selecionado: {painel_selecionado}\n' \
                    f'Quantidade de painéis necessários: {quantidade_paineis_necessarios}\n' \
                    f'Capacidade ao instalar: {potencia_final:.3f} kW\n' \
                    f'Preço final: R${preco_final}'

    messagebox.showinfo("Resultados da Análise", resultado_str)

def consumo_resultados():
    media_mensal = analise_consumo.get_media()
    consumo_diario_medio = analise_consumo.get_consumo_diario_medio(media_mensal)
    nova_media, novo_consumo = analise_consumo.arredondar_valores(media_mensal, consumo_diario_medio)

    resultado_str = f'Média Mensal: {nova_media} kWh\n' \
                    f'Consumo Diário Médio: {novo_consumo} kWh'

    messagebox.showinfo("Resultados do Consumo de Energia", resultado_str)

def criar_interface():
    root = tk.Tk()
    root.title("Análise de Placa Solar")
    root.iconbitmap('')
    root.geometry('500x350')

    button_analisar0 = tk.Button(root, text="Consumo", font=("Helvetica",15), command=consumo_resultados)
    button_analisar0.pack(pady=20)

    button_analisar1 = tk.Button(root, text="Realizar Análise", font=("Helvetica",15), command=solar_resultados)
    button_analisar1.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    criar_interface()
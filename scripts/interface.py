import os
import webbrowser
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import json


# Obtém o diretório do script atual
script_dir = os.path.dirname(os.path.abspath(__file__)) 

OUTPUT_PATH = Path(__file__).parent
#ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\igork\Desktop\UI solar\build\assets\frame0")
ASSETS_PATH = os.path.join(script_dir,'..', 'scripts', 'assets', 'frame0')


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Função que cria a interface gráfica
def criar_interface():

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
        resultado0_str = f'Painel Selecionado: {painel_selecionado}\n' \
                         f'Quantidade de painéis necessários: {quantidade_paineis_necessarios}\n' \
                         f'Capacidade ao instalar: {potencia_final:.3f} kW\n' \
                         f'Preço final: R${preco_final}'
        canvas.create_text(
            304.0,
            205.0,
            anchor="nw",
            text=resultado0_str,
            fill="#000000",
            font=("Montserrat Medium", 12 * -1)
        )
        button_2.config(state=tk.DISABLED)

    # Função que mostra os resultados do consumo de energia
    def consumo_resultados():
        global resultado1_str
        global resultado11_str
        # Caminho para o arquivo JSON que contém os dados do consumo de energia
        caminho_arquivo_json = os.path.join(script_dir, '..', 'config', 'param.json')
        with open(caminho_arquivo_json, 'r') as file:
            config = json.load(file)
        dados_consumo = config.get('Dados_Consumo_Bruto', {})
        
        # Extrai os dados do consumo de energia do arquivo JSON
        media_mensal = dados_consumo.get('media_mensal')
        consumo_diario_medio = dados_consumo.get('consumo_diario_medio')

        # Cria a string com os resultados e exibe em uma messagebox
        resultado1_str  = f'{media_mensal} kWh'
        
        resultado11_str = f'{consumo_diario_medio} kWh'


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
        resultado2_str = f'Máximo de Painéis em Série: {maxPS}\n' \
                         f'Máximo de Painéis em Paralelo: {maxPP}\n' \
                         f'Fator de Dimensionamento: {fator_dimens}\n' \
                         f'Máxima Tensão de Entrada: {max_tensao} V\n' \
                         f'Máxima Corrente de Entrada: {max_corrente} A\n' \
                         f'Status da Instalação: {instalacao_status}\n' \
        
        canvas.create_text(
            304.0,
            289.0,
            anchor="nw",
            text=resultado2_str,
            fill="#000000",
            font=("Montserrat SemiBold", 12 * -1)
        )
        button_3.config(state=tk.DISABLED)
        

    # Função que mostra as informações sobre o aplicativo
    def mostrar_sobre():
        sobre = "Proteus Analyzer™ v1.0\n\nEste aplicativo criado pelo grupo Proteus, ajuda a simplificar a análise e cálculos relacionados à instalação de geração distribuída fotovoltaica residencial.\n\n\nGostaria de acessar o nosso repositório no GitHub?"
        resposta = messagebox.askyesno("Sobre", sobre)  # Exibe a mensagem com um botão de confirmação
        if resposta:
            webbrowser.open_new_tab("https://github.com/xLowZ/pin-geracao") 


    window = Tk()

    window.geometry("700x450+620+270")
    window.configure(bg = "#FFFFFF")


    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 450,
        width = 700,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        0.0,
        0.0,
        700.0,
        59.0,
        fill="#000000",
        outline="")

    canvas.create_rectangle(
        10.0,
        64.0,
        688.0,
        176.0,
        fill="#6DC934",
        outline="")

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        349.0,
        297.0,
        image=image_image_1
    )

    canvas.create_text(
        110.0,
        9.0,
        anchor="nw",
        text="Proteus Solar Analyzer",
        fill="#FFB400",
        font=("Montserrat Black", 32 * -1)
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        183.0,
        131.0,
        image=image_image_2
    )

    canvas.create_text(
        40.0,
        104.0,
        anchor="nw",
        text="Média Mesal",
        fill="#000000",
        font=("Montserrat Bold", 12 * -1)   
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        515.0,
        131.0,
        image=image_image_3
    )

    canvas.create_text(
        372.0,
        104.0,
        anchor="nw",
        text="Consumo Diário",
        fill="#000000",
        font=("Montserrat Bold", 12 * -1)
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        550.0,
        29.0,
        image=image_image_4
    )
    
    consumo_resultados()
    
    canvas.create_text(
        37.0,
        120.0,
        anchor="nw",
        text=resultado1_str,
        fill="#000000",
        font=("Montserrat Bold", 24 * -1)
        )
        
    canvas.create_text(
        369.0,
        120.0,
        anchor="nw",
        text=resultado11_str,
        fill="#000000",
        font=("Montserrat Bold", 24 * -1)
        )

    canvas.create_text(
        26.0,
        64.0,
        anchor="nw",
        text="Consumo",
        fill="#000000",
        font=("Montserrat Medium", 24 * -1)
    )

    canvas.create_text(
        82.0,
        202.0,
        anchor="nw",
        text="Analise Solar",
        fill="#000000",
        font=("Montserrat Medium", 24 * -1)
    )

    canvas.create_rectangle(
        297.0,
        202.0,
        673.0,
        393.0,
        fill="#FFFFFF",
        outline="")
    

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=mostrar_sobre,
        relief="flat"
    )
    button_1.place(
        x=646.0,
        y=423.0,
        width=52.0,
        height=25.0
    )

    canvas.create_rectangle(
        371.0,
        280.0,
        597.0,
        281.0492192230013,
        fill="#2196F3",
        outline="")

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=solar_resultados,
        relief="flat"
    )
    button_2.place(
        x=94.0,
        y=262.0,
        width=127.0,
        height=44.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=inversor_resultados,
        relief="flat"
    )
    button_3.place(
        x=94.0,
        y=321.0,
        width=127.0,
        height=44.0
    )
    window.resizable(False, False)
    window.mainloop()
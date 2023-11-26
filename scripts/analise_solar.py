"""
    Módulo dedicado a fazer a análise quanto ao recurso solar obtido
"""

import os
import json
from math import ceil
import numpy as np

# Potência e preço por unidade dos painéis (kW e R$)
PAINEIS_SOLARES = np.array([[0.330, 579.00], 
                   [0.280, 519.00], 
                   [0.460, 749.00],
                   [0.280, 464.07]])

# Lista que será preenchida posteriormente
precos = []

NOMES_PAINEIS = ['ODA330_36_P',
                 'OSDA_ODA280_30_P',
                 'SUNOVA_SS_460_60_MDH',
                 'TRESUN_RS6C_280P']

# Obtém o caminho absoluto para o diretório do script
script_dir = os.path.dirname(os.path.abspath(__file__))



caminho_arquivo_json = os.path.join(script_dir, '..', 'config', 'param.json')


def novos_dados(media_m):
    """
        Valores deverão ser ajustados de acordo
        com o desconto do custo de disponibilidade
    
        Monofásico: o consumidor paga uma taxa mínima equivalente a 30 kWh;
        Bifásico: o custo de disponibilidade pago corresponde a 50 kWh;
        Trifásico: a taxa mínima é igual a 100 kWh.
    """
    # Alimentação trifásica
    tarifa = 30

    nova_media = media_m - tarifa
    novo_cdm = nova_media / 30

    aprx_cdm = round(novo_cdm, 2)

    return aprx_cdm 

def get_dados_consumo():
    """ Pega os dados obtidos de analise_consumo
        através de param.json

    Returns:
        float: retorna os valores calculados anteriormente
    """

    with open(caminho_arquivo_json, 'r') as file:
        config = json.load(file)

        # Acessar os dados de consumo
        dados_consumo = config.get('Dados_Consumo_Bruto', {})

        media_mensal = dados_consumo.get('media_mensal')

        # Ajuste com o custo de disponibilidade
        nova_media_mensal = novos_dados(media_mensal)

        return nova_media_mensal


def calculo_potencia(media):
    """Cálculo da potência mínima do microgerador
    (ou do Inversor)

    Pm = E / (Td x Hsp)

        Pm(Wp): Potência de pico;
        E(kWh): Consumo médio diário (cdm);
        HSP:    Média de HSP anual;
        Td:     Taxa de desempenho (0.75)
    
    Args:
        media (float): média mensal obtida
        cdm (float): consumo diário médio obtido
    """

    Td = 0.75
    Hsp = 4.88

    # media = novo consumo médio diário
    Pm = media / (Td * Hsp)

    return Pm


def get_numero_de_paineis(Ps):
    """Cálculo do número de paneis necessários
       para atingir a demanda

    Args:
        Ps (__float__): Potência do sistema
    """

    # Número de painéis necessários por modelo
    numero_de_paineis_tipo1 = 0
    numero_de_paineis_tipo2 = 0
    numero_de_paineis_tipo3 = 0
    numero_de_paineis_tipo4 = 0

    # Cálculo iterando pela lista de painéis
    for i in range(len(PAINEIS_SOLARES)):
        if   i == 0:
            numero_de_paineis_tipo1 = Ps / PAINEIS_SOLARES[i][0]
        elif i == 1:    
            numero_de_paineis_tipo2 = Ps / PAINEIS_SOLARES[i][0]
        elif i == 2:    
            numero_de_paineis_tipo3 = Ps / PAINEIS_SOLARES[i][0]
        elif i == 3:    
            numero_de_paineis_tipo4 = Ps / PAINEIS_SOLARES[i][0]


    # Arredondando nº de painéis para cima
    numero_paineis_final_1 = ceil(numero_de_paineis_tipo1)
    numero_paineis_final_2 = ceil(numero_de_paineis_tipo2)
    numero_paineis_final_3 = ceil(numero_de_paineis_tipo3)
    numero_paineis_final_4 = ceil(numero_de_paineis_tipo4)

    return numero_paineis_final_1, numero_paineis_final_2, numero_paineis_final_3, numero_paineis_final_4


def decidir_painel(p1, p2, p3, p4):
    """Função para calcular o painel mais barato,
    consequentemente o que será usado

    Args:
        p1 (_int_): _quantidade para o tipo de painel_
        p2 (_int_): _quantidade para o tipo de painel_
        p3 (_int_): _quantidade para o tipo de painel_
        p4 (_int_): _quantidade para o tipo de painel_

    Returns:
        _type_: _description_
    """
    preco_painel_1 = 0
    preco_painel_2 = 0
    preco_painel_3 = 0
    preco_painel_4 = 0

    for i in range(len(PAINEIS_SOLARES)):
        if   i == 0:
            preco_painel_1 = p1 * PAINEIS_SOLARES[i][1]
            precos.append(preco_painel_1)
        elif i == 1:    
            preco_painel_2 = p2 * PAINEIS_SOLARES[i][1]
            precos.append(preco_painel_2)
        elif i == 2:    
            preco_painel_3 = p3 * PAINEIS_SOLARES[i][1]
            precos.append(preco_painel_3)
        elif i == 3:    
            preco_painel_4 = p4 * PAINEIS_SOLARES[i][1]
            precos.append(preco_painel_4)

    preco_selecionado = min(precos)
    painel_selecionado = precos.index(preco_selecionado)
    
    return painel_selecionado

def main():
    media_mensal = get_dados_consumo()
    
    Potencia = calculo_potencia(media_mensal)

    qtd_painel1, qtd_painel2, qtd_painel3, qtd_painel4 = get_numero_de_paineis(Potencia)

    # Salvar em uma lista para facilitar visualização
    quantidade_paineis = np.array([qtd_painel1, qtd_painel2, qtd_painel3, qtd_painel4])

    painel_final = decidir_painel(qtd_painel1, qtd_painel2, qtd_painel3, qtd_painel4)

    potencia_final = quantidade_paineis[painel_final] * PAINEIS_SOLARES[painel_final, 0]

    print(f'Painel Selecionado: {NOMES_PAINEIS[painel_final]}')
    print(f'Quantidade de painéis necessários: {quantidade_paineis[painel_final]}')
    print(f'Capacidade ao instalar: {potencia_final:.3f}kW')
    print(f'Preço final: R${precos[painel_final]}')


if __name__ == "__main__":
    main()    
"""
    Módulo dedicado a fazer a análise quanto ao recurso solar obtido
"""

import os
from math import ceil
import numpy as np
import pandas as pd
import json

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# =========================== Configurações =================================
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Obtém o caminho absoluto para o diretório do script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Potência e preço por unidade dos painéis (kW e R$)
# Df = DataFrame
df = pd.read_csv(os.path.join(script_dir, '..', 'data', 'paineis.csv'))

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# ================== Variáveis Globais e Constantes =========================
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# ============== Enums pra evitar numeros mágicos  =====================

POTENCIA, PRECO_UNITARIO, MODELO = range(3)
DIAS_MES = 30

# Criar matriz com a potência, preço por unidade e modelo de cada painel
PAINEIS_SOLARES = df[['potencia[kW]', 'preco', 'modelo']].to_numpy()

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# =============================== Funções ===================================
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def get_dados_consumo():
    """ Pega os dados obtidos de analise_consumo
        através de param.json

    Returns:
        float: retorna os valores calculados anteriormente
    """
    caminho_arquivo_json = os.path.join(script_dir, '..', 'config', 'param.json')
    with open(caminho_arquivo_json, 'r') as file:
        config = json.load(file)

    # Acessar os dados de consumo
    dados_consumo = config.get('Dados_Consumo_Bruto', {})

    media_mensal = dados_consumo.get('media_mensal')

    # Ajuste com o custo de disponibilidade
    return novos_dados(media_mensal, config)

def novos_dados(media_m, config):
    """
        Valores deverão ser ajustados de acordo
        com o desconto do custo de disponibilidade
    
        Monofásico: o consumidor paga uma taxa mínima equivalente a 30 kWh;
        Bifásico: o custo de disponibilidade pago corresponde a 50 kWh;
        Trifásico: a taxa mínima é igual a 100 kWh.
    """

    # Qualquer erro de digitação na configuração resultará
    # em uma análise trifásica
    # Obter o valor de "padrao_alimentacao" do JSON
    padrao = config.get('padrao_alimentacao')

    if padrao.lower() == 'monofasico':
        tarifa = 30
    elif padrao.lower() == 'bifasico':
        tarifa = 50
    else:
        tarifa = 100        

    nova_media = media_m - tarifa
    novo_cdm = nova_media / DIAS_MES

    return round(novo_cdm, 2)

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

    caminho_arquivo_json = os.path.join(script_dir, '..', 'config', 'param.json')
    with open(caminho_arquivo_json, 'r') as file:
        config = json.load(file)

    HSP = float(config.get('HSP'))

    TAXA_DESEMPENHO = 0.75 

    # media = novo consumo médio diário
    Pm = media / (TAXA_DESEMPENHO * HSP)

    return Pm 

def get_numero_de_paineis(Ps):
    """Cálculo do número de paneis necessários
       para atingir a demanda

    Args:
        Ps (__float__): Potência do sistema
    """

    # Número de painéis necessários por modelo
    quantidade_paineis = []

    # Cálculo iterando pela lista de painéis
    for painel in range(len(PAINEIS_SOLARES)):
        numero_paineis = Ps / PAINEIS_SOLARES[painel][POTENCIA]
        quantidade_paineis.append(ceil(numero_paineis))

    return np.array(quantidade_paineis)

def decidir_painel(num_paineis):
    """Função para calcular o painel mais barato,
    consequentemente o que será usado

    Args:
        num_paineis : Array com o número de cada painel necessário

    """
    precos = []

    # Multiplica o preço unitário x qntd de painéis para calcular
    # custo total para cada caso
    for painel in range(len(PAINEIS_SOLARES)):
        preco_painel = num_paineis[painel] * PAINEIS_SOLARES[painel][PRECO_UNITARIO]
        precos.append(preco_painel)

    # Seleciona o mais barato
    preco_selecionado = min(precos)

    # Retorna o índice correspondente ao painel solar escolhido
    return precos.index(preco_selecionado), precos

def salvar_em_json(dados, caminho_arquivo):
    """ Salvando dados obtivos

    Args:
        dados (dictionary): dicionário contendo o conteúdo a ser salvo
        caminho_arquivo (None): caminho para o arquivo
    """
    # Leitura do arquivo JSON atual
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            conteudo_atual = json.load(arquivo)
    except FileNotFoundError:
        # Se o arquivo não existir, crie um dicionário vazio
        conteudo_atual = {}

    # Atualização do dicionário com os novos dados
    conteudo_atual.update(dados)

    # Escrita do dicionário atualizado de volta no arquivo JSON
    with open(caminho_arquivo, 'w') as arquivo:
        json.dump(conteudo_atual, arquivo, indent=2)

def main():
    media_mensal = get_dados_consumo()
    
    Potencia = calculo_potencia(media_mensal)

    quantidade_paineis = get_numero_de_paineis(Potencia)

    painel_final, precos = decidir_painel(quantidade_paineis)

    potencia_final = quantidade_paineis[painel_final] * PAINEIS_SOLARES[painel_final, POTENCIA]

    # Dicionário para organizar os dados
    dados_solar = {
        "painel_selecionado": PAINEIS_SOLARES[painel_final][MODELO], 
        "qtd_paineis_necessarios": int(quantidade_paineis[painel_final]),
        "capacidade_total": round(potencia_final, 2),
        "preco_instalacao": precos[painel_final],
        "demanda": round(Potencia, 4)
    }

    caminho_arquivo_json = os.path.join(script_dir, '..', 'config', 'param.json')
    # Salvar os dados em um arquivo JSON
    salvar_em_json({"Dados_Solar": dados_solar}, caminho_arquivo_json)

    print(f'Painel Selecionado: {PAINEIS_SOLARES[painel_final][MODELO]}')
    print(f'Quantidade de painéis necessários: {quantidade_paineis[painel_final]}')
    print(f'Capacidade ao instalar: {potencia_final:.3f}kW')
    print(f'Preço final: R${precos[painel_final]}')

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# =========================== Início da Execução ============================
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

if __name__ == "__main__":
    main()    
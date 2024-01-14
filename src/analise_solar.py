"""
    Módulo dedicado a fazer a análise quanto ao recurso solar obtido
"""

import os
from math import ceil
import numpy as np
import pandas as pd
import json
import logging

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# =========================== Configurações =================================
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Obtém o caminho absoluto para o diretório do script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PAINEIS = pd.read_csv(os.path.join(SCRIPT_DIR, '..', 'data', 'paineis.csv'))

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# =================== Variáveis Globais e Constantes ========================
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

POTENCIA, PRECO_UNITARIO, MODELO = range(3)

# Criar matriz com a potência, preço por unidade e modelo de cada painel
PAINEIS_SOLARES = DATA_PAINEIS[['potencia[kW]', 'preco', 'modelo']].to_numpy()

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# =============================== Funções ===================================
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def get_caminho_json():
    return os.path.join(SCRIPT_DIR, '..', 'config', 'param.json')

def log_config():
    log_path = os.path.join(SCRIPT_DIR, '..', 'logs', 'registros.log')
    logging.basicConfig(filename=log_path, level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    return logger

def get_dados_consumo(js_dir):
    """ Pega os dados obtidos de analise_consumo
        através de param.json

    Returns:
        float: retorna os valores calculados anteriormente
    """

    with open(js_dir, 'r') as file:
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

    DIAS_MES = 30

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

def calculo_potencia(media, js_dir):
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

    with open(js_dir, 'r') as file:
        config = json.load(file)

    HSP = float(config.get('HSP'))

    TAXA_DESEMPENHO = 0.75 

    # media = novo consumo médio diário
    Pm = media / (TAXA_DESEMPENHO * HSP)

    return Pm 

def get_numero_de_paineis(Ps):
    """Cálculo do número de paneis necessários p/ modelo
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
    logger = log_config()

    js_dir = get_caminho_json()

    media_mensal = get_dados_consumo(js_dir)
    
    Potencia = calculo_potencia(media_mensal, js_dir)

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

    # Salvar os dados em um arquivo JSON
    salvar_em_json({"Dados_Solar": dados_solar}, js_dir)

    logger.info(f'Painel Selecionado: {PAINEIS_SOLARES[painel_final][MODELO]}')
    logger.info(f'Quantidade de painéis necessários: {quantidade_paineis[painel_final]}')
    logger.info(f'Capacidade ao instalar: {potencia_final:.3f}kW')
    logger.info(f'Preço final: R${precos[painel_final]}')
    print(f'Painel Selecionado: {PAINEIS_SOLARES[painel_final][MODELO]}')
    print(f'Quantidade de painéis necessários: {quantidade_paineis[painel_final]}')
    print(f'Capacidade ao instalar: {potencia_final:.3f}kW')
    print(f'Preço final: R${precos[painel_final]}')

    logging.shutdown()

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# =========================== Início da Execução ============================
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

if __name__ == "__main__":
    main()    
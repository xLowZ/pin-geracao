"""
    Módulo dedicado a fazer os cálculos relacionados ao consumo de energia
    Para serem exportados para o arquivo de configuração do módulo principal
"""

import pandas as pd
import os
import json

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# =========================== Configurações =================================
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Obtém o caminho absoluto para o diretório do script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Constrói o caminho absoluto para o arquivo CSV
conta_luz_csv = os.path.join(script_dir, '..', 'data', 'conta_luz.csv')

# Pegando os dados do arquivo conta_luz.csv
data = pd.read_csv(conta_luz_csv)

# ============================= Constantes ==================================

DIAS_MES = 30
NUM_MESES_ANO = 12

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# =============================== Funções ===================================
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def get_media():
    """
        Média mensal:
        Somatório de todo o consumo
        dividido pelo número total de meses em 1 ano 
    """
    return round(((data["Consumo[kWh]"].sum()) / NUM_MESES_ANO), 2)

def get_consumo_diario_medio(media):
    """
    Cálculo do consumo diário médio 
    baseado na média de consumo obtida

    Args:
        media (flot): media mensal obtida
    """

    # Consumo Diário Médio = cdm
    return round((media / DIAS_MES), 2)

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
    
    media_mensal = get_media()
    consumo_diario_medio = get_consumo_diario_medio(media_mensal)

    # Dicionário para organizar os dados
    dados_consumo = {
        "media_mensal": media_mensal, 
        "consumo_diario_medio": consumo_diario_medio
    }

    caminho_arquivo_json = os.path.join(script_dir, '..', 'config', 'param.json')
    # Salvar os dados em um arquivo JSON
    salvar_em_json({"Dados_Consumo_Bruto": dados_consumo}, caminho_arquivo_json)

    # Exibir resultados ou realizar outras ações (opcional)
    print(f"Média Mensal: {media_mensal}kWh")
    print(f"Consumo Diário Médio: {consumo_diario_medio}kWh")

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# =========================== Início da Execução ============================
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

if __name__ == "__main__":
    main()
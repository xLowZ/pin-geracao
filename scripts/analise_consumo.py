"""
    Módulo dedicado a fazer os cálculos relacionados ao consumo de energia
    Para serem exportados para o arquivo de configuração do módulo principal
"""

import pandas as pd
import os
import json
import logging

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# =============================== Funções ===================================
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def get_dados():
    """Retorna o caminho relativo para os arquivos contendo as informações de
    conta de luz e de configurações
    """

    m_dir  = os.path.dirname(os.path.abspath(__file__))
    cl_dir = os.path.join(m_dir, '..', 'data', 'conta_luz.csv')
    js_dir = os.path.join(m_dir, '..', 'config', 'param.json')

    log_path = os.path.join(m_dir, '..', 'logs', 'registros.log')
    logging.basicConfig(filename=log_path, level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    return cl_dir, js_dir, logger

def get_media(data, logger):
    """Calcula a média mensal de consumo."""

    try:
        return data['Consumo[kWh]'].mean()   
    except KeyError:
        logger.error("Coluna 'Consumo[kWh]' não encontrada nos dados.")
        return None

def get_consumo_diario_medio(media):
    """Calcula o consumo diário médio."""

    if media is not None:
        DIAS_MES = 30
        return round(media / DIAS_MES, 2)
    
    return None

def salvar_em_json(dados, caminho_arquivo):
    """Salva os dados em um arquivo JSON."""

    try:
        with open(caminho_arquivo, 'r') as arquivo:
            conteudo_atual = json.load(arquivo)
    except FileNotFoundError:
        conteudo_atual = {}

    conteudo_atual.update(dados)

    with open(caminho_arquivo, 'w') as arquivo:
        json.dump(conteudo_atual, arquivo, indent=2)

def main():
    conta_luz_csv, caminho_arquivo_json, logger = get_dados()

    try:
        data = pd.read_csv(conta_luz_csv)

        media_mensal = get_media(data, logger)
        consumo_diario_medio = get_consumo_diario_medio(media_mensal)

        dados_consumo = {
            "media_mensal": media_mensal,
            "consumo_diario_medio": consumo_diario_medio
        }

        salvar_em_json({"Dados_Consumo_Bruto": dados_consumo}, caminho_arquivo_json)

        logger.info(f"Média Mensal: {media_mensal} kWh")
        logger.info(f"Consumo Diário Médio: {consumo_diario_medio} kWh")
        print(f"Média Mensal: {media_mensal}kWh")
        print(f"Consumo Diário Médio: {consumo_diario_medio}kWh")
    except Exception as e:
        logger.exception("Ocorreu um erro durante a execução do programa.")

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# =========================== Início do Módulo ==============================
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

if __name__ == "__main__":
    main()
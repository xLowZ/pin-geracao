'''
    Módulo com as contas necessárias para determinar as ligações
    dos painéis no inversor e verificá-las
'''

import os
import json
import pandas as pd
from math import floor

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# =========================== Configurações =================================
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Obtém o caminho absoluto para o diretório do script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Constrói o caminho absoluto para o arquivo CSV
inversor_csv = os.path.join(script_dir, '..', 'data', 'inversor.csv')

# Constrói o caminho absoluto para o arquivo CSV
paineis_csv = os.path.join(script_dir, '..', 'data', 'paineis.csv')

# Pegando os dados dos arquivos
dataInversor = pd.read_csv(inversor_csv)
dataPaineis = pd.read_csv(paineis_csv)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# =============================== Funções ===================================
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def get_painel_selecionado_e_capacidade():
    caminho_arquivo_json = os.path.join(script_dir, '..', 'config', 'param.json')
    with open(caminho_arquivo_json, 'r') as file:
        config = json.load(file)

    # Acessar os dados de consumo
    dados_painel = config.get('Dados_Solar', {})

    return dados_painel.get('painel_selecionado'), dados_painel.get('capacidade_total') * 1000     
                                                    # x1000 = Transformar de kW para W 

def paineis_serie(Vinv, Voc_painel):
    """Calcula o nº max de painéis em serie suportados

    Args:
        Vinv : Tensão máxima do inversor
        Voc_painel : Tensão de circuito aberto do painel
    """
    return floor(Vinv/Voc_painel)

def paineis_paralelo(Iinv, Isc_painel):
    """Calcula o nº max de painéis em paralelo suportados

    Args:
        Iinv (float): Capacidade de corrente do inversor
        Isc_painel (float): Corrente de curto circuito
    """
    return floor(Iinv/Isc_painel)

def get_FDI(Pnca, Pfv):
    """Fator de dimensionamento do inversor, utilizado para compensar
    perdas de potência entre o arranjo dos módulos e inversor.

    Args:
        Pnca : Potência Nominal CA do inversor
        Pfv : Potência de pico dos painéis
    """

    return round((Pnca/Pfv), 2)

def get_tensao_entrada(Vinv_min, Npaineis_serie, Vm, Vinv):
    """Calcula a tensão de entrada e verifica se está menor que a suportada.

    Args:
        Vinv_min : Tensão mínima de entrada do inversor
        Npaineis_serie : Número de painéis em série
        Vm : Tensão de máxima potência dos painéis
        Vinv : Tensão máxima de entrada do inversor
    """
    exprV = Npaineis_serie * Vm

    if Vinv_min < exprV < Vinv:
        return exprV, True
    else:
        return exprV, False
    
def get_corrente_entrada(Npaineis_paralelo, Isc_painel, Iinv):
    """Calcula a corrente de entrada e verifica se está menor que a suportada.

    Args:
        Npaineis_paralelo :  Número de painéis em paralelo
        Isc_painel : Corrente de curto circuito
        Iinv : Capacidade de corrente do inversor
    """

    expr = Npaineis_paralelo * Isc_painel

    if expr < Iinv:
        return expr, True
    else:
        return expr, False

def verif_tensao_MPPT(expr, Vminmppt, Vmaxmppt):
    """Verifica se a tensão está dentro da faixa MPPT

    Args:
        expr : produto obtido anteriormente por -> Nº de painéis em série x Tensão de máxima potência dos painéis
        Vminmppt : Tensão mínima do MPPT
        Vmaxmppt : Tensão máxima do MPPT
    """
    
    if Vminmppt < expr < Vmaxmppt:
        return True
    else:
        return False

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

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    # ============================== Variáveis ==================================
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    # Painel
    caminho_arquivo_json = os.path.join(script_dir, '..', 'config', 'param.json')
    painel_selecionado, capacidade_sistema = get_painel_selecionado_e_capacidade()

    Voc_painel = dataPaineis.loc[dataPaineis['modelo'] == painel_selecionado, 'tensao_em_aberto'].values[0]
    Isc_painel = dataPaineis.loc[dataPaineis['modelo'] == painel_selecionado, 'corrente_cc'].values[0]
    V_max_pot_painel = dataPaineis.loc[dataPaineis['modelo'] == painel_selecionado, 'tensao_max_pot'].values[0]

    # Inversor
    V_max_inversor = dataInversor['MAX_tensao_entrada[Vcc]'].iloc[0] 
    V_min_inversor = dataInversor['MIN_tensao_entrada[Vcc]'].iloc[0] 
    I_max_inversor = dataInversor['corrente_max[A]'].iloc[0]
    Pot_max_inversor = dataInversor['potencia_nominal_saida[W]'].iloc[0]

    # V_min_mppt = dataInversor['min_MPPT[Vcc]'].iloc[0]
    # V_max_mppt = dataInversor['max_MPPT[Vcc]'].iloc[0]
    
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    # ========================= Execução dos Cálculos ===========================
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    num_paineis_em_serie = paineis_serie(V_max_inversor, Voc_painel)
    num_paineis_em_paralelo = paineis_paralelo(I_max_inversor, Isc_painel)
    fdi = get_FDI(Pot_max_inversor, capacidade_sistema)
    tensao_entrada, flag_tensao = get_tensao_entrada(V_min_inversor, num_paineis_em_serie,  V_max_pot_painel, V_max_inversor)
    corrente_entrada, flag_corrente = get_corrente_entrada(num_paineis_em_paralelo, Isc_painel, I_max_inversor)

    # flag_MPPT = verif_tensao_MPPT(tensao_entrada, V_min_mppt, V_max_mppt)

    if flag_tensao and flag_corrente: #and flag_MPPT:
        print('Tudo dentro dos conformes, \033[32minstalação possível\033[0m')
        instalacao = 'Possível'
    else:
        instalacao = 'Revisar'
        if not flag_tensao and not flag_corrente:
            print('\033[33mAVISO\033[0m:\nFora da faixa de tensão e corrente do inversor')
        elif not flag_corrente:
            print('\033[33mAVISO\033[0m:\nFora da faixa de corrente do inversor')
        else:
            print('\033[33mAVISO\033[0m:\nFora da faixa de tensão do inversor')   

    # Dicionário para organizar os dados
    dados_inversor = {
        "maximo_de_paineis_em_serie": num_paineis_em_serie, 
        "maximo_de_paineis_em_paralelo": num_paineis_em_paralelo,
        "fator_de_dimensionamento": fdi,
        "maxima_tensao_de_entrada": tensao_entrada,
        "maxima_corrente_de_entrada": corrente_entrada,
        "instalacao": instalacao  
    }
    
    salvar_em_json({"Dados_Inversor": dados_inversor}, caminho_arquivo_json)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# ============================ Inicialização ================================
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    
if __name__ == "__main__":
    main()    
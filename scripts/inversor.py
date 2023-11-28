'''
    Módulo com as contas necessárias para determinar as ligações
    dos painéis no inversor e verificá-las
'''

from math import floor

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# =========================== Configurações =================================
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-



# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# =============================== Funções ===================================
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def paineis_serie(Vinv, Voc_painel):
    """Calcula o nº max de painéis em serie suportados

    Args:
        Vinv (float): Tensão máxima do inversor
        Voc_painel (float): Tensão de circuito aberto do painel
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
        Pnca (float): Potência Nominal CA do inversor
        Pfv (float): Potência de pico dos painéis
    """
    return round((Pnca/Pfv), 2)

def get_tensao_entrada(Vinv_min, Npaineis_serie, Vm, Vinv):
    """Calcula a tensão de entrada e verifica se  está menor que a suportada.

    Args:
        Vinv_min : Tensão mínima de entrada do inversor
        Npaineis_serie : Número de painéis em série
        Vm : Tensão de máxima potência dos painéis
        Vinv : Tensão máxima de entrada do inversor
    """
    expr = Npaineis_serie * Vm

    if Vinv_min < expr < Vinv:
        return expr, True
    else:
        return expr, False
    
def get_corrente_entrada(Npaineis_paralelo, Isc_painel, Iinv):
    """Verifica se a corrente de entrada está menor que a suportada.

    Args:
        Npaineis_paralelo :  Número de painéis em paralelo
        Isc_painel : Corrente de curto circuito
        Iinv : Capacidade de corrente do inversor
    """

    expr = Npaineis_paralelo * Isc_painel

    if expr < Iinv:
        return True
    else:
        return False

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

def main():
    """Função com a lógica principal
    """




# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# ============================ Inicialização ================================
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    
if __name__ == "__main__":
    main()    
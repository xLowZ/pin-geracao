import subprocess
import sys

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# ============================ CONFIGURAÇÃO =================================
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

COMMAND = ['python', 'app.py'] if sys.platform == 'win32' else ['python3', 'app.py']

subprocess.Popen(COMMAND, creationflags=subprocess.CREATE_NO_WINDOW)

################################################################

# Importando os módulos
import analise_consumo
import analise_solar
import interface
import inversor

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# ========================== Função Principal ===============================
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def executar_todos_os_modulos():
    print("Análise Consumo...\n")
    analise_consumo.main()

    print("\nAnálise Solar...\n")
    analise_solar.main()

    print('\n')
    inversor.main()

    interface.criar_interface()

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# ============================ Inicialização ================================
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

if __name__ == "__main__":
    executar_todos_os_modulos()
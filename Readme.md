# Análise de viabilidade de instalação de geração distribuída fotovoltaica residencial

## Sobre o Projeto
- O Grupo Proteus apresenta um programa projetado para simplificar a análise e cálculos relacionados à instalação de geração distribuída fotovoltaica residencial para esse caso específico. Esta ferramenta visa facilitar o processo de tomada de decisões para aqueles interessados em adotar sistemas de energia solar em suas residências.

## Como usar

### Pré-requisitos

Antes de começar, certifique-se de ter o Python instalado em seu sistema. Você pode baixar a versão mais recente [aqui](https://www.python.org/downloads/).

### Instalação das Dependências

No terminal, certifique-se de estar no mesmo diretório do arquivo `requirements.txt` e execute o seguinte comando:
```bash
pip install -r requirements.txt
```
### Inicialização
Após a conclusão da instalação das dependências, ajuste manualmente os arquivos `conta_luz.csv` e `param.json` com os dados de conta de luz e padrão de entrada respectivamente. Por último, no terminal, certifique-se de estar no mesmo diretório do aplicativo (scripts/) e inicie o programa com o seguinte comando:
```bash
python App.py
```

### Observação:
- O programa é simples e não leva em consideração, por exemplo, a área disponível para o cálculo do nº de painéis e não puxa os dados de incidência solar automaticamente, pois foi pensado para o caso em questão.

- Por enquanto, para algum aproveitamento do mesmo, aqui vão algumas instruções:
    - Link para descobrir o [HSP](http://www.cresesb.cepel.br/index.php?section=sundata)
    - Substituir a variável HSP em `analise_solar` (dentro da função "calculo_potencia") com o número encontrado.
- Verificar o padrão de alimentação para denominar a tarifa (em param.json):
    - De acordo com Resolução ANEEL RESOLUÇÃO NORMATIVA ANEEL Nº 1.000:    
    Art. 291. O custo de disponibilidade do sistema elétrico é o valor em moeda corrente equivalente a:     
    I - 30 kWh, se monofásico ou bifásico a dois condutores;       
    II - 50 kWh, se bifásico a três condutores; ou  
    III - 100 kWh, se trifásico.

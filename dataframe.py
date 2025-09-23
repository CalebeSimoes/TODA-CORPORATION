import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

 # variaveis
inicio = '2020-01-01'
fim = '2024-12-31'
data = pd.date_range(inicio, fim)
direcao_do_vento = [0 , 90, 180, 270] 
preco_venda_mwh = 195
custo_fixo_mensal = 18525
impostos = 35.65
random.seed(42)

# meu dataframe
dataframe = {
    'VEL_VENTO': [random.randint(0, 29)for _ in range(1500)],
    'DIRECAO_VENTO': [random.choice(direcao_do_vento)for _ in range(1500)],
    'TEMP_AR': [random.randint(9, 28)for _ in range(1500)],
    'DATA': [random.choice(data)for _ in range(1500)]
    }

df = pd.DataFrame(dataframe)

# gerando o calculo de energia com base na potencia maxima da captação de ar da turbina
condicoes = [
    df['VEL_VENTO'] <= 3,  
    (df['VEL_VENTO'] > 3) & (df['VEL_VENTO'] <= 15), 
    (df['VEL_VENTO'] > 15) & (df['VEL_VENTO'] <= 25), 
    df['VEL_VENTO'] > 25 
]
resultados = [
    0,
    random.randint(200, 800),
    1000,
    0
]

# alterações e criacao de mais variaveis
df['ENERGIA_GERADA'] = np.select(condicoes, resultados, default=0)
df['DATA'] = pd.to_datetime(df['DATA'])
data_2023_inicio = "2023-01-01"
data_2023_fim = "2023-12-31"
data_2023 = df[(df['DATA'] >= data_2023_inicio) & (df['DATA'] <= data_2023_fim)]
df_media_energia = df['ENERGIA_GERADA'].mean()

df_agregado = df.groupby('VEL_VENTO')['ENERGIA_GERADA'].mean().reset_index()




plt.figure(figsize=(12, 7))

# Plote a linha principal com marcadores
plt.plot(
    df_agregado['VEL_VENTO'],
    df_agregado['ENERGIA_GERADA'],
    marker='o',
    linestyle='-',
    color='#1f77b4',
    label='Média de Energia Gerada'
)


plt.axvspan(0, 3, color='gray', alpha=0.2, label='Vento Insuficiente')

# Vento ótimo para geração
plt.axvspan(3, 25, color='green', alpha=0.1, label='Faixa de Geração Ideal')

# Vento muito forte (desligamento por segurança)
plt.axvspan(25, 30, color='red', alpha=0.2, label='Vento Excessivo (Desligamento)')

# Adicione anotações para explicar os pontos críticos
plt.annotate(
    'Início da Geração\n(Cut-in Speed)',
    xy=(3.5, 20),
    xytext=(5, 250),
    arrowprops=dict(facecolor='black', shrink=0.05),
    fontsize=10,
    ha='center'
)

plt.annotate(
    'Potência Máxima\n(Rated Power)',
    xy=(15, 950),
    xytext=(18, 1050),
    arrowprops=dict(facecolor='black', shrink=0.05),
    fontsize=10,
    ha='center'
)

plt.annotate(
    'Desligamento\npor Segurança\n(Cut-out Speed)',
    xy=(25.5, 20),
    xytext=(28, 250),
    arrowprops=dict(facecolor='black', shrink=0.05),
    fontsize=10,
    ha='center'
)

# Configurações do gráfico
plt.title("Evolução da Energia Gerada com a Velocidade do Vento", fontsize=18, pad=20)
plt.xlabel("Velocidade do Vento (m/s)", fontsize=14)
plt.ylabel("Média de Energia Gerada (MWh)", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(np.arange(0, 31, 2))
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()








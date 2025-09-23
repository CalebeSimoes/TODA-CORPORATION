import pandas as pd
import random
import numpy as np



inicio = '2020-01-01'
fim = '2024-12-31'
data = pd.date_range(inicio, fim)
direcao_do_vento = [0 , 90, 180, 270] 
preco_venda_kwh = 195
custo_fixo_mensal = 18525
impostos = 35.65
random.seed(42)

dataframe = {
    'VEL_VENTO': [random.randint(0, 29)for _ in range(1500)],
    'DIRECAO_VENTO': [random.choice(direcao_do_vento)for _ in range(1500)],
    'TEMP_AR': [random.randint(9, 28)for _ in range(1500)],
    'DIA': [random.choice(data)for _ in range(1500)]
    }
df = pd.DataFrame(dataframe)

condicoes = [
    df['VEL_VENTO'] <= 3,  
    (df['VEL_VENTO'] > 3) & (df['VEL_VENTO'] <= 15), 
    (df['VEL_VENTO'] > 15) & (df['VEL_VENTO'] <= 25), 
    df['VEL_VENTO'] > 25 
]
resultados = [
    0,
    np.random.randint(200, 800, size=len(df)),
    1000,
    0
]
df['ENERGIA_GERADA'] = np.select(condicoes, resultados, default=0)



print(df)
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
import matplotlib.ticker as mticker
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

# --- 1. Variáveis e Configurações ---
inicio = '2020-01-01'
fim = '2024-12-31'
data_range_full = pd.date_range(inicio, fim) # Renomeado para evitar conflito com a coluna 'DATA' no df
direcao_do_vento = [0, 90, 180, 270]
preco_venda_mwh = 195
custo_fixo_anual = 222300
impostos_anual = 427.8
random.seed(42)

# --- 2. Criação do DataFrame ---
# Ajuste no range para que 'DATA' tenha mais datas únicas por ano

num_samples = 1500
df_data = {
    'VEL_VENTO': [random.randint(0, 29) for _ in range(num_samples)],
    'DIRECAO_VENTO': [random.choice(direcao_do_vento) for _ in range(num_samples)],
    'TEMP_AR': [random.randint(9, 28) for _ in range(num_samples)],
    'DATA': random.choices(data_range_full, k=num_samples) # Usar random.choices para mais realismo
}

df = pd.DataFrame(df_data)

# --- 3. Geração de Energia e Cálculos ---
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
df['DATA'] = pd.to_datetime(df['DATA'])
df['ANO'] = df['DATA'].dt.year
df['MES'] = df['DATA'].dt.month 


energia_gerada = df.groupby('ANO')['ENERGIA_GERADA'].sum().reset_index()
df_agregado_vento = df.groupby('VEL_VENTO')['ENERGIA_GERADA'].mean().reset_index() 

energia_gerada['FATURAMENTO_BRUTO'] = energia_gerada['ENERGIA_GERADA'] * preco_venda_mwh

energia_gerada['FATURAMENTO_LIQUIDO'] = energia_gerada['FATURAMENTO_BRUTO'] - (energia_gerada['ENERGIA_GERADA'] * (impostos_anual / 100)) - custo_fixo_anual


# --- Gráfico 1: Comparação entre Vento e Energia Gerada ---
plt.figure(figsize=(12, 7))
plt.plot(
    df_agregado_vento['VEL_VENTO'],
    df_agregado_vento['ENERGIA_GERADA'],
    marker='o',
    linestyle='-',
    color='#1f77b4',
    label='Média de Energia Gerada'
)

plt.axvspan(0, 3, color='gray', alpha=0.2, label='Vento Insuficiente')
plt.axvspan(3, 25, color='green', alpha=0.1, label='Faixa de Geração Ideal')
plt.axvspan(25, 30, color='red', alpha=0.2, label='Vento Excessivo (Desligamento)')

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

plt.title("Evolução da Energia Gerada com a Velocidade do Vento", fontsize=18, pad=20)
plt.xlabel("Velocidade do Vento (m/s)", fontsize=14)
plt.ylabel("Média de Energia Gerada (MWh)", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(np.arange(0, 31, 2))
plt.legend(loc='upper left')
plt.tight_layout()
plt.show() # Adicione plt.show() para cada gráfico para que eles apareçam individualmente.


# --- Gráfico 2: Faturamento Líquido Total por Ano ---
plt.figure(figsize=(12, 7))
plt.bar(
    energia_gerada['ANO'].astype(str), 
    energia_gerada['FATURAMENTO_LIQUIDO'],
    color='skyblue'
)

plt.title("Faturamento Líquido Total por Ano", fontsize=18, pad=20)
plt.xlabel("Ano", fontsize=14)
plt.ylabel("Faturamento Líquido (R$)", fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Formatar os rótulos do eixo Y como moeda
formatter = mticker.FormatStrFormatter('R$ %1.2f')
plt.gca().yaxis.set_major_formatter(formatter)

# Adicionar os valores em cada barra
for i, v in enumerate(energia_gerada['FATURAMENTO_LIQUIDO']):
    plt.text(i, v + (energia_gerada['FATURAMENTO_LIQUIDO'].max() * 0.02), f'R$ {v:,.0f}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# --- Gráfico 3: Faturamento por Mês para Cada Ano ---

faturamento_mensal = df.groupby(['ANO', 'MES']).agg(
    ENERGIA_GERADA=('ENERGIA_GERADA', 'sum')
).reset_index()

faturamento_mensal['FATURAMENTO_BRUTO'] = faturamento_mensal['ENERGIA_GERADA'] * preco_venda_mwh

faturamento_mensal['FATURAMENTO_LIQUIDO'] = faturamento_mensal['FATURAMENTO_BRUTO'] - (faturamento_mensal['ENERGIA_GERADA'] * (impostos_anual / 100))

custo_fixo_mensal = custo_fixo_anual / 12 # Distribuir o custo fixo anual pelos 12 meses

faturamento_mensal['FATURAMENTO_LIQUIDO'] = faturamento_mensal['FATURAMENTO_LIQUIDO'] - custo_fixo_mensal


anos_unicos = faturamento_mensal['ANO'].unique()
meses_nomes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

# Criar um gráfico para cada ano
for ano in sorted(anos_unicos):
    df_ano = faturamento_mensal[faturamento_mensal['ANO'] == ano]
    # Garantir que todos os 12 meses apareçam, mesmo que com faturamento zero
    meses_completos = pd.DataFrame({'MES': range(1, 13)})
    df_ano = pd.merge(meses_completos, df_ano, on='MES', how='left').fillna(0)

    plt.figure(figsize=(12, 7))
    plt.bar(
        df_ano['MES'].apply(lambda x: meses_nomes[int(x)-1]), # Usar nomes dos meses no eixo X
        df_ano['FATURAMENTO_LIQUIDO'],
        color='lightcoral'
    )

    plt.title(f"Faturamento Líquido Mensal - Ano {ano}", fontsize=18, pad=20)
    plt.xlabel("Mês", fontsize=14)
    plt.ylabel("Faturamento Líquido (R$)", fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    
    plt.gca().yaxis.set_major_formatter(formatter) # Reutilizando o formatter

    # Adicionar os valores em cada barra
    for i, v in enumerate(df_ano['FATURAMENTO_LIQUIDO']):
        plt.text(i, v + (df_ano['FATURAMENTO_LIQUIDO'].max() * 0.02 if df_ano['FATURAMENTO_LIQUIDO'].max() > 0 else 100000), # Ajuste para não ter erro com max=0
                 f'R$ {v:,.0f}', ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    plt.show()

print("Faturamento Líquido por Ano:")
print(energia_gerada[['FATURAMENTO_LIQUIDO', 'ANO']].style.format({'FATURAMENTO_LIQUIDO': 'R$ {:,.2f}'}))

df_media_vel_vento = df.groupby('ANO').agg(VEL_VENTO_MEDIO=('VEL_VENTO', 'mean')).reset_index()
df_media_temp_ar = df.groupby('ANO').agg(TEMP_AR_MEDIO=('TEMP_AR', 'mean')).reset_index()
df_dir_mais_comum = df.groupby('ANO').agg(DIRECAO_VENTO_MAIS_COMUM=('DIRECAO_VENTO', lambda x: x.mode()[0])).reset_index()



features_anuais = pd.merge(df_media_vel_vento, df_media_temp_ar, on='ANO')
features_anuais = pd.merge(features_anuais, df_dir_mais_comum, on='ANO')


X_train = features_anuais[['VEL_VENTO_MEDIO', 'TEMP_AR_MEDIO', 'DIRECAO_VENTO_MAIS_COMUM']]
y_train = energia_gerada['FATURAMENTO_LIQUIDO']


modelo_sgd_reg = make_pipeline(StandardScaler(), SGDRegressor(loss='squared_error', max_iter=1000, tol=1e-3))
modelo_sgd_reg.fit(X_train, y_train)


dados_para_prever_2025 = pd.DataFrame({
    'VEL_VENTO_MEDIO': [features_anuais['VEL_VENTO_MEDIO'].mean()],
    'TEMP_AR_MEDIO': [features_anuais['TEMP_AR_MEDIO'].mean()],
    'DIRECAO_VENTO_MAIS_COMUM': [features_anuais['DIRECAO_VENTO_MAIS_COMUM'].mode()[0]]
})

previsao_faturamento_2025 = modelo_sgd_reg.predict(dados_para_prever_2025)


print("Previsão de Faturamento para 2025:")
print(f"R$ {previsao_faturamento_2025[0]}")
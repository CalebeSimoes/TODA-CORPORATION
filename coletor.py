import requests
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
import os

# Conexão com o banco de dados
with sqlite3.connect('my_database.db') as connection:
    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS crypto_prices (
        id INTEGER PRIMARY KEY,
        volume REAL,
        price REAL,
        timestamp INTEGER
    );  
"""
    
    cursor.execute(create_table_query)
    connection.commit()
    print("Table 'crypto_prices' created successfully!")

    # Uso do requests para requisao da API
    parametros = {
        'vs_currency': 'brl',
        'days': '31'
    }

    response = requests.get('https://api.coingecko.com/api/v3/coins/bitcoin/market_chart', params=parametros)

    # Aloca dados da requisao no banco de dados
    if response.status_code == 200:
        data = response.json()
        prices = data.get('prices')
        volumes = data.get('total_volumes')
        
        if prices and volumes:
            # Prepare os dados para inserção
            dados_para_inserir = []
            for price_data, volume_data in zip(prices, volumes):
                timestamp = price_data[0]
                price = price_data[1]
                volume = volume_data[1]
                dados_para_inserir.append((timestamp, price, volume))
            
            # Insere todos os dados de uma vez (melhor performance)
            insert_query = "INSERT INTO crypto_prices (timestamp, price, volume) VALUES (?, ?, ?);"
            cursor.executemany(insert_query, dados_para_inserir)
            
            # Commit a transação fora do loop
            connection.commit()
            print("Dados inseridos no banco de dados com sucesso!")

    else:
        print(f"Erro na requisição de dados: {response.status_code}")

# --- Segunda parte: Análise e ML ---

# Tratamento dos dados no pandas
with sqlite3.connect('my_database.db') as connection:
    df = pd.read_sql_query("SELECT * FROM crypto_prices", connection)

df['data'] = pd.to_datetime(df['timestamp'], unit='ms')

# Remove duplicatas e define o índice
df.drop_duplicates(subset='data', keep='first', inplace=True)
df.set_index('data', inplace=True)

# Calcula a média móvel e remove os valores NaN iniciais
periodo = 31
df['media_movel'] = df['price'].rolling(window=periodo).mean()
df.dropna(inplace=True)

print(df[['media_movel']].head())

# Gráficos de visualização
sns.set_style("whitegrid")
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x=df.index, y='price', label='Preço do Bitcoin (BRL)', color='blue')

sns.lineplot(data=df, x=df.index, y='media_movel', label=f'Média Móvel ({periodo} dias)', color='red', linestyle='--')

plt.title(f'Evolução do Preço do Bitcoin e Média Móvel ({periodo} dias)', fontsize=16)
plt.xlabel('Data', fontsize=12)
plt.ylabel('Preço (R$)', fontsize=12)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

if not os.path.exists('statis'):
    os.makedirs('static')
else:
    print("Caminho ja salvo!")
    
plt.savefig("static/grafico_evolucao.png")

# ML
X = df[['media_movel']]
y = df['price']

X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.2, random_state=42)

modelo = LinearRegression()
modelo.fit(X_treino, y_treino)
modelo_previsao = 'modelo_regressao.pkl'
joblib.dump(modelo, modelo_previsao)


precisao = modelo.score(X_teste, y_teste)
print(f"A precisao do modelo é de: {precisao:.2f}")

# Obtenha o último valor da média móvel para a previsão
nova_media_movel = df['media_movel'].iloc[-1]

# Faça a previsão usando o valor mais recente
previsao = modelo.predict([[nova_media_movel]])

print(f"A previsão do preço do Bitcoin com base na média móvel de {nova_media_movel:.2f} é de: {previsao[0]:.2f}")


# No seu arquivo app.py
from flask import Flask, render_template, request, jsonify
import pandas as pd
import sqlite3
import joblib
import os

app = Flask(__name__)

# Rota principal (para carregar a página inicial)
# Aceita requisições GET do navegador
@app.route('/')
def home():
    return render_template('index.html')

# Rota de previsão (para processar a requisição do JavaScript)
# Aceita apenas requisições POST
@app.route('/prever', methods=['POST'])
def prever():
    try:
        dados_json = request.get_json()
        data_string = dados_json['data_previsao']
        
        if not os.path.exists('modelo_regressao.pkl'):
            return jsonify({'erro': 'O modelo de previsão não foi encontrado.'}), 500

        modelo = joblib.load('modelo_regressao.pkl')

        with sqlite3.connect('my_database.db') as connection:
            df = pd.read_sql_query("SELECT * FROM crypto_prices", connection)
            df['data'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.drop_duplicates(subset='data', keep='first', inplace=True)
            df.set_index('data', inplace=True)
            timestamp_base = df.index.min()
        
        data_previsao = pd.to_datetime(data_string)
        dias_desde_inicio = (data_previsao - timestamp_base).days
        
        previsao_valor = modelo.predict([[dias_desde_inicio]])[0]
        valor_formatado = f"R$ {previsao_valor:.2f}"

        return jsonify({'previsao': valor_formatado})

    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

# Importa a lógica de geração de dados do seu arquivo dataframe.py
from dataframe import df, energia_gerada, faturamento_mensal, df_agregado_vento, preco_venda_mwh, impostos_anual, custo_fixo_anual, meses_nomes

app = Flask(__name__)

# Rotas existentes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/insight")
def insight():
    return render_template("insight.html")

# Nova rota para o dashboard interativo
@app.route("/dashboard", methods=['POST'])
def dashboard():
    # Obtém o ano enviado pelo formulário no JavaScript
    ano_selecionado = int(request.form['ano_selecionado'])

    # Filtra os dados de faturamento mensal para o ano selecionado
    df_ano = faturamento_mensal[faturamento_mensal['ANO'] == ano_selecionado].copy()
    
    # Preenche meses sem dados com zero para o gráfico ficar completo
    meses_completos = pd.DataFrame({'MES': range(1, 13)})
    df_ano = pd.merge(meses_completos, df_ano, on='MES', how='left').fillna(0)

    # Gera o gráfico de faturamento mensal
    plt.figure(figsize=(12, 7))
    plt.bar(
        df_ano['MES'].apply(lambda x: meses_nomes[int(x)-1]),
        df_ano['FATURAMENTO_LIQUIDO'],
        color='lightcoral'
    )
    plt.title(f"Faturamento Líquido Mensal - Ano {ano_selecionado}", fontsize=18, pad=20)
    plt.xlabel("Mês", fontsize=14)
    plt.ylabel("Faturamento Líquido (R$)", fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    formatter = mticker.FormatStrFormatter('R$ %1.2f')
    plt.gca().yaxis.set_major_formatter(formatter)
    
    # Adiciona os valores nas barras
    for i, v in enumerate(df_ano['FATURAMENTO_LIQUIDO']):
        plt.text(i, v + (df_ano['FATURAMENTO_LIQUIDO'].max() * 0.02 if df_ano['FATURAMENTO_LIQUIDO'].max() > 0 else 100000),
                 f'R$ {v:,.0f}', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    
    # Define o caminho do arquivo e salva a imagem
    caminho_grafico_mensal = f"static/faturamento_mensal_{ano_selecionado}.png"
    plt.savefig(caminho_grafico_mensal)
    plt.close() # Fecha a figura para liberar memória

    # Obtém o faturamento líquido anual para o ano selecionado
    faturamento_anual = energia_gerada[energia_gerada['ANO'] == ano_selecionado]['FATURAMENTO_LIQUIDO'].values
    faturamento_anual_str = faturamento_anual[0] if faturamento_anual.size > 0 else 0

    # Retorna os dados como JSON para o JavaScript
    return jsonify({
        'ano': ano_selecionado,
        'faturamento_liquido': faturamento_anual_str,
        'grafico_mensal': caminho_grafico_mensal,
        'grafico_anual': "static/faturamento_anual.png" # Você pode manter o gráfico anual como estático, pois não muda
    })

if __name__ == '__main__':
    
    app.run(debug=True)
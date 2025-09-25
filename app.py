from flask import Flask, render_template, request, jsonify
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os
import matplotlib

# Importa a lógica de geração de dados do seu arquivo dataframe.py
from dataframe import df, energia_gerada, faturamento_mensal, df_agregado_vento, preco_venda_mwh, impostos_anual, custo_fixo_anual, meses_nomes

matplotlib.use('Agg')

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



@app.route("/insight", methods=['GET', 'POST'])
def insight():
    if request.method == 'POST':
        try:
            ano_selecionado = int(request.form['ano_selecionado'])
            
            # ✅ VERIFICA SE É ANO DE PREVISÃO (2025)
            if ano_selecionado == 2025:
                return gerar_dashboard_previsao(ano_selecionado)
            else:
                return gerar_dashboard_real(ano_selecionado)
                
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
            return jsonify({'error': f'Erro interno: {str(e)}'}), 500
    
    return render_template("insight.html")

def gerar_dashboard_real(ano_selecionado):
    """Gera dashboard para anos com dados reais (2020-2024)"""
    df_ano = faturamento_mensal[faturamento_mensal['ANO'] == ano_selecionado].copy()
    
    # Preenche meses sem dados com zero
    meses_completos = pd.DataFrame({'MES': range(1, 13)})
    df_ano = pd.merge(meses_completos, df_ano, on='MES', how='left').fillna(0)
    
    # ✅ AUMENTAR O TAMANHO DA FIGURA
    plt.figure(figsize=(16, 9))  # Era (12, 7) - agora maior (16:9)
    plt.clf()
    
    bars = plt.bar(
        range(len(df_ano)),
        df_ano['FATURAMENTO_LIQUIDO'],
        color='lightcoral',
        tick_label=df_ano['MES'].apply(lambda x: meses_nomes[int(x)-1])
    )
    
    plt.title(f"Faturamento Líquido Mensal - Ano {ano_selecionado}", fontsize=22, pad=25)  # ✅ FONTE MAIOR
    plt.xlabel("Mês", fontsize=16)  # ✅ FONTE MAIOR
    plt.ylabel("Faturamento Líquido (R$)", fontsize=16)  # ✅ FONTE MAIOR
    
    # ✅ AUMENTAR TAMANHO DOS RÓTULOS DOS EIXOS
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Formatação e valores nas barras
    formatter = mticker.StrMethodFormatter('R$ {x:,.0f}')
    plt.gca().yaxis.set_major_formatter(formatter)
    
    for bar, v in zip(bars, df_ano['FATURAMENTO_LIQUIDO']):
        height = bar.get_height()
        if v > 0:  # Só mostra valor se for maior que zero
            plt.text(bar.get_x() + bar.get_width()/2., height + (df_ano['FATURAMENTO_LIQUIDO'].max() * 0.02),
                    f'R$ {v:,.0f}', ha='center', va='bottom', fontsize=10)  # ✅ FONTE MAIOR
    
    plt.tight_layout()
    caminho_grafico_mensal = f"static/faturamento_mensal_{ano_selecionado}.png"
    plt.savefig(caminho_grafico_mensal, dpi=100, bbox_inches='tight')  # ✅ MAIOR QUALIDADE
    plt.close()


    # Faturamento anual real
    faturamento_anual_data = energia_gerada[energia_gerada['ANO'] == ano_selecionado]['FATURAMENTO_LIQUIDO']
    faturamento_anual_str = faturamento_anual_data.values[0] if len(faturamento_anual_data) > 0 else 0

    return jsonify({
        'ano': ano_selecionado,
        'faturamento_liquido': float(faturamento_anual_str),
        'grafico_mensal': caminho_grafico_mensal,
        'grafico_anual': "static/faturamento_anual.png",
        'tipo': 'real'  # ✅ Indica que são dados reais
    })

def gerar_dashboard_previsao(ano_selecionado):
    """Gera dashboard com previsão para 2025"""
    
    # ✅ USA A PREVISÃO QUE JÁ EXISTE NO SEU dataframe.py
    from dataframe import previsao_faturamento_2025
    
    # Cria dados mensais simulados baseados na previsão anual
    faturamento_previsto = previsao_faturamento_2025[0]
    faturamento_mensal_previsto = faturamento_previsto / 12  # Distribui igualmente pelos meses
    
    # Cria DataFrame simulado para 2025
    meses = range(1, 13)
    dados_2025 = pd.DataFrame({
        'MES': meses,
        'FATURAMENTO_LIQUIDO': [faturamento_mensal_previsto] * 12  # Mesmo valor para todos os meses
    })
    
    # Adiciona alguma variação aleatória para ficar mais realista
    import random
    random.seed(42)  # Para resultados consistentes
    
    for i in range(len(dados_2025)):
        # Variação de ±10% em cada mês
        variacao = random.uniform(0.9, 1.1)
        dados_2025.at[i, 'FATURAMENTO_LIQUIDO'] *= variacao
    
    # Gera o gráfico de previsão
    plt.figure(figsize=(12, 7))
    plt.clf()
    
    bars = plt.bar(
        range(len(dados_2025)),
        dados_2025['FATURAMENTO_LIQUIDO'],
        color='lightgreen',  # Cor diferente para previsão
        alpha=0.7,
        tick_label=dados_2025['MES'].apply(lambda x: meses_nomes[int(x)-1])
    )
    
    plt.title(f"Previsão de Faturamento Líquido Mensal - Ano {ano_selecionado} 📊", fontsize=18, pad=20)
    plt.xlabel("Mês", fontsize=14)
    plt.ylabel("Faturamento Líquido Previsto (R$)", fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    formatter = mticker.StrMethodFormatter('R$ {x:,.0f}')
    plt.gca().yaxis.set_major_formatter(formatter)
    
    for bar, v in zip(bars, dados_2025['FATURAMENTO_LIQUIDO']):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + (dados_2025['FATURAMENTO_LIQUIDO'].max() * 0.02),
                f'R$ {v:,.0f}', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    caminho_grafico_mensal = f"static/faturamento_mensal_{ano_selecionado}.png"
    plt.savefig(caminho_grafico_mensal, dpi=150, bbox_inches='tight', 
           facecolor='white', edgecolor='none')
    plt.close()

    return jsonify({
        'ano': ano_selecionado,
        'faturamento_liquido': float(faturamento_previsto),
        'grafico_mensal': caminho_grafico_mensal,
        'grafico_anual': "static/faturamento_anual.png",
        'tipo': 'previsao',  # ✅ Indica que são dados previstos
        'observacao': 'Dados baseados em previsão estatística'
    })

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
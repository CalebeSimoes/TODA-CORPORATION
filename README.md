

Análise e Previsão de Preço do Bitcoin com Python
Este projeto é uma ferramenta de análise de dados completa que coleta, processa, visualiza e prevê o preço do Bitcoin utilizando um modelo de Machine Learning e uma aplicação web simples.

🚀 Recursos Principais
Coleta de Dados: Obtém dados históricos de preço e volume do Bitcoin através da API pública da CoinGecko.

Armazenamento de Dados: Armazena os dados coletados em um banco de dados local SQLite para persistência.

Análise e Visualização: Utiliza a biblioteca Pandas para manipulação de dados e Matplotlib/Seaborn para criar um gráfico de linha interativo da evolução do preço e da média móvel.

Machine Learning: Treina um modelo de Regressão Linear para prever o preço futuro do Bitcoin com base em dados históricos.

Aplicação Web: Uma interface simples e funcional construída com Flask que exibe o gráfico de análise e permite ao usuário inserir uma data para obter uma previsão de preço.

🛠️ Tecnologias Utilizadas
Python

requests: Para fazer requisições à API.

sqlite3: Para a criação e manipulação do banco de dados local.

pandas: Para análise e manipulação dos dados.

matplotlib & seaborn: Para a criação das visualizações.

scikit-learn & joblib: Para o treinamento e salvamento do modelo de Machine Learning.

Flask: Para a criação da aplicação web.

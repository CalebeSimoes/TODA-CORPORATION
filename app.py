from flask import Flask, render_template

# Cria a sua aplicação Flask
app = Flask(__name__)

# Define a rota principal do seu site (a página inicial)
@app.route('/')
def home():
    return render_template('index.html')

# Roda o aplicativo (apenas se este script for executado diretamente)
if __name__ == '__main__':
    app.run(debug=True)
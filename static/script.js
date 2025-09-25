document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript carregado na página insight.html');
    
    const form = document.getElementById('dashboardForm');
    const resultadoContainer = document.getElementById('dashboardResults');

    if (form && resultadoContainer) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            
            const anoSelecionado = document.getElementById('ano_selecionado').value;
            console.log(' Enviando requisição para ano:', anoSelecionado);

            // Mostrar loading
            resultadoContainer.innerHTML = '<p> Carregando dados...</p>';

            fetch('/insight', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'ano_selecionado=' + encodeURIComponent(anoSelecionado)
            })
            .then(response => {
                console.log(' Resposta do servidor:', response.status);
                
                if (!response.ok) {
                    // Tenta obter mais detalhes do erro
                    return response.text().then(text => {
                        throw new Error(`Erro ${response.status}: ${text}`);
                    });
                }
                return response.json();
            })
            .then(data => {
                console.log(' Dados recebidos com sucesso:', data);
                
                // Verifica se há erro na resposta
                if (data.error) {
                    throw new Error(data.error);
                }
                
                // Formatar o faturamento
                const faturamentoFormatado = new Intl.NumberFormat('pt-BR', {
                    style: 'currency',
                    currency: 'BRL'
                }).format(data.faturamento_liquido);

                // Atualizar a interface
                resultadoContainer.innerHTML = `
    <div class="dashboard-result">
        <h3>${titulo}</h3>
        <p class="faturamento-total"> Faturamento Líquido: <strong>${faturamentoFormatado}</strong></p>
        ${observacao}
        
        <!--  PRIMEIRO GRÁFICO MAIOR (MENSAL) -->
        <div class="grafico-destaque">
            <h4> ${data.tipo === 'previsao' ? 'Previsão Mensal' : 'Faturamento Mensal'} - ${data.ano}</h4>
            <img src="${data.grafico_mensal}?t=${new Date().getTime()}" alt="Gráfico Mensal" class="grafico-grande">
        </div>
        
        <!--  SEGUNDO GRÁFICO (ANUAL) -->
        <div class="grafico-secundario">
            <h4> Comparativo Anual</h4>
            <img src="${data.grafico_anual}?t=${new Date().getTime()}" alt="Gráfico Anual">
        </div>
    </div>
`;
                
                resultadoContainer.classList.add('visible');
            })
            .catch(error => {
                console.error(' Erro completo:', error);
                resultadoContainer.innerHTML = `
                    <div class="error-message">
                        <p> Ocorreu um erro ao carregar o dashboard</p>
                        <p><strong>${error.message}</strong></p>
                        <p>Verifique o terminal do Flask para mais detalhes.</p>
                    </div>
                `;
            });
        });
    } else {
        console.error(' Formulário ou container não encontrado');
        if (!form) console.error('Formulário com ID dashboardForm não encontrado');
        if (!resultadoContainer) console.error('Container com ID dashboardResults não encontrado');
    }
});

// Header dinâmico ao scroll
window.addEventListener('scroll', function() {
    const header = document.querySelector('.main-header');
    if (window.scrollY > 100) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// Fechar menu mobile ao clicar em um link
document.querySelectorAll('.main-nav a').forEach(link => {
    link.addEventListener('click', () => {
        document.querySelector('.main-nav').classList.remove('active');
    });
});
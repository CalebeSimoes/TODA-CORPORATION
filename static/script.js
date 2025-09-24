document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.main-nav');
    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });
    }

    const dashboardButton = document.querySelector('.btn-dash');
    const formElement = document.querySelector('.form-container form');

    if (dashboardButton && formElement) {
        dashboardButton.addEventListener('click', function(event) {
            event.preventDefault();

            const formData = new FormData(formElement);
            
            console.log('Ano Selecionado:', formData.get('ano_selecionado'));

            fetch('/dashboard', { // Altere a rota aqui
                method: 'POST',
                body: formData,
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
    // Processa os dados recebidos do backend
    console.log('Dados do dashboard recebidos:', data);
    
    // Seleciona o contêiner onde o dashboard será exibido
    const dashboardContainer = document.querySelector('.dashboard-conteiner');
    
    // Verifica se o contêiner existe antes de tentar modificar o HTML
    if (dashboardContainer) {
        // Formata o faturamento líquido para um formato de moeda (R$ 24.558.972,35)
        const faturamentoFormatado = new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(data.faturamento_liquido);

        // Atualiza o conteúdo HTML do contêiner dinamicamente
        dashboardContainer.innerHTML = `
            <h3>Dashboard do Ano ${data.ano}</h3>
            <p>Faturamento Líquido: ${faturamentoFormatado}</p>
            <img src="${data.grafico_mensal}" alt="Gráfico de Faturamento Mensal">
            <img src="${data.grafico_anual}" alt="Gráfico de Faturamento Anual">
        `;
    }
})
            .catch(error => {
                console.error('Erro ao buscar o dashboard:', error);
                const dashboardContainer = document.querySelector('.dashboard-conteiner');
                if (dashboardContainer) {
                    dashboardContainer.innerHTML = `<p style="color: red;">Ocorreu um erro ao carregar o dashboard. Tente novamente mais tarde.</p>`;
                }
            });
        });
    }
});
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
    // Seleciona o contêiner do dashboard
    const dashboardContainer = document.querySelector('.dashboard-conteiner');

    if (dashboardContainer) {
        // Formata o faturamento líquido
        const faturamentoFormatado = new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(data.faturamento_liquido);

        // Atualiza o conteúdo HTML
        dashboardContainer.innerHTML = `
            <h3>Dashboard do Ano ${data.ano}</h3>
            <p>Faturamento Líquido: ${faturamentoFormatado}</p>
            <img src="${data.grafico_mensal}" alt="Gráfico de Faturamento Mensal">
            <img src="${data.grafico_anual}" alt="Gráfico de Faturamento Anual">
        `;

        // Adiciona a classe 'visible' para ativar a transição
        dashboardContainer.classList.add('visible');
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
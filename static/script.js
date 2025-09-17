document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form'); // Seleciona o primeiro formulário da página
    const predictionResult = document.querySelector('#prediction-result');
    const dateInput = document.querySelector('#prediction-date');

    // Cria a variável "hoje" com o formato correto
    const today = new Date().toISOString().split('T')[0];
    dateInput.setAttribute('min', today);

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Uso de const para consistência, e de nomes em inglês como boa prática
        const selectedDate = dateInput.value;
        const currentDate = new Date();
        const selectedDateTime = new Date(selectedDate);

        // A lógica do "return" está perfeita aqui!
        if (selectedDateTime <= currentDate) {
            predictionResult.textContent = 'Por favor, insira uma data futura.';
            return;
        }

        predictionResult.textContent = "Calculando...";

        fetch('/prever', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'data_previsao': selectedDate }),
        })
        .then(response => response.json()) // json() com "j" minúsculo
        .then(data => {
            if (data.previsao) {
                // CORRIGIDO: uso de crase (`) para a interpolação
                predictionResult.textContent = `O preço do Bitcoin em ${selectedDate} será de ${data.previsao} (valor previsto).`;
            } else if (data.erro) {
                // CORRIGIDO: uso de crase (`) para a interpolação
                predictionResult.textContent = `Erro: ${data.erro}`;
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            predictionResult.textContent = "Ocorreu um erro ao conectar com o servidor.";
        });
    });
});
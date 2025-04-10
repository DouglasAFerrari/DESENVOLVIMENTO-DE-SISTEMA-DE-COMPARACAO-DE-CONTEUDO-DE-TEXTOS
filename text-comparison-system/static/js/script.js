document.getElementById('compareBtn').addEventListener('click', async () => {
    const fileInput1 = document.getElementById('file1');
    const fileInput2 = document.getElementById('file2');
    const resultArea = document.getElementById('result-area');
    const resultText = document.getElementById('result-text');
    const loadingIndicator = document.getElementById('loading');
    const errorMessage = document.getElementById('error-message');

    // Limpa resultados anteriores e mostra indicador de carregamento
    resultText.textContent = '';
    errorMessage.style.display = 'none';
    resultArea.style.display = 'block'; // Mostra a área de resultado
    loadingIndicator.style.display = 'block';

    const file1 = fileInput1.files[0];
    const file2 = fileInput2.files[0];

    if (!file1 || !file2) {
        errorMessage.textContent = 'Por favor, selecione ambos os arquivos.';
        errorMessage.style.display = 'block';
        loadingIndicator.style.display = 'none';
        return;
    }

    const formData = new FormData();
    formData.append('file1', file1);
    formData.append('file2', file2);

    try {
        // Faz a requisição para o endpoint /compare
        const response = await fetch('/compare', {
            method: 'POST',
            body: formData,
            // Headers geralmente não são necessários para FormData com fetch,
            // o browser define Content-Type como multipart/form-data corretamente.
        });

        loadingIndicator.style.display = 'none'; // Esconde o carregamento

        if (!response.ok) {
            // Tenta pegar a mensagem de erro do JSON, se houver
            let errorMsg = `Erro ${response.status}: ${response.statusText}`;
            try {
                const errorData = await response.json();
                if (errorData && errorData.error) {
                    errorMsg = errorData.error;
                }
            } catch (e) {
                // Ignora se a resposta não for JSON válido
            }
            errorMessage.textContent = `Erro ao processar: ${errorMsg}`;
            errorMessage.style.display = 'block';
            resultText.textContent = ''; // Limpa qualquer texto de resultado anterior
        } else {
            // Processa a resposta de sucesso
            const data = await response.json();
            if (data && typeof data.correlation_index === 'number') {
                const percentage = (data.correlation_index * 100).toFixed(2);
                resultText.textContent = `Os arquivos "${data.filename1}" e "${data.filename2}" possuem um índice de correlação de ${data.correlation_index.toFixed(4)} (${percentage}%).`;
                errorMessage.style.display = 'none'; // Garante que a msg de erro está oculta
            } else {
                 errorMessage.textContent = 'Resposta inválida do servidor.';
                 errorMessage.style.display = 'block';
                 resultText.textContent = '';
            }
        }

    } catch (error) {
        // Erro de rede ou outro erro inesperado no fetch
        console.error('Erro na requisição:', error);
        loadingIndicator.style.display = 'none';
        errorMessage.textContent = 'Erro de conexão ou falha na requisição ao servidor.';
        errorMessage.style.display = 'block';
        resultText.textContent = '';
    } finally {
        // Limpa os campos de arquivo após a tentativa (opcional)
        // fileInput1.value = '';
        // fileInput2.value = '';
    }
});
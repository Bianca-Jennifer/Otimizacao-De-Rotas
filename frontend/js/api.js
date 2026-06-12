async function enviarDadosDaRota(dados) {

    const urlDoArquivo = './js/resultado.json'; 

    try {
        const resposta = await fetch(urlDoArquivo);

        if (!resposta.ok) {
            throw new Error('Não foi possível carregar o arquivo resultado.json');
        }

        return await resposta.json();
        
    } catch (erro) {
        console.error("Erro ao ler o arquivo local:", erro);
        throw erro;
    }
}
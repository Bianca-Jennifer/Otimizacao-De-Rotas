async function enviarDadosDaRota(dados) {

    const urlDaApi = 'http://localhost:5000/processar_rota'; 

    try {
        const resposta = await fetch(urlDaApi, {
            method: 'POST',
            body: dados
        });

        if (!resposta.ok) {
            throw new Error('Erro ao processar rota no servidor');
        }

        return await resposta.json();

    } catch (erro) {
        console.error("Falha na comunicação com a API:", erro);
        throw erro;
    }
}
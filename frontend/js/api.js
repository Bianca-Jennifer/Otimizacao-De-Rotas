// async function enviarDadosDaRota(dados) {

//     const urlDoArquivo = './js/resultado.json'; 

//     try {
//         const resposta = await fetch(urlDoArquivo);

//         if (!resposta.ok) {
//             throw new Error('Não foi possível carregar o arquivo resultado.json');
//         }

//         return await resposta.json();
        
//     } catch (erro) {
//         console.error("Erro ao ler o arquivo local:", erro);
//         throw erro;
//     }
// }

async function enviarDadosDaRota(dados) {

    const urlDaApi = 'http://localhost:8000/algoritmo/executar';

    try {
        const resposta = await fetch(urlDaApi, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
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
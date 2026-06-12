async function enviarDadosDaRota(dados) {
    const enderecoApi = 'http://localhost:8000/api/otimizar';

    try {
        const resposta = await fetch(enderecoApi, {
            method: 'POST',
            body: dados
        });

        if (!resposta.ok) {
            throw new Error('Erro de comunicacao com a API');
        }

        const resultado = await resposta.json();
        return resultado;
        
    } catch (erro) {
        throw erro;
    }
}


// async function enviarDadosDaRota(dados) {
//     // Simulando o tempo de processamento da API (1.5 segundos)
//     return new Promise(resolver => {
//         setTimeout(() => {
//             console.log("Mock: Simulando trajeto linear de A para B (sem retorno).");
            
//             resolver({
//                 distancia: "4.2",
//                 combustivel: "0.3",
//                 geracoes: 150,
//                 rota_nomes: [
//                     "Ponto A - Origem (Midway Mall)",
//                     "Parada 1 (Cruzamento Bernardo Vieira)",
//                     "Parada 2 (Portugal Center)",
//                     "Parada 3 (Arena das Dunas)",
//                     "Ponto B - Destino Final (UFRN)"
//                 ],
//                 // Coordenadas traçando um caminho quase reto descendo a avenida
//                 coordenadas: [
//                     [-5.8118, -35.2062], // Origem
//                     [-5.8160, -35.2075], // Parada 1
//                     [-5.8210, -35.2095], // Parada 2
//                     [-5.8267, -35.2126], // Parada 3
//                     [-5.8320, -35.2150]  // Destino
//                 ]
//             });
//         }, 1500);
//     });
// }
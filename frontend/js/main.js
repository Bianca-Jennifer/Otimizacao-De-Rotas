const telaInicial = document.getElementById('telaInicial');
const telaConfiguracao = document.getElementById('telaConfiguracao');
const botaoComecar = document.getElementById('botaoComecar');

const passoArquivo = document.getElementById('passoArquivo');
const passoDados = document.getElementById('passoDados');
const botaoProsseguir = document.getElementById('botaoProsseguir');
const arquivoCSV = document.getElementById('arquivoCSV');

const formularioUpload = document.getElementById('formularioUpload');
const indicadorCarregamento = document.getElementById('indicadorCarregamento');
const textoBotao = document.getElementById('textoBotao');
const botaoEnviar = document.getElementById('botaoEnviar');

const blocoResultados = document.getElementById('blocoResultados');
const resultadoDistancia = document.getElementById('resultadoDistancia');
const resultadoCombustivel = document.getElementById('resultadoCombustivel');
const listaCidades = document.getElementById('listaCidades');

let mapaInstancia = null;
let grupoDeRotas = null;

botaoComecar.addEventListener('click', () => {
    telaInicial.classList.add('fade-out');
    
    setTimeout(() => {
        telaInicial.classList.add('d-none');
        telaInicial.classList.remove('fade-out');
        
        telaConfiguracao.classList.remove('d-none');
        telaConfiguracao.classList.add('fade-in');
    }, 500);
});

botaoProsseguir.addEventListener('click', () => {
    if (!arquivoCSV.value) {
        alert('Por favor, selecione o arquivo CSV antes de prosseguir.');
        return;
    }

    passoArquivo.classList.add('fade-out');
    
    setTimeout(() => {
        passoArquivo.classList.add('d-none');
        passoArquivo.classList.remove('fade-out');
        
        passoDados.classList.remove('d-none');
        passoDados.classList.add('fade-in');
    }, 500);
});

//empacotamento de dados para enviar para API
formularioUpload.addEventListener('submit', async function(evento) {
    evento.preventDefault();

    botaoEnviar.disabled = true;
    indicadorCarregamento.classList.remove('d-none');
    textoBotao.textContent = 'Processando...';
    blocoResultados.classList.add('d-none');

    const dadosDoFormulario = new FormData();
    
    dadosDoFormulario.append('consumoMedio', document.getElementById('consumoMedio').value);
    dadosDoFormulario.append('capacidadeTanque', document.getElementById('capacidadeTanque').value);
    dadosDoFormulario.append('combustivelAtual', document.getElementById('combustivelAtual').value);
    dadosDoFormulario.append('formaSelecao', document.getElementById('formaSelecao').value);
    dadosDoFormulario.append('mutacao', document.getElementById('mutacao').value);
    dadosDoFormulario.append('tamanhoPopulacao', document.getElementById('tamanhoPopulacao').value);
    dadosDoFormulario.append('limiteGeracoes', document.getElementById('limiteGeracoes').value);
    dadosDoFormulario.append('arquivoCSV', arquivoCSV.files[0]);

    try {
        const respostaDaApi = await enviarDadosDaRota(dadosDoFormulario);
        
        if (respostaDaApi.distancia) {
            resultadoDistancia.textContent = respostaDaApi.distancia + ' km';
        }
        
        if (respostaDaApi.combustivel) {
            resultadoCombustivel.textContent = respostaDaApi.combustivel + ' L';
        }

        if (respostaDaApi.rota_nomes && Array.isArray(respostaDaApi.rota_nomes)) {
            listaCidades.innerHTML = respostaDaApi.rota_nomes.map((ponto, index) => 
                `<li class="list-group-item bg-transparent text-white border-secondary border-opacity-25">${index + 1}. ${ponto}</li>`
            ).join('');
        }

        blocoResultados.classList.remove('d-none');
        blocoResultados.classList.add('fade-in');

        setTimeout(() => {
            if (respostaDaApi.coordenadas && respostaDaApi.coordenadas.length > 0) {
                if (!mapaInstancia) {
                    mapaInstancia = L.map('mapaLeaflet').setView(respostaDaApi.coordenadas[0], 13);
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                        attribution: '© OpenStreetMap'
                    }).addTo(mapaInstancia);
                } else {
                    if (grupoDeRotas) {
                        mapaInstancia.removeLayer(grupoDeRotas);
                    }
                }

                mapaInstancia.invalidateSize();

                grupoDeRotas = L.featureGroup().addTo(mapaInstancia);
                
                L.polyline(respostaDaApi.coordenadas, {
                    color: '#3b82f6', 
                    weight: 5,
                    opacity: 0.8
                }).addTo(grupoDeRotas);

                respostaDaApi.coordenadas.forEach((coordenada, indice) => {
                    const nomeDoLocal = respostaDaApi.rota_nomes ? respostaDaApi.rota_nomes[indice] : (indice + 1).toString();
                    L.marker(coordenada).addTo(grupoDeRotas).bindPopup(`<b>${indice + 1}º</b> - ${nomeDoLocal}`);
                });

                mapaInstancia.fitBounds(grupoDeRotas.getBounds(), {padding: [30, 30]});
            }
        }, 300);

    } catch (erro) {
        console.log(erro);
    } finally {
        botaoEnviar.disabled = false;
        indicadorCarregamento.classList.add('d-none');
        textoBotao.innerHTML = '<i class="bi bi-send me-2"></i>Processar Rota';
    }
});
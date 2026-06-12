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
        // Recebe o pacote GeoJSON (FeatureCollection) da API
        const dadosGeoJson = await enviarDadosDaRota(dadosDoFormulario);
        
        const rotaFeature = dadosGeoJson.features.find(f => f.geometry.type === 'LineString');
        const pontosFeatures = dadosGeoJson.features.filter(f => f.geometry.type === 'Point');

        // Calcular Distância e Consumo lendo as "properties" da linha
        if (rotaFeature && rotaFeature.properties.distance_m) {
            const distanciaKm = (rotaFeature.properties.distance_m / 1000).toFixed(2);
            resultadoDistancia.textContent = distanciaKm + ' km';
            
            const consumoMedioInformado = parseFloat(document.getElementById('consumoMedio').value);
            const combustivelGasto = (distanciaKm / consumoMedioInformado).toFixed(2);
            resultadoCombustivel.textContent = combustivelGasto + ' L';
        }

        // Montar a lista de paradas dinamicamente lendo os pontos
        if (pontosFeatures.length > 0) {
            listaCidades.innerHTML = pontosFeatures.map((ponto) => 
                `<li class="list-group-item bg-transparent text-white border-secondary border-opacity-25">
                    <strong>${ponto.properties.papel.toUpperCase()}:</strong> ${ponto.properties.name}
                </li>`
            ).join('');
        }

        blocoResultados.classList.remove('d-none');
        blocoResultados.classList.add('fade-in');

        // Renderizar o Mapa
        setTimeout(() => {
            if (!mapaInstancia) {
                mapaInstancia = L.map('mapaLeaflet').setView([-5.8, -35.2], 13);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '© OpenStreetMap'
                }).addTo(mapaInstancia);
            } else {
                if (grupoDeRotas) {
                    mapaInstancia.removeLayer(grupoDeRotas);
                }
            }

            mapaInstancia.invalidateSize();

            grupoDeRotas = L.geoJSON(dadosGeoJson, {

                style: function (feature) {
                    if (feature.geometry.type === 'LineString') {
                        return { color: '#1f69f3', weight: 5, opacity: 0.8 };
                    }
                },

                onEachFeature: function (feature, layer) {
                    if (feature.geometry.type === 'Point') {
                        layer.bindPopup(`<b>${feature.properties.papel.toUpperCase()}</b><br>${feature.properties.name}`);
                    }
                }
            }).addTo(mapaInstancia);

            mapaInstancia.fitBounds(grupoDeRotas.getBounds(), {padding: [30, 30]});
            
        }, 300);

    } catch (erro) {
        console.log(erro);
    } finally {
        botaoEnviar.disabled = false;
        indicadorCarregamento.classList.add('d-none');
        textoBotao.innerHTML = '<i class="bi bi-send me-2"></i>Processar Rota';
    }
});
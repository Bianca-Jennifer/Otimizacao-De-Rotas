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

function parsearCSV(conteudo) {
    const linhas = conteudo.trim().split('\n');
    return linhas.slice(1).map(linha => {
        const [nome, latitude, longitude, tipo] = linha.split(',');
        return {
            nome: nome.trim(),
            latitude: parseFloat(latitude),
            longitude: parseFloat(longitude),
            tipo: tipo.trim()
        };
    });
}

//empacotamento de dados para enviar para API
formularioUpload.addEventListener('submit', async function(evento) {
    evento.preventDefault();

    botaoEnviar.disabled = true;
    indicadorCarregamento.classList.remove('d-none');
    textoBotao.textContent = 'Processando...';
    blocoResultados.classList.add('d-none');

    const conteudoCSV = await arquivoCSV.files[0].text();
    const lugares = parsearCSV(conteudoCSV);

    const payload = {
        lugares,
        veiculo: {
            consumoMedio: parseFloat(document.getElementById('consumoMedio').value),
            capacidadeTanque: parseFloat(document.getElementById('capacidadeTanque').value),
            combustivelAtual: parseFloat(document.getElementById('combustivelAtual').value),
        },
        limiteGeracoes: parseInt(document.getElementById('limiteGeracoes').value),
        tamanhoPopulacao: parseInt(document.getElementById('tamanhoPopulacao').value),
        formaSelecao: document.getElementById('formaSelecao').value,
        mutacao: document.getElementById('mutacao').value === 'sim',
    };

try {
        const respostaApi = await enviarDadosDaRota(payload);
        const dadosCalculados = respostaApi.resultado;

        const distanciaEmKm = (dadosCalculados.distancia_total / 1000).toFixed(2);
        resultadoDistancia.textContent = distanciaEmKm + ' km';
        
        const litrosConsumidos = dadosCalculados.litros_gastos.toFixed(2);
        resultadoCombustivel.textContent = litrosConsumidos + ' L';

        if (dadosCalculados.ordem_de_visita_nomes && dadosCalculados.ordem_de_visita_nomes.length > 0) {
            listaCidades.innerHTML = dadosCalculados.ordem_de_visita_nomes.map((local, indice) => {
                let funcaoLocal = "PARADA";
                if (indice === 0) funcaoLocal = "ORIGEM";
                else if (indice === dadosCalculados.ordem_de_visita_nomes.length - 1) funcaoLocal = "DESTINO";

                return `<li class="list-group-item bg-transparent text-white border-secondary border-opacity-25">
                    <strong>${funcaoLocal}:</strong> ${local.nome}
                </li>`;
            }).join('');
        }

        blocoResultados.classList.remove('d-none');
        blocoResultados.classList.add('fade-in');

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

            const colecaoGeoJson = {
                type: "FeatureCollection",
                features: []
            };

            if (dadosCalculados.caminho_para_desenho) {
                dadosCalculados.caminho_para_desenho.forEach(caminho => {
                    colecaoGeoJson.features.push({
                        type: "Feature",
                        properties: { 
                            nome: `${caminho.origem} para ${caminho.destino}` 
                        },
                        geometry: caminho.geometry
                    });
                });
            }

            if (dadosCalculados.ordem_de_visita_nomes) {
                dadosCalculados.ordem_de_visita_nomes.forEach((local, indice) => {
                    let funcaoDoPonto = "Parada";
                    if (indice === 0) funcaoDoPonto = "Origem";
                    else if (indice === dadosCalculados.ordem_de_visita_nomes.length - 1) funcaoDoPonto = "Destino";

                    colecaoGeoJson.features.push({
                        type: "Feature",
                        properties: { 
                            name: local.nome, 
                            papel: funcaoDoPonto 
                        },
                        geometry: {
                            type: "Point",
                            coordinates: [local.longitude, local.latitude]
                        }
                    });
                });
            }

            grupoDeRotas = L.geoJSON(colecaoGeoJson, {
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
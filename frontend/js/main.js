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
        await enviarDadosDaRota(dadosDoFormulario);
    } catch (erro) {
        console.log(erro);
    } finally {
        botaoEnviar.disabled = false;
        indicadorCarregamento.classList.add('d-none');
        textoBotao.innerHTML = '<i class="bi bi-send me-2"></i>Processar Rota';
    }
});
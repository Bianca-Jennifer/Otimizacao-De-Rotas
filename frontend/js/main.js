
const telaInicial = document.getElementById('telaInicial');
const telaConfiguracao = document.getElementById('telaConfiguracao');
const botaoComecar = document.getElementById('botaoComecar');

botaoComecar.addEventListener('click', () => {
    telaInicial.classList.add('fade-out');
    
    setTimeout(() => {
        telaInicial.classList.add('d-none');
        telaInicial.classList.remove('fade-out');
        
        telaConfiguracao.classList.remove('d-none');
        telaConfiguracao.classList.add('fade-in');
    }, 500);
});

const formularioUpload = document.getElementById('formularioUpload');
const indicadorCarregamento = document.getElementById('indicadorCarregamento');
const textoBotao = document.getElementById('textoBotao');
const botaoEnviar = document.getElementById('botaoEnviar');

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
    dadosDoFormulario.append('arquivoCSV', document.getElementById('arquivoCSV').files[0]);

    try {
        await enviarDadosDaRota(dadosDoFormulario);
    } catch (erro) {
        console.log(erro);
    } finally {
        botaoEnviar.disabled = false;
        indicadorCarregamento.classList.add('d-none');
        textoBotao.textContent = 'Enviar Dados e Arquivo';
    }
});
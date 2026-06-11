const formularioUpload = document.getElementById('formularioUpload');
const indicadorCarregamento = document.getElementById('indicadorCarregamento');
const textoBotao = document.getElementById('textoBotao');
const botaoEnviar = document.getElementById('botaoEnviar');

formularioUpload.addEventListener('submit', async function(evento) {
    evento.preventDefault();

    botaoEnviar.disabled = true;
    indicadorCarregamento.classList.remove('d-none');
    textoBotao.textContent = 'Processando...';

    const consumoMedio = document.getElementById('consumoMedio').value;
    const capacidadeTanque = document.getElementById('capacidadeTanque').value;
    const combustivelAtual = document.getElementById('combustivelAtual').value;
    const formaSelecao = document.getElementById('formaSelecao').value;
    const mutacao = document.getElementById('mutacao').value;
    const tamanhoPopulacao = document.getElementById('tamanhoPopulacao').value;
    const limiteGeracoes = document.getElementById('limiteGeracoes').value;
    const arquivoCSV = document.getElementById('arquivoCSV').files[0];

    const dadosDoFormulario = new FormData();

    dadosDoFormulario.append('consumoMedio', consumoMedio);
    dadosDoFormulario.append('capacidadeTanque', capacidadeTanque);
    dadosDoFormulario.append('combustivelAtual', combustivelAtual);
    dadosDoFormulario.append('formaSelecao', formaSelecao);
    dadosDoFormulario.append('mutacao', mutacao);
    dadosDoFormulario.append('tamanhoPopulacao', tamanhoPopulacao);
    dadosDoFormulario.append('limiteGeracoes', limiteGeracoes);
    dadosDoFormulario.append('arquivoCSV', arquivoCSV);

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
# Otimizacao-De-Rotas

## Guia de Instalação e Execução

### 1º Passo: Baixar Arquivos na Sua Máquina
A primeira etapa antes de qualquer coisa é baixar o repositório na sua máquina. Para isso:
- Clique em "Code"; e
- Clique em "Download ZIP".

### 2º Passo: Configure as Variáveis de Ambiente da Aplicação
As variáveis de ambiente são essenciais para a execução conforme seu desejo, portanto configurar elas é extremamente essencial. Para isso, crie uma cópia do arquivo .env.example com o nome .env.

Esteja certo que preencheu todas as variáveis presentes no arquivo antes de passar para as próximas etapas.

### 3º Passo: Instalar o Docker
Por ser uma ferramenta em constante evolução, o processo de instalação pode ser alterado com certa frequência. Para informações detalhadas acerca da instalação, recomendamos o tutorial disponibilizado no [site da ferramenta](https://docs.docker.com/desktop/).

### 4º Passo: Baixar Mapa da Região
Para download dos mapas, acesse o site oficial do [geofabrik](https://download.geofabrik.de/), navegue até a região que deseja hospedar e então baixe o arquivo de tipo .osm.pbf.

Para baixar a região Nordeste do Brasil, [clique aqui](https://download.geofabrik.de/south-america/brazil/nordeste-latest.osm.pbf).

### 5º Passo: Extração das Informações do Mapa
Após o download do mapa é necessário realizar as etapas de extração e particionamento das informações. Para isso, execute o comando comando responsável pelo script de extração:
```
docker compose run --rm processor
```
**ATENÇÃO!**
É extremamente necessário que você tenha disponível pelo menos 10x mais memória ram que o tamanho do arquivo baixado na etapa 2. Valores menores que esse podem ocasionar falta de recurso nessa etapa, o que retornará erro. A utilização de memória de SWAP se mostrou ineficiente em testes realizados internamente por frequentemente estarem associados ao efeito de [thrashing](https://medium.com/@nishakuvadiya10/thrashing-in-operating-systems-when-too-much-swapping-slows-everything-down-f7ee8be956bf).

### 6º Passo: Inicialização do Container
Após todas as etapas de pré-processamento de todas as informações do mapa, execute o comando de inicialização do container:
```
docker compose up -d
```
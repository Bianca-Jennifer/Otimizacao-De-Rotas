
# Otimização de Rotas

  

**Disciplina:** Introdução à Inteligência Artificial

**Semestre:** 2026.1

**Professor:** ANDRE LUIS FONSECA FAUSTINO

**Turma:** T04

  

## Integrantes do Grupo

* ALEX EDUARDO NASCIMENTO DA APRESENTAÇÃO (20250066518)

* BIANCA JENNIFER FRANKLIN DA SILVA (20240020604)

* KELPY DE AZEVEDO LIMA (20250030032)

* VINICIUS KAUÃ GOMES DA SILVA (20250035404)

  

## Descrição do Projeto

Uma aplicação web desenvolvida para calcular e otimizar rotas de veículos utilizando Algoritmos Genéticos. O sistema não apenas encontra o caminho mais curto entre múltiplos pontos obrigatórios, mas também leva em consideração a autonomia do veículo e a localização estratégica de postos de combustível ao longo do trajeto.

  

## Guia de Instalação e Execução

### 1º Passo: Baixar Arquivos na Sua Máquina

A primeira etapa antes de qualquer coisa é baixar o repositório na sua máquina. Para isso acesse o [repositório](https://github.com/Bianca-Jennifer/Otimizacao-De-Rotas) e então siga os seguintes passos:

- Clique em "Code"; e
- Clique em "Download ZIP".
- Extraia o arquivo baixado no seu computador.

### 2º Passo: Configure as Variáveis de Ambiente da Aplicação

As variáveis de ambiente são essenciais para a execução conforme seu desejo, portanto configurar elas é extremamente essencial. Para isso, renomeie o arquivo .env.example para .env e preencha as variáveis conforme necessidade.
Antes de passar para as próximas etapas, esteja certo que todas as variáveis presentes no arquivo estejam preenchidas.

### 3º Passo: Instalar o Docker

Por ser uma ferramenta em constante evolução, o processo de instalação pode ser alterado. Para informações detalhadas acerca da instalação, recomendamos o tutorial disponibilizado no [site da ferramenta](https://docs.docker.com/desktop/).

### 4º Passo: Baixar Mapa da Região

Para download dos mapas, acesse o site oficial do [geofabrik](https://download.geofabrik.de/), navegue até a região que deseja hospedar e então baixe o arquivo de tipo .osm.pbf.

Para baixar a região Nordeste do Brasil, [clique aqui](https://download.geofabrik.de/south-america/brazil/nordeste-latest.osm.pbf).

  

### 5º Passo: Extração das Informações do Mapa

Após o download do mapa é necessário realizar as etapas de extração e particionamento das informações. Para isso, execute o comando responsável pelo script de extração:
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
## Estrutura dos Arquivos

*  `algoritmo_genetico/`: Contém a lógica central, aplicando os conceitos de evolução, cruzamento, mutação e seleção para otimizar os trajetos.

*  `classes/`: Modelos de dados e entidades do domínio. Armazena as estruturas fundamentais como `Veiculo`, `Lugar`, `Individuo` e `DefinicaoProblema`, padronizando como as informações transitam pelo código.

*  `cliente_distancias/`: Responsável por calcular as rotas reais, gerar as matrizes de distâncias e processar as coordenadas geográficas dos locais.

*  `services/`: Concentra a orquestração e as regras do sistema, sendo responsável por preparar os dados do front-end, gerenciar a lógica complexa de autonomia e postos de combustível, gerar as rotas iniciais e formatar as coordenadas geográficas finais para o mapa.

## Resultados e Demonstração

![Print de Roteamento Bem Sucedido](https://github.com/Bianca-Jennifer/Otimizacao-De-Rotas/blob/develop/screenshot/roteamento_bem_sucedido.png)

## Referências

- [GeeksforGeeks – Genetic Algorithms](https://www.geeksforgeeks.org/dsa/genetic-algorithms/)
- [DataCamp – Introduction to Genetic Algorithms in Python](https://www.datacamp.com/tutorial/genetic-algorithm-python)
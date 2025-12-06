# 📊 Monitor de Mercado B3 - Case Neoway

Este projeto é uma solução de *Análise de Dados* desenvolvida para monitorar o mercado de ações brasileiro (B3), cruzando dados financeiros (cotações) com dados cadastrais.

O objetivo foi simular o ambiente de dados da **Neoway**, transformando dados brutos em inteligência de mercado para tomada de decisão estratégica.

![Capa do Projeto](files/images/print_1.png)

## 💼 O Desafio de Negócio

O mercado financeiro gera milhões de registros diários, mas dados isolados não geram insights. O desafio consistiu em:

* **Ingerir e tratar** grandes volumes de dados históricos e cadastro de empresas.
* **Enriquecer** a análise com indicadores macroeconômicos (Dólar, Selic, IPCA).
* **Desenvolver um Dashboard** que atendesse a três perfis: o Analista Técnico (Micro), o Gestor de Portfólio (Macro) e o Auditor (Compliance).

## 🛠️ Arquitetura da Solução

O projeto segue a arquitetura **Raw, Clean e Enrich**, garantindo governança e performance.

* **ETL:** Python utilizando a biblioteca Pandas para limpeza, tipagem e criação das tabelas fato e dimensão.
* **Modelagem:** Star Schema (Fato Cotações, Fato Dados Externos, Dimensão Calendário, Dimensão Empresas).
* **Analytics:** Microsoft Power BI com medidas DAX avançadas para estatística financeira.

---
## 📈 Tour pelo Dashboard

### 1. Monitor de Ativos
   Focada na análise de ativos isoladamente, esta tela permite dissecar o comportamento de um ativo específico.
   
* **Destaque Técnico:** Implementação de gráfico Candlestick combinado com médias móveis.
* **Gestão de Risco:** Gráfico de Drawdown Histórico, calculado via DAX para medir a queda percentual em relação ao topo histórico, essencial para avaliar o risco do ativo.
* **KPIs Dinâmicos:** Variação do período, Preço de Fechamento e Volume Financeiro.

   ![Monitor de Ativos](files/images/print_2_tela1.png)

### 2. Radar de Mercado
   Focada na visão "Macro", responde onde estão as oportunidades e os riscos do mercado.
* **Matriz Risco x Retorno:** Cruza a Volatilidade no eixo X com a Rentabilidade no eixo Y. Permite identificar ativos de alto retorno e baixo risco.
* **Mapa de Liquidez:** Visão hierárquica de setores, onde o tamanho representa o volume financeiro e a cor indica a performance.
* **Ranking:** Top 20 ativos por rentabilidade no período.

   ![Radar de Mercado](files/images/print_3_tela2.png)

### 3. Relatórios Detalhados
   Focada na granularidade e na qualidade dos dados cadastrais.

* **Enriquecimento:** Traz dados exclusivos como saúde tributária, nível de atividade e porte da empresa, que permite uma análise mais profunda da empresa.
* **Tratamento de Dados:** Máscara de CNPJ aplicada via DAX para formatar visualmente os dados sem impactar a performance do banco de dados.

   ![Relatórios Detalhados](files/images/print_4_tela3.png)

---

## 🧠 Destaques Técnicos

### 🐍 Python (ETL)
* Script de carga incremental e tratamento de nulos.
* Geração de chaves para otimizar relacionamentos no Power BI.

### 📊 DAX

Abaixo estão as principais medidas desenvolvidas para solucionar regras de negócio:

### _Dimensoes

#### CNPJ_Formatado
* **Objetivo:** Melhorar a legibilidade do campo cnpj aplicando uma máscara padrão de CNPJ (XX.XXX.XXX/XXXX-XX) sem alterar o dado original utilizado nos relacionamentos.
* **Lógica:** A medida verifica o comprimento do campo: se tiver 14 dígitos, aplica a formatação direta; se tiver 13 dígitos (perda de zero à esquerda), realiza a sanitização do dado adicionando o zero antes de formatar. Caso contrário, retorna o valor original.

---
#### Titulo_Completo
* **Objetivo:** Aumentar a clareza do gráfico candlestick fornecendo contexto ao título do visual utilizando nome do ativo e período selecionado.
* **Lógica:** Constrói uma string dinâmica baseada no contexto de filtro atual. Utiliza SELECTEDVALUE para identificar o ativo ou aplicar um valor default "Mercado" caso nenhum ativo esteja selecionado e concatena com as datas de início e fim do período, aplicando formatação de texto.

---
#### Ultima_Atualizacao
* **Objetivo:** Garantir a transparência e a confiabilidade do dashboard, informando ao usuário exatamente até quando os dados apresentados são válidos.
* **Lógica:** Busca a data mais recente presente na tabela fCotacoes. O resultado é convertido do formato de data para texto e concatenado com uma string.

---
#### Drawdown%
* **Objetivo:** Mensurar o risco de investimento calculando a queda percentual do preço atual em relação ao seu topo histórico. Responde à pergunta: "Quanto o investidor estaria perdendo hoje se tivesse comprado no pior momento?"
* **Lógica:** Implementa um padrão de cálculo de Máximo Acumulado. A função CALCULATE com FILTER e ALLSELECTED percorre o histórico do período selecionado para encontrar o valor máximo atingido até a data atual. A medida utiliza o [Preço Fechamento (Contínuo)] para garantir que dias sem negociação ou finais de semana não gerem falsos drawdowns de -100%.

---
#### Preco_Fechamento_Cont
* **Objetivo:** Garantir a continuidade visual em gráficos de linha e a integridade matemática de cálculos, evitando que o preço "caia a zero" ou fique vazio em dias sem pregão, sejam finais de semana ou feriados.
* **Lógica:** A medida ignora o filtro de data atual para varrer o passado e identificar a data mais recente que possui registro de valor de negociação, projetando este último valor para o dia atual.

---
#### Preco_Fechamento_Periodo
* **Objetivo:** Exibir o valor do ativo no final do período selecionado, em vez de realizar uma soma sem sentido de todos os preços do ano. Trata o preço como um snapshot de fim de período.
* **Lógica:** Identifica a data mais recente disponível e utiliza CALCULATE para restringir a agregação apenas aos registros desse dia específico, ignorando os dias anteriores do período.

---
#### Rentabilidade%
* **Objetivo:** Calcular a performance absoluta do ativo dentro do período selecionado.
* **Lógica:** Calcula a variação percentual (Valor_Final - Valor_Inicial) / Valor_Inicial. A medida utiliza MIN(fCotacoes[dt_pregao]) e MAX em vez das datas da dimensão calendário para garantir que os preços de referência sejam buscados no primeiro e último dia útil com pregão, evitando erros de divisão por zero ou valores nulos caso o período inicie em um feriado ou final de semana.

---
#### Variacao%
* **Objetivo:** Calcular a amplitude total de movimento do preço dentro do período selecionado, iniciando no momento de abertura do mercado e terminando no seu encerramento. Diferente da rentabilidade tradicional que compara Fechamento vs. Fechamento, essa métrica mostra o ganho/perda real de uma posição iniciada na Abertura do primeiro dia e encerrada no Fechamento do último dia.
* **Lógica:** Calcula o valor da coluna vl_abertura no início do período e compara com a coluna vl_fechamento no final do período, retornando a variação percentual entre esses dois pontos distintos.

---
#### Volatilidade
* **Objetivo:** Mensura o grau de risco e instabilidade do ativo.
* **Lógica:** A medida obtém o Desvio Padrão dos preços de fechamento e o normaliza dividindo pela média do período. Isso transforma a volatilidade em um indicador percentual.

---
## 🚀 Como Executar

1. Clone o repositório.
2.  Execute os scripts na pasta `/scripts` seguindo a ordem lógica:
    * `Extract`: Para ingestão dos dados brutos.
    * `Transform`: Para limpeza e padronização.
    * `Load`: Para modelagem e geração dos arquivos `.csv` finais.
3. Abra o arquivo teste_bi.pbix no Power BI Desktop e clique em **Atualizar** para carregar os dados do dashboard.

---
*Desenvolvido por **Douglas** como parte do case técnico para a NeoWay.*

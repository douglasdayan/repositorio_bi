📊 Monitor de Mercado B3 & Analytics - Neoway Challenge

Este projeto é uma solução End-to-End de Análise de Dados desenvolvida para monitorar o mercado de ações brasileiro (B3), cruzando dados financeiros (cotações) com dados cadastrais enriquecidos (compliance e perfil tributário).

O objetivo foi simular o ambiente de dados da Neoway, transformando dados brutos em inteligência de mercado para tomada de decisão estratégica.

![alt text](print_1.png)

💼 O Desafio de Negócio
O mercado financeiro gera milhões de registros diários, mas dados isolados não geram insights. O desafio consistiu em:

Ingerir e Tratar grandes volumes de dados de cotações históricas e cadastro de empresas.

Enriquecer a análise com indicadores macroeconômicos (Dólar, Selic, IPCA).

Desenvolver um Dashboard que atendesse a três perfis: o Analista Técnico (Micro), o Gestor de Portfólio (Macro) e o Auditor (Compliance).

🛠️ Arquitetura da Solução
O projeto segue a arquitetura de Medallion (Bronze, Silver, Gold), garantindo governança e performance.

ETL & Engenharia: Python usando biblioteca Pandas para limpeza, tipagem e criação das tabelas Fato/Dimensão.

Modelagem: Star Schema (Fato Cotações, Fato Dados Externos, Dimensão Calendário, Dimensão Empresas).

Analytics: Microsoft Power BI com medidas DAX avançadas para estatística financeira.

📈 Tour pelo Dashboard
1. Monitor de Ativos (Análise Técnica)
Focada na análise "Micro", esta tela permite dissecar o comportamento de um ativo específico.

Destaque Técnico: Implementação de gráfico Candlestick nativo combinado com médias móveis.

Gestão de Risco: Gráfico de Drawdown Histórico (área vermelha), calculado via DAX complexo para medir a queda percentual em relação ao topo histórico, essencial para avaliar o risco do ativo.

KPIs Dinâmicos: Variação do período, Preço de Fechamento e Volume Financeiro.

![alt text](print_2_tela1.png)

2. Radar de Mercado (Estratégia & Portfólio)
Focada na visão "Macro", responde onde estão as oportunidades e os riscos do mercado.

Matriz Risco x Retorno (Scatter Plot): O coração da estratégia. Cruza a Volatilidade (Desvio Padrão anualizado) no eixo X com a Rentabilidade no eixo Y. Permite identificar ativos na "Fronteira Eficiente" (Alto Retorno, Baixo Risco) e ativos tóxicos.

Mapa de Liquidez (Treemap): Visão hierárquica de setores, onde o tamanho representa o volume financeiro e a cor indica a performance (Verde/Vermelho).

Ranking: Top N ativos por rentabilidade no período.

![alt text](print_3_tela2.png)

3. Relatórios Detalhados (Auditoria & Compliance)
Focada na granularidade e na qualidade do dado cadastral, alinhada ao core business da Neoway.

Enriquecimento: Traz dados exclusivos como Saúde Tributária, Nível de Atividade e Porte da empresa.

Tratamento de Dados: Máscara de CNPJ aplicada via DAX para formatar visualmente os dados sem impactar a performance do banco de dados.

![alt text](print_4_tela3.png)

🧠 Destaques Técnicos (The "Secret Sauce")
🐍 Python (ETL)
Script de carga incremental e tratamento de nulos.

Geração de chaves sub-rogadas para otimizar relacionamentos no Power BI.

Filtro inteligente de janelas temporais (YTD) na camada Gold para performance.

📊 DAX Avançado
Cálculo de Volatilidade: Uso de funções estatísticas (STDEV.P) normalizadas pela média para criar o coeficiente de variação.

Correção de Feriados (Last Non-Blank): O gráfico de Drawdown utiliza lógica de inteligência temporal para projetar o último preço de fechamento sobre finais de semana, evitando o efeito de "queda para zero" nos gráficos de linha.

Contexto de Transição: Medidas iteradoras (AVERAGEX) para calcular corretamente a rentabilidade média de setores, evitando distorções de agregação simples.

🚀 Como Executar
Clone o repositório.

Execute os scripts na pasta /scripts para gerar os arquivos .csv processados.

Abra o arquivo .pbix no Power BI Desktop.

Desenvolvido por Douglas como parte do case técnico para a NeoWay.
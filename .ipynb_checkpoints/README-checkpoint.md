# Case iFood - Analista de dados

Considere uma empresa bem estabelecida que atua no setor de varejo de alimentos. Atualmente, eles têm cerca de vários milhares de clientes registrados e atendem quase um milhão de consumidores por ano. Eles vendem produtos de 5 grandes categorias: vinhos, carnes, frutas exóticas, peixes especialmente preparados e produtos doces. Estes podem ser divididos ainda mais em produtos de *gold* e regulares. Os clientes podem encomendar e adquirir produtos por meio de 3 canais de vendas: lojas físicas, catálogos e site da empresa. Globalmente, a empresa teve receitas sólidas e uma linha de fundo saudável nos últimos 3 anos, mas as perspectivas de crescimento dos lucros para os próximos 3 anos não são promissoras... Por esse motivo, várias iniciativas estratégicas estão sendo consideradas para inverter essa situação. Um deles é melhorar o desempenho das atividades de marketing, com foco especial em campanhas de marketing.

![pairplot](reports/images/clusters.png)

Projeto estudo de caso baseado no processo seletivo para Analista de Dados do iFood disponível [neste repositório](https://github.com/ifood/ifood-data-business-analyst-test).

Descrição completa do case [aqui](related/ifood_crm_data_analyst_case.md).

## Objetivos

Através do estudo de caso do processo seletivo do Ifood foi  possível:
- Construir uma análise exploratória robusta.
- Segmentar os clientes da base de dados fornecida.
- Construir um modelo de classificação para prever se um cliente irá comprar o produto oferecido na campanha.
- Apresentar uma estrutura de projeto de Ciência de Dados, com a utilização de notebooks, scripts, relatórios e repositório no GitHub.
- Apresentar boas práticas de programação em Python, como a utilização de funções e arquivos de script para facilitar o reaproveitamento de código.
- Mostrar boas práticas de uso do SciKit-Learn, como a utilização de pipelines e otimização de hiperparâmetros.

## Detalhes do dataset utilizado e resumo dos resultados

Um dicionário de dados está disponível: [aqui](related/dicionario_dados.md).
Descrição completa [aqui](related/ifood_crm_data_analyst_case.md).

Com um pipeline com pré-processamento, PCA e K-Means, a base foi segmentada em 3 clusters:

![clusters](reports/images/pca.png)

Análise por cluster:

- Cluster 0:

  - Menor renda  
  - menor gasto 
  - maior probabilidade de ter filhos (jovens)
  - baixa propensão a aceitar campanhas
  - único cluster com porcentagem significativa de pessoas com escolaridade básica
  - grupo com pessoas mais jovens
  

- Cluster 1: 
 
  - Renda alta 
  - gasto alto 
  - menor probabilidade de ter filhos
  - mais propenso a aceitar campanhas
  - cluster sem pessoas com escolaridade básica
  - mais pessoas com idade intermediária/elevada
  

- Cluster 2: 
  - Renda intermediária
  - gasto intermediário
  - maior probabilidade de ter filhos (adolescentes)
  - pode aceitar campanhas
  - mais pessoas com idade intermediária/elevada

![clusters](reports/images/clusters_features.png)
Posteriormente, seis modelos de classificação com diferentes abordagens e complexidades foram treinados para comparar desempenho e entender o comportamento em relação a classificação dos clientes.  A ideia é avaliar desde modelos base simples até modelos avançados com capacidade de ajuste fino e desempenho elevado em bases reais.

1. LogisticRegression – Modelo Linear Interpretable 

    * É simples, eficiente e rápido, especialmente em datasets com número razoável de features.

    * Interpretação direta dos coeficientes ajuda na explicação do modelo.

    * Funciona bem quando a relação entre as variáveis é aproximadamente linear.

    * Ponto de atenção: Pode não capturar relações não lineares nos dados.

2. SGDClassifier – Gradiente Estocástico (versátil e eficiente)

    * Muito eficiente em grandes volumes de dados.

    * Permite usar diferentes funções de perda (log loss, hinge, etc.).

    * Suporta regularizações L1, L2 e ElasticNet.

    * Ponto de atenção: Sensível a hiperparâmetros como taxa de aprendizado e número de iterações.

3. KNeighborsClassifier – Baseado em Instância

    * Simples e intuitivo.

    * Não faz suposições sobre a distribuição dos dados.

    * Bom para conjuntos pequenos e quando a distância entre exemplos tem significado.

    * Ponto de atenção:
  
        * Custo computacional alto em datasets grandes.

        * Muito sensível à escolha de K e ao escalonamento das variáveis.

4. SVC – Máquinas de Vetores de Suporte (SVM)

    * Robusto para margens pequenas entre classes.

    * Funciona bem com kernel trick para problemas não lineares.

    * Bom desempenho em problemas complexos de classificação com feature space de alta dimensão.

    * Ponto de atenção:

        * Custo computacional alto em datasets grandes.

        * Pode exigir ajuste fino de C e kernel.

5. XGBoost – Boosting Avançado e Otimizado

    * Altamente eficaz em problemas reais com dados tabulares.

    * Suporta customização, regularização e lida bem com valores ausentes.

    * Excelente desempenho em dados desbalanceados, especialmente com o parâmetro scale_pos_weight.

    * Ponto de atenção: Mais complexo para ajustar e interpretar.

6. LightGBM – Boosting com Foco em Performance

    * Semelhante ao XGBoost, mas mais rápido, usando histogramas e crescimento leaf-wise.

    * Muito rápido e eficiente em datasets grandes.

    * Lida bem com features categóricas e dados desbalanceados.

    * Suporte nativo a scale_pos_weight e early stopping.

    * Ponto de atenção:

        * Pode overfitar se não for cuidadosamente ajustado.

        * Requer tratamento especial em datasets muito pequenos.
     
Um DummyClassifier foi utilizado como baseline. 

## Conclusão

- Modelos lineares como Regressão Logística tiveram ótimo desempenho, mesmo em comparação com modelos de árvore.
- O uso de `average_precision` como métrica principal foi essencial para melhor interpretação do desempenho em uma base desbalanceada.

![comparing_models](reports/images/comparing_models.png)

Com base nessa comparação, o modelo de Regressão Logística foi escolhido para passar por uma otimização de hiperparâmetros. 

## Organização do projeto

```

├── data                <- Arquivos de dados para o projeto.
├── models              <- Modelos gerados para o projeto.
|
├── notebooks           <- Cadernos Jupyter. 
│
|   └──src              <- Código-fonte para uso neste projeto.
|      │
|      ├── __init__.py  <- Torna um módulo Python
|      ├── helpers.py   <- Funções auxiliares do projeto
|      ├── config.py    <- Configurações básicas do projeto
|      ├── graphics.py  <- Scripts para criar visualizações exploratórias e orientadas a resultados
|      └── models.py    <- Funções utilizadas no modelo
|
├── related            <- Dicionários de dados/ iFood Data Analyst Case.
├── reports            <- Relatório gerado durante o projeto utilizando a biblioteca [ydata-profiling]
│   └── images        <- Gráficos e figuras gerados para serem usados em relatórios
├── environment.yml       <- O arquivo de requisitos para reproduzir o ambiente de análise
├── LICENSE            <- Licença de código aberto se uma for escolhida
├── README.md          <- README principal para desenvolvedores que usam este projeto.
|
```

## Configuração do ambiente

1. Faça o clone do repositório que será criado a partir deste modelo.

    ```bash
    git clone ENDERECO_DO_REPOSITORIO
    ```

2. Crie um ambiente virtual para o seu projeto utilizando o gerenciador de ambientes de sua preferência.

    a. Caso esteja utilizando o `conda`, exporte as dependências do ambiente para o arquivo `ambiente.yml`:

      ```bash
      conda env export > ambiente.yml
      ```

    b. Caso esteja utilizando outro gerenciador de ambientes, exporte as dependências
    para o arquivo `requirements.txt` ou outro formato de sua preferência. Adicione o
    arquivo ao controle de versão, removendo o arquivo `ambiente.yml`.



Para mais informações sobre como usar Git e GitHub, [clique aqui](https://cienciaprogramada.com.br/2021/09/guia-definitivo-git-github/). Sobre ambientes virtuais, [clique aqui](https://cienciaprogramada.com.br/2020/08/ambiente-virtual-projeto-python/).



## Como reproduzir o projeto

O projeto foi desenvolvido utilizando o Python 3.11.5. Para reproduzir o projeto, crie um ambiente virtual com o Conda, ou ferramenta similar, com o Python 3.11.5 e instale as bibliotecas abaixo:

| Biblioteca       | Versão |
| ---------------- | ------ |
| Imbalanced-Learn | 0.11.0 |
| Matplotlib       | 3.7.2  |
| NumPy            | 1.24.3 |
| Pandas           | 1.5.3  |
| Scikit-Learn     | 1.3.0  |
| Seaborn          | 0.12.2 |

Essas são as bibliotecas principais utilizadas no projeto. O relatório foi gerado com a biblioteca [ydata-profiling](https://github.com/ydataai/ydata-profiling), instale-a se quiser reproduzir o relatório. 

# Tech Challenge - Pipeline Batch Bovespa

<br>Tech Challenge é o projeto da fase que englobará os conhecimentos obtidos em todas as disciplinas da fase.

<br>Pipeline Batch Bovespa: ingestão e arquitetura de dados
<br>Neste projeto deve se construir um pipeline de dados completo para extrair, processar e analisar dados do pregão da B3, utilizando AWS S3, Glue, Lambda e Athena. 

<br>Para esse desafio, sua entrega deve conter os seguintes requisitos:
<br><br>Requisito 1: scrap de dados do site da B3 com dados do pregão.
<br>Requisito 2: os dados brutos devem ser ingeridos no s3 em formato parquet com partição diária.
<br>Requisito 3: o bucket deve acionar uma lambda, que por sua vez irá chamar o job de ETL no glue.
<br>Requisito 4: a lambda pode ser em qualquer linguagem. Ela apenas deverá iniciar o job Glue.
<br>Requisito 5: o job Glue deve ser feito no modo visual. Este job deve conter as seguintes transformações obrigatórias:
<br>&nbsp;&nbsp;&nbsp;A: agrupamento numérico, sumarização, contagem ou soma.
<br>&nbsp;&nbsp;&nbsp;B: renomear duas colunas existentes além das de agrupamento.
<br>&nbsp;&nbsp;&nbsp;C: realizar um cálculo com campos de data, exemplo, poder ser du-ração, comparação, diferença entre datas.
<br>Requisito 6: os dados refinados no job glue devem ser salvos no formato parquet em uma pasta chamada refined, particionado por data e pelo nome ou abreviação da ação do pregão.
<br>Requisito 7: o job Glue deve automaticamente catalogar o dado no Glue Catalog e criar uma tabela no banco de dados default do Glue Catalog.
<br>Requisito 8: os dados devem estar disponíveis e legíveis no Athena.


---
## Diagrama de Arquitetura

![Arquitetura da API](./images/arquitetura.png)

---

5mlet_tc_fase_2/<br>
├── glue/<br>
│   └─  glue-job-stl-b3.py<br>
├── images/<br>
│   └── arquitetura.jpg<br>
├── lambda/<br>
│   └─  glue_trigger.py<br>
├── venv/<br>
├── scrap_b3.py/<br>
├── requirements.txt<br>
└── README.md  <br>


## Requisitos

- **Python 3.7 ou superior**
- **pip** (gerenciador de pacotes)

## Dependências

- **boto3**
- **pandas**
- **requests**
- **pyarrow**



### Autor 👨‍💻
Desenvolvido por: Dennis Rocha. [(Linkedin)](https://www.linkedin.com/in/dennissrocha/)
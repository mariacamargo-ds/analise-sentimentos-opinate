# Dashboard Interativo Opinate: Análise de Sentimentos em Debates Políticos Acadêmicos

> Projeto Integrador III — Ciência de Dados | Fatec Cotia  
> Parceria com a plataforma **[Opinate](https://opinate.com.br)** (Neo Reformata)

---

## Sobre o Projeto

A **Opinate** é uma plataforma de debates políticos públicos e privados desenvolvida com um princípio central: ser livre de manipulação algorítmica. Sem bots, sem engajamento artificial, sem bolhas de filtro. Apenas argumentação.

Este projeto aplica **Processamento de Linguagem Natural (NLP)** sobre textos de debate político em português brasileiro, com o objetivo de identificar automaticamente a polaridade de sentimento (positivo, negativo, neutro) em postagens universitárias, gerando insumos para análise de tendências socio-políticas no ambiente acadêmico.

A motivação técnica é direta: **não existe dataset público com a label "debate político acadêmico em PT-BR"**. Esse projeto preenche essa lacuna com uma abordagem de geração de dados sintéticos orientada a domínio, combinada com fine-tuning de modelo transformer especializado em português.

---

## Pipeline

```
TweetSentBR (benchmark base)
        │
        ▼
Benchmark Zero-Shot  ──►  Seleção de modelo por F1-Macro
        │
        ▼
Dataset Sintético Universitário (35.000 amostras · 10 universidades)
        │
        ▼
Fine-Tuning  ──►  pysentimiento/RoBERTuito ajustado ao domínio
        │
        ▼
[em andamento]  Protótipo Streamlit + FastAPI + DeepSeek API
```

---

## Benchmark Zero-Shot

Avaliação comparativa de três modelos multilíngues/PT-BR sobre o dataset **TweetSentBR** (2.010 amostras de teste), sem qualquer ajuste fino:

| Modelo | F1-Macro | Decisão |
|---|---|---|
| `cardiffnlp/twitter-xlm-roberta-base-sentiment` | — | Descartado |
| `distilbert-base-multilingual-cased` | — | Descartado |
| `pysentimiento/robertuito-sentiment-analysis` | **0.8897** | ✅ **Eleito** |

**Por que o pysentimiento?** O RoBERTuito foi pré-treinado sobre 500 milhões de tweets em espanhol e português, o que o torna estruturalmente mais adequado ao domínio informal de redes sociais e debates online em PT-BR. O desempenho zero-shot superior indicou que a representação interna do modelo já captura bem as nuances lexicais do português brasileiro coloquial, exatamente o registro presente nos debates da Opinate.

---

## Dataset Sintético

Para o fine-tuning, foi gerado um corpus de postagens universitárias simulando **35.000 estudantes de 10 universidades, públicas e particulares, brasileiras**:

`USP · UNICAMP · UFMG · UFRJ · UFBA · UnB · FGV · PUC-SP · Mackenzie · Insper`

Cada perfil institucional possui templates de linguagem próprios, refletindo variações de registro, vocabulário e posicionamento político típicos de cada ambiente acadêmico. Os tópicos cobrem o espectro político-social brasileiro de 2023–2025.

**Decisão técnica crítica:** a atribuição de sentimento é derivada diretamente do bloco de template selecionado, não de um sorteio independente. Isso elimina a incoerência semântica entre conteúdo do post e label, que foi o principal bug corrigido ao longo das iterações do gerador (`gerar_post_v3`).

---

## Fine-Tuning

O fine-tuning do `pysentimiento/robertuito-sentiment-analysis` foi realizado sobre uma base inicial de ~725 postagens sintéticas.

**Resultado observado:** convergência para F1-Macro 1.0000 a partir da época 2 — identificado como **overfitting**, dado o tamanho reduzido do dataset e a regularidade dos templates de geração.

**Plano de mitigação:** expansão da base para ~2.500 postagens com maior diversidade de temas e variações de template, seguida de re-treinamento com monitoramento de validação.

---

## Estrutura do Repositório

```
sentiment-opinate/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/                  # instrução de download do TweetSentBR
│   └── synthetic/            # dataset sintético gerado
│
├── notebooks/
│   ├── 01_benchmark_zeroshot.ipynb
│   └── 02_finetuning_pysentimiento.ipynb
│
└── src/
    └── dataset_generator.py  # módulo de geração sintética (gerar_post_v3)
```

---

## Instalação

```bash
git clone https://github.com/seu-usuario/sentiment-opinate.git
cd sentiment-opinate
pip install -r requirements.txt
```

---

## Tecnologias

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-FFD21E?style=flat&logo=huggingface&logoColor=black)
![pysentimiento](https://img.shields.io/badge/pysentimiento-RoBERTuito-blueviolet?style=flat)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=flat&logo=jupyter&logoColor=white)

- `transformers` · `datasets` · `pysentimiento`
- `pandas` · `numpy` · `scikit-learn`
- `streamlit` · `fastapi` *(protótipo — em andamento)*

---

## Status

| Etapa | Status |
|---|---|
| Benchmark zero-shot | ✅ Concluído |
| Geração do dataset sintético | ✅ Concluído |
| Fine-tuning (rodada inicial) | ✅ Concluído |
| Expansão do dataset + re-treino | 🔄 Em andamento |
| Protótipo Streamlit + FastAPI | 🔄 Em andamento |
| Integração DeepSeek API | ⏳ Planejado |

---

## Contexto Acadêmico

Desenvolvido como **Projeto Integrador III** no curso de Tecnologia em Ciência de Dados da **Fatec Cotia**, em parceria com a **Neo Reformata** (plataforma Opinate).

---

## Autora

**Maria Eduarda da Cruz de Camargo & Yghor Kristian Andrade**  
Estudante de Ciência de Dados · Fatec Cotia  
[LinkedIn](https://linkedin.com/in/seu-perfil) · [GitHub](https://github.com/mariacamargo-ds)

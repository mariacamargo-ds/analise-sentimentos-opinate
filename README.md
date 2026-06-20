# Dashboard Interativo Opinate: Análise de Sentimentos em Debates Políticos Acadêmicos

> Projeto Integrador III — Ciência de Dados · Fatec Cotia
> Inspirado na plataforma **[Opinate](https://opinate.com.br)** (Neo Reformata)

---

## Sobre o Projeto

A **Opinate** é uma plataforma de debates políticos para o ambiente acadêmico, livre de manipulação algorítmica — sem bots, sem engajamento artificial, sem bolhas de filtro.

Este projeto aplica **Processamento de Linguagem Natural (NLP)** sobre textos de debate político em português brasileiro, classificando automaticamente o sentimento (positivo, negativo, neutro) de postagens universitárias sintéticas, e entrega essa análise num **protótipo interativo em Streamlit**, com camada adicional de insight contextual via IA generativa.

A motivação técnica: **não existe dataset público rotulado para "debate político acadêmico em PT-BR"**. O projeto preenche essa lacuna com geração de dados sintéticos orientada a domínio, fine-tuning de um transformer especializado em português, e um painel de visualização que transforma os resultados em decisão.

---

## Pipeline

```
TweetSentBR (benchmark base)
        │
        ▼
Benchmark Zero-Shot  ──►  Seleção de modelo por F1-Macro
        │
        ▼
Dataset Sintético Universitário (725 amostras · 10 universidades · 15 temas)
        │
        ▼
Fine-Tuning  ──►  pysentimiento/RoBERTuito ajustado ao domínio
        │
        ▼
Protótipo Streamlit  ──►  Feed de debates · Thread + sentimento · Insights com gráficos
        │
        ▼
Insight contextual via DeepSeek API
```

---

## Benchmark Zero-Shot

Avaliação comparativa de modelos multilíngues/PT-BR sobre o dataset **TweetSentBR** (2.010 amostras de teste), sem ajuste fino:

| Modelo | F1-Macro | Decisão |
|---|---|---|
| `cardiffnlp/twitter-xlm-roberta-base-sentiment` | 0.7092 | ❌ Descartado |
| `distilbert-base-multilingual-cased` | 0.4086 | ❌ Descartado |
| `pysentimiento/robertuito-sentiment-analysis` | **0.8897** | ✅ **Eleito** |

**Por que o pysentimiento?** O RoBERTuito foi pré-treinado sobre 500 milhões de tweets em espanhol e português, tornando-o estruturalmente mais adequado ao domínio informal de redes sociais em PT-BR — exatamente o registro presente nos debates da Opinate.

---

## Dataset Sintético

Corpus de postagens universitárias simulando estudantes de **10 universidades brasileiras** (`USP · UNICAMP · UFMG · UFRJ · UFBA · UnB · FGV · PUC-SP · Mackenzie · Insper`) debatendo **15 temas** do espectro político-social brasileiro.

> 📓 A geração completa está documentada nos notebooks `sprint04_base_academico.ipynb` e `Bases_Iniciais_b2b_b2c.ipynb`. Uma amostra está disponível em `dados-projeto/base-sintetica-academica/amostra-posts.csv`.

**Decisão técnica:** o sentimento é derivado diretamente do template de conteúdo selecionado — não de um sorteio independente — eliminando incoerência semântica entre post e label.

---

## Fine-Tuning

Fine-tuning do `pysentimiento/robertuito-sentiment-analysis` sobre **725 postagens sintéticas**.

**Resultado observado:** convergência para F1-Macro ≈1.0000 a partir da época 2 — **overfitting identificado e documentado**, dado o tamanho reduzido do dataset e a regularidade dos templates de geração.

**Plano de mitigação:** expansão da base (~2.500 amostras com maior diversidade temática) e re-treinamento com monitoramento de validação — próxima iteração do projeto.

---

## Protótipo Interativo (Streamlit)

Interface que aplica o pipeline completo num ambiente de uso real, com identidade visual inspirada na Opinate:

| Tela | O que mostra |
|---|---|
| **Feed** | Lista de debates abertos, com barra de distribuição de sentimentos por thread, filtros por universidade/tema/sentimento e busca |
| **Thread** | Posts individuais com badge de sentimento, painel de análise da thread e classificador de texto livre em tempo real |
| **Insights** | Gráficos de distribuição geral, sentimento × universidade, sentimento × perfil político, polarização por tema e engajamento por universidade |

**Camada de IA:**
- **pysentimiento (fine-tunado)** classifica sentimento de novos textos em tempo real, localmente
- **DeepSeek API** gera um insight contextual em linguagem natural sobre cada thread, a partir da amostra de posts e da distribuição de sentimentos

Modo claro/escuro disponível, com identidade visual e navegação customizadas.

Confira o protótipo na plataforma Streamlit: 

### Como rodar localmente

```bash
# 1. Clone o repositório
git clone https://github.com/mariacamargo-ds/analise-sentimentos-opinate.git
cd analise-sentimentos-opinate

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Configure sua chave da DeepSeek
mkdir .streamlit
echo 'DEEPSEEK_API_KEY = "sua_chave_aqui"' > .streamlit/secrets.toml

# 4. Rode o app
streamlit run app.py
```

O app abre automaticamente em `http://localhost:8501`.

> ⚠️ O modelo fine-tunado (`modelo_finetuned/`) não está incluso no repositório por tamanho. Rode o notebook `finetuning_pysent.ipynb` para gerá-lo localmente, ou o app usa o modelo pysentimiento original como fallback.

---

## Estrutura do Repositório

```
analise-sentimentos-opinate/
│
├── app.py                          # entrada do Streamlit — navegação, tema, layout
├── requirements.txt
├── .gitignore
│
├── .streamlit/
│   └── secrets.toml                # chave DeepSeek (não versionado)
│
├── assets/                         # logo, ícones de navegação e identidade visual
│
├── pages/
│   ├── feed.py                     # tela 1 — feed de debates
│   ├── thread.py                   # tela 2 — thread detalhada + classificador
│   └── insights.py                 # tela 3 — painel de gráficos
│
├── utils/
│   ├── data.py                     # carregamento e cache dos dados
│   ├── sentiment.py                # carrega modelo fine-tunado, classifica texto
│   └── deepseek.py                 # geração de insight contextual via API
│
├── dados-projeto/
│   ├── base-sintetica-academica/
│   │   └── amostra-posts.csv       # amostra do dataset sintético (725 posts)
│   └── raw/
│       └── README.md               # instruções de download do TweetSentBR
│
└── notebooks/
    ├── Bases_Iniciais_b2b_b2c.ipynb
    ├── sprint04_base_academico.ipynb   # geração do dataset sintético
    ├── modelos_test.ipynb              # benchmark zero-shot
    └── finetuning_pysent.ipynb         # fine-tuning do pysentimiento
```

---

## Tecnologias

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-FFD21E?style=flat&logo=huggingface&logoColor=black)
![pysentimiento](https://img.shields.io/badge/pysentimiento-RoBERTuito-blueviolet?style=flat)
![Plotly](https://img.shields.io/badge/Plotly-Charts-3F4F75?style=flat&logo=plotly&logoColor=white)
![DeepSeek](https://img.shields.io/badge/DeepSeek-API-0d6ad6?style=flat)

- `transformers` · `datasets` · `pysentimiento` · `torch`
- `pandas` · `numpy`
- `streamlit` · `plotly`
- `openai` (SDK usado para conectar à API da DeepSeek)

---

## Status

| Etapa | Status |
|---|---|
| Benchmark zero-shot | ✅ Concluído |
| Geração do dataset sintético | ✅ Concluído |
| Fine-tuning (rodada inicial) | ✅ Concluído — overfitting documentado |
| Protótipo Streamlit (Feed · Thread · Insights) | ✅ Concluído |
| Integração DeepSeek API | ✅ Concluído |
| Expansão do dataset + re-treino | 🔄 Próxima iteração |

---

## Contexto Acadêmico

Desenvolvido como **Projeto Integrador III** no curso de Tecnologia em Ciência de Dados da **Fatec Cotia**.

---

## Autores

**Maria Camargo e Yghor Andrade**

Estudantes de Ciência de Dados · Fatec Cotia

[GitHub – Maria Camargo](https://github.com/mariacamargo-ds)

[GitHub – Yghor Andrade](https://github.com/mariacamargo-ds)

import streamlit as st
from pathlib import Path
from transformers import pipeline

MODEL_PATH = Path(__file__).resolve().parent.parent.parent / "modelo_finetuned"

LABEL_MAP = {
    "POS": "positivo",
    "NEG": "negativo",
    "NEU": "neutro",
    "LABEL_0": "negativo",
    "LABEL_1": "neutro",
    "LABEL_2": "positivo",
}

CORES = {
    "positivo": "#1D9E75",
    "negativo": "#E24B4A",
    "neutro":   "#888780",
}

EMOJIS = {
    "positivo": "🟢",
    "negativo": "🔴",
    "neutro":   "⚪",
}

@st.cache_resource(show_spinner="Carregando modelo de sentimentos...")
def carregar_modelo():
    if not MODEL_PATH.exists():
        st.warning(f"Modelo não encontrado em {MODEL_PATH}. Usando pysentimiento padrão.")
        return pipeline(
            "text-classification",
            model="pysentimiento/robertuito-sentiment-analysis"
        )
    return pipeline("text-classification", model=str(MODEL_PATH))

def classificar(texto: str) -> str:
    clf = carregar_modelo()
    resultado = clf(texto[:512])[0]["label"]
    return LABEL_MAP.get(resultado, resultado.lower())

def classificar_lote(textos: list[str]) -> list[str]:
    clf = carregar_modelo()
    resultados = clf([t[:512] for t in textos], batch_size=16)
    return [LABEL_MAP.get(r["label"], r["label"].lower()) for r in resultados]

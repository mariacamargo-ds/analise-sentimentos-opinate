import streamlit as st
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "dados-projeto" / "base-sintetica-academica"
OPINATE_DIR = BASE_DIR.parent / "opinate_data"

@st.cache_data
def carregar_posts() -> pd.DataFrame:
    caminho = OPINATE_DIR / "df_posts.csv"
    if not caminho.exists():
        caminho = DATA_DIR / "amostra-posts.csv"
    df = pd.read_csv(caminho, encoding="utf-8-sig")
    df.columns = df.columns.str.strip().str.lower()
    df["sentimento"] = df["sentimento"].str.strip().str.lower()
    return df

@st.cache_data
def carregar_threads() -> pd.DataFrame:
    caminho = OPINATE_DIR / "df_threads.csv"
    if not caminho.exists():
        return pd.DataFrame()
    df = pd.read_csv(caminho, encoding="utf-8-sig")
    df.columns = df.columns.str.strip().str.lower()
    return df

@st.cache_data
def carregar_usuarios() -> pd.DataFrame:
    caminho = OPINATE_DIR / "df_usuarios.csv"
    if not caminho.exists():
        return pd.DataFrame()
    df = pd.read_csv(caminho, encoding="utf-8-sig")
    df.columns = df.columns.str.strip().str.lower()
    return df

def posts_por_thread(thread_id: str, df_posts: pd.DataFrame) -> pd.DataFrame:
    col = "thread_id" if "thread_id" in df_posts.columns else "tema"
    return df_posts[df_posts[col] == thread_id].reset_index(drop=True)

def resumo_sentimentos(df: pd.DataFrame) -> dict:
    if df.empty or "sentimento" not in df.columns:
        return {"positivo": 0, "negativo": 0, "neutro": 0}
    contagem = df["sentimento"].value_counts(normalize=True) * 100
    return {
        "positivo": round(contagem.get("positivo", 0), 1),
        "negativo": round(contagem.get("negativo", 0), 1),
        "neutro":   round(contagem.get("neutro",   0), 1),
    }

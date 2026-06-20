import os
import streamlit as st
from openai import OpenAI

@st.cache_resource
def _cliente():
    api_key = os.getenv("DEEPSEEK_API_KEY") or st.secrets.get("DEEPSEEK_API_KEY", "")
    return OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

def gerar_insight(tema: str, posts: list[dict], dist: dict) -> str:
    """
    posts: lista de dicts com chaves 'conteudo' e 'sentimento'
    dist:  dict com 'positivo', 'negativo', 'neutro' em %
    """
    amostra = "\n".join(
        f"[{p['sentimento'].upper()}] {p['conteudo'][:200]}"
        for p in posts[:15]
    )

    prompt = f"""Você é um analista de opinião especializado em debates acadêmicos brasileiros.

Tema do debate: "{tema}"

Distribuição de sentimentos:
- Positivo: {dist['positivo']}%
- Negativo: {dist['negativo']}%
- Neutro:   {dist['neutro']}%

Amostra de posts (até 15):
{amostra}

Com base nisso, escreva um parágrafo curto (3-4 frases) com:
1. O clima predominante e sua provável causa
2. Os principais pontos de divergência entre os participantes
3. Uma observação sobre o padrão de engajamento

Seja direto, analítico e use linguagem acessível. Não repita os números,interprete-os. Faça uma análise, com no máximo, 12 linhas. Se necessário, pule linhas e inicie um novo parágrafo."""

    try:
        resp = _cliente().chat.completions.create(
            model="deepseek-v4-flash",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Não foi possível gerar o insight: {e}"

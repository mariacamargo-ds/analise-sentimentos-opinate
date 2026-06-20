import streamlit as st
import pandas as pd
from utils.data import carregar_posts, resumo_sentimentos

CORES  = {"positivo": "#1D9E75", "negativo": "#E24B4A", "neutro": "#888780"}
LABELS = {"positivo": "🟢 positivo", "negativo": "🔴 negativo", "neutro": "⚪ neutro"}

TOPIC_COLORS = {
    "Educação":      "#E6F1FB:#185FA5",
    "Política":      "#FAEEDA:#854F0B",
    "Saúde":         "#EEEDFE:#534AB7",
    "Economia":      "#E1F5EE:#0F6E56",
    "Meio Ambiente": "#E8F5E3:#2D6A1F",
    "Tecnologia":    "#FDE8FB:#7A1FA5",
    "Segurança":     "#FBEBEB:#A32D2D",
    "Cultura":       "#FFF3E0:#B35C00",
}

def _badge_tema(tema):
    cores = TOPIC_COLORS.get(tema, "#F1EFE8:#5F5E5A").split(":")
    return f'<span style="font-size:11px;background:{cores[0]};color:{cores[1]};padding:3px 10px;border-radius:10px;font-weight:500;">{tema}</span>'

def _barra(dist):
    return f"""
    <div style="display:flex;gap:3px;margin-top:10px;height:5px;border-radius:4px;overflow:hidden;">
      <div style="width:{dist['positivo']}%;background:#1D9E75;"></div>
      <div style="width:{dist['negativo']}%;background:#E24B4A;"></div>
      <div style="width:{dist['neutro']}%;background:#888780;"></div>
    </div>
    <div style="display:flex;gap:14px;margin-top:5px;">
      <span style="font-size:11px;color:#1D9E75;">{dist['positivo']}% pos</span>
      <span style="font-size:11px;color:#E24B4A;">{dist['negativo']}% neg</span>
      <span style="font-size:11px;color:#888780;">{dist['neutro']}% neu</span>
    </div>"""

def render(card_bg, text, border, teal):
    df_posts = carregar_posts()

    # ── Filtros ────────────────────────────────────────────────────────────────
    col_busca, col_univ, col_tema, col_sent = st.columns([3, 2, 2, 2])
    with col_busca:
        busca = st.text_input("", placeholder="🔍  Buscar debates...", label_visibility="collapsed")
    universidades = ["Todas"] + sorted(df_posts["universidade"].dropna().unique().tolist()) \
        if "universidade" in df_posts.columns else ["Todas"]
    with col_univ:
        univ_sel = st.selectbox("Universidade", universidades, label_visibility="collapsed")
    temas = ["Todos os temas"] + sorted(df_posts["tema"].dropna().unique().tolist()) \
        if "tema" in df_posts.columns else ["Todos os temas"]
    with col_tema:
        tema_sel = st.selectbox("Tema", temas, label_visibility="collapsed")
    with col_sent:
        sent_sel = st.selectbox("Sentimento", ["Todos", "Positivo", "Negativo", "Neutro"],
                                label_visibility="collapsed")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Agrupamento ────────────────────────────────────────────────────────────
    col_agrupa = "thread_id" if "thread_id" in df_posts.columns else "tema"
    threads = []
    for chave, grupo in df_posts.groupby(col_agrupa):
        dist = resumo_sentimentos(grupo)
        predominante = max(dist, key=dist.get)
        tema = grupo["tema"].iloc[0] if "tema" in grupo.columns else str(chave)
        univs = grupo["universidade"].dropna().unique().tolist() if "universidade" in grupo.columns else []
        threads.append({
            "id": chave, "tema": tema, "dist": dist,
            "predominante": predominante, "n_posts": len(grupo),
            "n_univs": len(univs), "univs": univs[:3],
            "titulo": tema,
        })

    # ── Filtros aplicados ──────────────────────────────────────────────────────
    if busca:
        threads = [t for t in threads if busca.lower() in t["titulo"].lower()]
    if univ_sel != "Todas":
        threads = [t for t in threads if univ_sel in t["univs"]]
    if tema_sel != "Todos os temas":
        threads = [t for t in threads if t["tema"] == tema_sel]
    if sent_sel != "Todos":
        threads = [t for t in threads if t["predominante"] == sent_sel.lower()]

    if not threads:
        st.info("Nenhum debate encontrado com os filtros aplicados.")
        return

    # ── Paginação ──────────────────────────────────────────────────────────────
    if "feed_pagina" not in st.session_state:
        st.session_state.feed_pagina = 1
    POR_PAGINA = 5
    exibir = threads[:st.session_state.feed_pagina * POR_PAGINA]
    tem_mais = len(threads) > len(exibir)

    # ── Cards ──────────────────────────────────────────────────────────────────
    for t in exibir:
        cor_badge = CORES[t["predominante"]]
        univs_str = " · ".join(t["univs"]) + (" e outras" if t["n_univs"] > 3 else "")

        st.markdown(f"""
        <div style="background:{card_bg};border:1px solid {border};border-radius:14px;
                    padding:20px 24px;margin-bottom:12px;
                    box-shadow:0 1px 3px rgba(0,0,0,0.04);">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:16px;">
            <div style="flex:1;min-width:0;">
              <div style="display:flex;gap:8px;align-items:center;margin-bottom:10px;flex-wrap:wrap;">
                {_badge_tema(t['tema'])}
                <span style="font-size:11px;color:#888780;">· {t['n_posts']} posts · {t['n_univs']} universidades</span>
              </div>
              <p style="font-size:15px;font-weight:500;color:{text};margin:0 0 5px;
                        white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{t['titulo']}</p>
              <p style="font-size:12px;color:#888780;margin:0;">{univs_str}</p>
            </div>
            <div style="flex-shrink:0;text-align:right;">
              <span style="font-size:12px;font-weight:500;color:{cor_badge};
                           background:{cor_badge}18;padding:4px 12px;border-radius:10px;">
                {t['predominante']}
              </span>
            </div>
          </div>
          {_barra(t['dist'])}
        </div>
        """, unsafe_allow_html=True)

        if st.button("Ver debate →", key=f"btn_{t['id']}"):
            st.session_state["thread_ativa"] = t["id"]
            st.session_state["thread_tema"]  = t["tema"]
            st.session_state.pagina = "thread"
            st.rerun()

    # ── Rodapé / Carregar mais ─────────────────────────────────────────────────
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    if tem_mais:
        col_c, col_info, col_d = st.columns([2, 3, 2])
        with col_info:
            st.markdown(f"""
            <div style="text-align:center;color:#888780;font-size:12px;margin-bottom:8px;">
              Exibindo {len(exibir)} de {len(threads)} debates
            </div>""", unsafe_allow_html=True)
            if st.button("↓  Carregar mais debates", key="load_more", use_container_width=True):
                st.session_state.feed_pagina += 1
                st.rerun()
    else:
        st.markdown(f"""
        <div style="text-align:center;padding:20px 0 8px;">
          <div style="display:inline-flex;align-items:center;gap:8px;
                      color:#888780;font-size:12px;background:#F1EFE8;
                      padding:8px 20px;border-radius:20px;">
            ✓ Todos os {len(threads)} debates carregados
          </div>
        </div>""", unsafe_allow_html=True)

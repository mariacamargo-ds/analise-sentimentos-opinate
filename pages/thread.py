import streamlit as st
from utils.data import carregar_posts, resumo_sentimentos
from utils.sentiment import classificar, CORES, EMOJIS
from utils.deepseek import gerar_insight

AVATAR_PALETTES = [
    ("#E1F5EE","#0F6E56"),("#E6F1FB","#185FA5"),("#EEEDFE","#534AB7"),
    ("#FAEEDA","#854F0B"),("#FBEBEB","#A32D2D"),("#F1EFE8","#5F5E5A"),
]

def _avatar(nome, bg, cor):
    partes = [p for p in str(nome).split(".") if p]
    iniciais = "".join([p[0].upper() for p in partes[:2]]) or "U"
    return (
        f"<div style='width:36px;height:36px;border-radius:50%;"
        f"background:{bg};color:{cor};display:flex;align-items:center;"
        f"justify-content:center;font-size:12px;font-weight:500;"
        f"flex-shrink:0;'>{iniciais}</div>"
    )

def render(card_bg, text, border, teal, teal_dark, escuro):
    df_posts = carregar_posts()

    # ── Botão voltar ───────────────────────────────────────────────────────────
    if st.button("← Voltar ao feed", key="btn_voltar"):
        st.session_state.pop("thread_ativa", None)
        st.session_state.pop("thread_tema", None)
        st.session_state["pagina"] = "feed"
        st.rerun()

    thread_id = st.session_state.get("thread_ativa")
    tema      = st.session_state.get("thread_tema", "Thread")

    # ── Sem thread selecionada: só orienta a voltar ao feed ────────────────────
    if not thread_id:
        st.markdown(
            f"<div style='background:{card_bg};border:1px solid {border};"
            f"border-radius:12px;padding:40px 24px;text-align:center;margin-top:24px;'>"
            f"<p style='font-size:14px;color:{text};margin:0 0 6px;'>Nenhum debate selecionado</p>"
            f"<p style='font-size:12px;color:#888780;margin:0;'>"
            f"Acesse o <b>Feed</b> e clique em \"Ver debate →\" em qualquer card "
            f"para abrir a análise completa aqui.</p>"
            f"</div>",
            unsafe_allow_html=True
        )
        return

    # ── Thread selecionada: carrega posts ──────────────────────────────────────
    col_agrupa   = "thread_id" if "thread_id" in df_posts.columns else "tema"
    df_thread    = df_posts[df_posts[col_agrupa] == thread_id].reset_index(drop=True)
    dist         = resumo_sentimentos(df_thread)
    predominante = max(dist, key=dist.get)

    col_posts, col_painel = st.columns([2, 1], gap="medium")

    # ════════════════════════════════════════════════════════
    # COLUNA ESQUERDA — posts
    # ════════════════════════════════════════════════════════
    with col_posts:
        st.markdown(
            f"<div style='margin-bottom:16px;'>"
            f"<h2 style='font-size:18px;font-weight:500;color:{text};margin:0 0 4px;'>{tema}</h2>"
            f"<p style='font-size:12px;color:#888780;'>{len(df_thread)} posts · debate aberto</p>"
            f"</div>",
            unsafe_allow_html=True
        )

        # Classificador
        st.markdown(
            f"<div style='background:{card_bg};border:1px solid {border};"
            f"border-radius:12px;padding:14px 16px;margin-bottom:16px;'>"
            f"<p style='font-size:13px;font-weight:500;color:{text};margin:0 0 10px;'>"
            f"Compartilhe sua ideia 💡</p>",
            unsafe_allow_html=True
        )
        novo = st.text_input(
            "classificar_input",
            placeholder="Digite um post para classificar o sentimento...",
            label_visibility="collapsed",
            key="input_classificar"
        )
        if st.button("Classificar →", key="btn_classificar"):
            if novo.strip():
                with st.spinner("Classificando..."):
                    label = classificar(novo)
                cor_l = CORES[label]
                em_l  = EMOJIS[label]
                st.markdown(
                    f"<div style='background:{cor_l}18;border:1px solid {cor_l};"
                    f"border-radius:8px;padding:10px 14px;margin-top:8px;'>"
                    f"<span style='font-size:13px;font-weight:500;color:{cor_l};'>"
                    f"{em_l} Sentimento detectado: {label.upper()}</span></div>",
                    unsafe_allow_html=True
                )
            else:
                st.warning("Digite algum texto antes de classificar.")
        st.markdown("</div>", unsafe_allow_html=True)

        # Lista de posts
        for i, row in df_thread.iterrows():
            sent     = str(row.get("sentimento", "neutro")).lower()
            cor      = CORES.get(sent, "#888780")
            emoji    = EMOJIS.get(sent, "⚪")
            perfil   = str(row.get("perfil", ""))
            univ     = str(row.get("universidade", ""))
            conteudo = str(row.get("conteudo", ""))
            palette  = AVATAR_PALETTES[i % len(AVATAR_PALETTES)]
            av       = _avatar(perfil or f"U{i}", palette[0], palette[1])
            st.markdown(
                f"<div style='background:{card_bg};border:1px solid {border};"
                f"border-radius:12px;padding:14px;margin-bottom:8px;'>"
                f"<div style='display:flex;gap:12px;align-items:flex-start;'>"
                f"{av}"
                f"<div style='flex:1;'>"
                f"<div style='display:flex;justify-content:space-between;align-items:center;'>"
                f"<span style='font-size:13px;font-weight:500;color:{text};'>{perfil or f'usuário_{i}'}</span>"
                f"<span style='font-size:11px;font-weight:500;color:{cor};"
                f"background:{cor}18;padding:2px 10px;border-radius:10px;'>{emoji} {sent}</span>"
                f"</div>"
                f"<p style='font-size:11px;color:#888780;margin:2px 0 8px;'>{univ}</p>"
                f"<p style='font-size:13px;color:{text};line-height:1.6;margin:0;'>{conteudo}</p>"
                f"</div></div></div>",
                unsafe_allow_html=True
            )

    # ════════════════════════════════════════════════════════
    # COLUNA DIREITA — painel de análise
    # ════════════════════════════════════════════════════════
    with col_painel:
        cor_pred = CORES.get(predominante, "#888780")
        em_pred  = EMOJIS.get(predominante, "")

        # Distribuição
        st.markdown(
            f"<div style='background:{card_bg};border:1px solid {border};"
            f"border-radius:12px;padding:16px;margin-bottom:12px;'>"
            f"<p style='font-size:11px;font-weight:500;color:#888780;"
            f"margin:0 0 12px;letter-spacing:0.5px;'>ANÁLISE DA THREAD</p>"
            f"<p style='font-size:12px;color:#888780;margin:0 0 4px;'>Clima predominante</p>"
            f"<p style='font-size:20px;font-weight:500;color:{cor_pred};margin:0 0 16px;'>"
            f"{em_pred} {predominante.capitalize()}</p>",
            unsafe_allow_html=True
        )
        for sent, pct in dist.items():
            cor = CORES[sent]
            st.markdown(
                f"<div style='margin-bottom:10px;'>"
                f"<div style='display:flex;justify-content:space-between;'>"
                f"<span style='font-size:12px;color:#888780;'>{sent.capitalize()}</span>"
                f"<span style='font-size:12px;font-weight:500;color:{cor};'>{pct}%</span>"
                f"</div>"
                f"<div style='height:6px;border-radius:3px;background:#E2E0D830;"
                f"margin-top:4px;overflow:hidden;'>"
                f"<div style='height:100%;width:{pct}%;background:{cor};border-radius:3px;'>"
                f"</div></div></div>",
                unsafe_allow_html=True
            )
        st.markdown("</div>", unsafe_allow_html=True)

        # Insight DeepSeek
        bg_insight = "#0F2920" if escuro else "#E1F5EE"
        st.markdown(
            f"<div style='background:{bg_insight};border:1px solid #5DCAA5;"
            f"border-radius:12px;padding:16px;margin-bottom:12px;'>"
            f"<p style='font-size:12px;font-weight:500;color:{teal};margin:0 0 8px;'>"
            f"✨ Insight IA · DeepSeek</p>",
            unsafe_allow_html=True
        )

        if "insight_gerado" not in st.session_state:
            st.session_state["insight_gerado"] = None
        if "insight_thread" not in st.session_state:
            st.session_state["insight_thread"] = None
        if st.session_state["insight_thread"] != thread_id:
            st.session_state["insight_gerado"] = None

        if st.session_state["insight_gerado"]:
            st.markdown(
                f"<p style='font-size:12px;color:#888780;line-height:1.6;margin:0;'>"
                f"{st.session_state['insight_gerado']}</p>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<p style='font-size:12px;color:#888780;font-style:italic;margin:0;'>"
                f"Clique em \"Gerar análise\" para um insight contextual desta thread.</p>",
                unsafe_allow_html=True
            )
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("✨ Gerar análise", key="btn_insight", use_container_width=True):
            posts_lista = df_thread[["conteudo", "sentimento"]].to_dict("records")
            with st.spinner("Analisando contexto da thread..."):
                insight = gerar_insight(tema, posts_lista, dist)
            st.session_state["insight_gerado"] = insight
            st.session_state["insight_thread"] = thread_id
            st.rerun()

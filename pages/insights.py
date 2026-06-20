import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.data import carregar_posts, resumo_sentimentos

CORES_SENT = {"positivo": "#1D9E75", "negativo": "#E24B4A", "neutro": "#888780"}

def _theme(escuro):
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E8E6DE" if escuro else "#1A1A18",
        font_size=12,
    )

def _titulo(label, text):
    return f"<p style='font-size:13px;font-weight:500;color:{text};margin:0 0 4px;'>{label}</p>"

def render(card_bg, text, border, teal, escuro):
    df = carregar_posts()

    if df.empty:
        st.warning("Nenhum dado carregado.")
        return

    # ── Filtros ────────────────────────────────────────────────────────────────
    cf1, cf2, cf3 = st.columns(3)
    univs = ["Todas"] + sorted(df["universidade"].dropna().unique()) if "universidade" in df.columns else ["Todas"]
    temas = ["Todos"] + sorted(df["tema"].dropna().unique())         if "tema"         in df.columns else ["Todos"]

    with cf1: univ_f = st.selectbox("Universidade", univs, key="ins_univ")
    with cf2: tema_f = st.selectbox("Tema",         temas, key="ins_tema")
    with cf3: sent_f = st.selectbox("Sentimento", ["Todos","positivo","negativo","neutro"], key="ins_sent")

    df_f = df.copy()
    if univ_f != "Todas" and "universidade" in df_f.columns: df_f = df_f[df_f["universidade"] == univ_f]
    if tema_f != "Todos" and "tema"         in df_f.columns: df_f = df_f[df_f["tema"]         == tema_f]
    if sent_f != "Todos":                                     df_f = df_f[df_f["sentimento"]   == sent_f]

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Métricas ───────────────────────────────────────────────────────────────
    total   = len(df_f)
    cnt     = df_f["sentimento"].value_counts() if total else {}
    pct_pos = round(cnt.get("positivo",0)/total*100,1) if total else 0
    pct_neg = round(cnt.get("negativo",0)/total*100,1) if total else 0
    n_univs = df_f["universidade"].nunique() if "universidade" in df_f.columns else 0

    m1,m2,m3,m4 = st.columns(4)
    m1.metric("Total de posts",  f"{total:,}")
    m2.metric("Positivos",       f"{pct_pos}%")
    m3.metric("Negativos",       f"{pct_neg}%")
    m4.metric("Universidades",   n_univs)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Linha 1: Donut + Barras por universidade ───────────────────────────────
    c1, c2 = st.columns([1, 2])

    with c1:
        st.markdown(_titulo("Distribuição geral", text), unsafe_allow_html=True)
        dist_df = df_f["sentimento"].value_counts().reset_index()
        dist_df.columns = ["sentimento", "count"]
        fig = px.pie(dist_df, names="sentimento", values="count", hole=0.55,
                     color="sentimento", color_discrete_map=CORES_SENT)
        fig.update_traces(textinfo="percent", textfont_size=12)
        fig.update_layout(**_theme(escuro), height=260,
                          margin=dict(t=10,b=10,l=10,r=10),
                          showlegend=True, legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        if "universidade" in df_f.columns:
            st.markdown(_titulo("Sentimento × Universidade", text), unsafe_allow_html=True)
            grp = df_f.groupby(["universidade","sentimento"]).size().reset_index(name="n")
            fig = px.bar(grp, x="universidade", y="n", color="sentimento",
                         color_discrete_map=CORES_SENT, barmode="stack",
                         labels={"n":"Posts","universidade":"","sentimento":"Sentimento"})
            fig.update_layout(**_theme(escuro), height=260,
                              margin=dict(t=10,b=50,l=10,r=10), xaxis_tickangle=-30)
            st.plotly_chart(fig, use_container_width=True)

    # ── Linha 2: Sentimento × Perfil + Polarização por tema ───────────────────
    c3, c4 = st.columns(2)

    with c3:
        if "perfil" in df_f.columns:
            st.markdown(_titulo("Sentimento × Perfil político", text), unsafe_allow_html=True)
            grp = df_f.groupby(["perfil","sentimento"]).size().reset_index(name="n")
            fig = px.bar(grp, x="n", y="perfil", color="sentimento",
                         color_discrete_map=CORES_SENT, barmode="stack", orientation="h",
                         labels={"n":"Posts","perfil":"","sentimento":"Sentimento"})
            fig.update_layout(**_theme(escuro), height=300,
                              margin=dict(t=10,b=10,l=10,r=10))
            st.plotly_chart(fig, use_container_width=True)

    with c4:
        if "tema" in df_f.columns:
            st.markdown(_titulo("Polarização por tema  (% negativo)", text), unsafe_allow_html=True)
            # Calcula % negativo por tema — temas mais polarizados no topo
            pol = (df_f.groupby("tema")["sentimento"]
                       .apply(lambda x: round((x=="negativo").sum()/len(x)*100, 1))
                       .reset_index())
            pol.columns = ["tema", "pct_neg"]
            pol = pol.sort_values("pct_neg", ascending=True)

            fig = go.Figure(go.Bar(
                x=pol["pct_neg"], y=pol["tema"],
                orientation="h",
                marker=dict(
                    color=pol["pct_neg"],
                    colorscale=[[0,"#1D9E75"],[0.5,"#F5A623"],[1,"#E24B4A"]],
                    showscale=False,
                ),
                text=pol["pct_neg"].apply(lambda v: f"{v}%"),
                textposition="outside",
            ))
            fig.update_layout(
                **_theme(escuro), height=300,
                margin=dict(t=10,b=10,l=10,r=40),
                xaxis=dict(title="% posts negativos", range=[0, pol["pct_neg"].max()+10]),
                yaxis=dict(title=""),
            )
            st.plotly_chart(fig, use_container_width=True)

    # ── Linha 3: Engajamento por universidade ──────────────────────────────────
    if "universidade" in df_f.columns:
        st.markdown(_titulo("Engajamento por universidade", text), unsafe_allow_html=True)
        eng = (df_f.groupby("universidade")
                   .agg(
                       total=("conteudo","count"),
                       pct_pos=("sentimento", lambda x: round((x=="positivo").sum()/len(x)*100,1)),
                       pct_neg=("sentimento", lambda x: round((x=="negativo").sum()/len(x)*100,1)),
                   )
                   .reset_index()
                   .sort_values("total", ascending=False))

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=eng["universidade"], y=eng["total"],
            name="Total de posts", marker_color=teal, opacity=0.8,
        ))
        fig.add_trace(go.Scatter(
            x=eng["universidade"], y=eng["pct_pos"],
            name="% Positivo", mode="lines+markers",
            line=dict(color="#1D9E75", width=2), yaxis="y2",
        ))
        fig.add_trace(go.Scatter(
            x=eng["universidade"], y=eng["pct_neg"],
            name="% Negativo", mode="lines+markers",
            line=dict(color="#E24B4A", width=2, dash="dot"), yaxis="y2",
        ))
        fig.update_layout(
            **_theme(escuro), height=300,
            margin=dict(t=10,b=50,l=10,r=10),
            yaxis=dict(title="Posts"),
            yaxis2=dict(title="%", overlaying="y", side="right", range=[0,100]),
            legend=dict(orientation="h", y=1.08),
            xaxis_tickangle=-30,
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Amostra ────────────────────────────────────────────────────────────────
    if "mostrar_amostra" not in st.session_state:
        st.session_state["mostrar_amostra"] = False

    if st.button("📄 Ver amostra dos dados", key="btn_amostra"):
        st.session_state["mostrar_amostra"] = not st.session_state["mostrar_amostra"]

    if st.session_state["mostrar_amostra"]:
        cols_show = [c for c in ["conteudo","sentimento","tema","universidade","perfil"] if c in df_f.columns]
        st.dataframe(
            df_f[cols_show].sample(min(50, len(df_f)), random_state=1).reset_index(drop=True),
            use_container_width=True, height=280
        )

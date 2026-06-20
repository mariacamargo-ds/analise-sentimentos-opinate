import streamlit as st
import base64
from pathlib import Path

st.set_page_config(
    page_title="Opinate Acadêmico",
    page_icon="assets/favicon.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Estado global ──────────────────────────────────────────────────────────────
if "tema"   not in st.session_state: st.session_state.tema   = "claro"
if "pagina" not in st.session_state: st.session_state.pagina = "feed"

escuro    = st.session_state.tema == "escuro"
TEAL      = "#1D9E75"
TEAL_DARK = "#0F6E56"
TEAL_BG   = "#E1F5EE" if not escuro else "#0A2E20"
BG        = "#F4F3F0" if not escuro else "#161614"
SIDEBAR   = "#FFFFFF"  if not escuro else "#1C1C1A"
TEXT      = "#1A1A18"  if not escuro else "#E8E6DE"
TEXT2     = "#6B6A65"  if not escuro else "#9C9A92"
BORDER    = "#E2E0D8"  if not escuro else "#2E2E2C"
CARD      = "#FFFFFF"  if not escuro else "#222220"

# ════════════════════════════════════════════════════════════════════════════
# CONSTANTES DE TAMANHO — ajuste manual aqui, sem precisar tocar no resto
# ════════════════════════════════════════════════════════════════════════════
NAV_ICON_SIZE_ATIVO   = 28
NAV_ICON_SIZE_INATIVO = 24
NAV_LABEL_SIZE        = 15
NAV_DESC_SIZE         = 11
NAV_ITEM_PADDING      = 12

TOGGLE_HEIGHT        = 64
TOGGLE_ICON_SIZE     = 22
TOGGLE_LABEL_SIZE    = 15

SOCIAL_ICON_SIZE   = 18
SOCIAL_BTN_WIDTH   = 150
SOCIAL_FONT_SIZE   = 13
SOCIAL_TITLE_SIZE  = 12

INSET_BANNER  = 4
INSET_NAVITEM = 4

PAGE_TITLE_SIZE    = 22   # px — tamanho do título da página (ex: "Thread")
PAGE_SUBTITLE_SIZE = 12   # px — tamanho do subtítulo (ex: "Posts, comentários...")

KPI_VALUE_SIZE = 16   # px — tamanho do número (ex: "725")
KPI_LABEL_SIZE = 11   # px — tamanho do texto abaixo (ex: "Posts")
KPI_PADDING    = "8px 2px"  # padding interno de cada card de KPI

# ── Helper de ícone — definido antes do CSS para poder ser usado nele também ───
def _icon_b64(nome_arquivo):
    p = Path(f"assets/{nome_arquivo}")
    if p.exists():
        with open(p, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# Ícone customizado para o botão de colapsar/expandir a sidebar
_sidebar_toggle_b64 = _icon_b64("icon_sidebar_toggle.png")

# Ícones de navegação — pré-computados aqui para virarem background-image dos
# botões via CSS (garante alinhamento idêntico ao item ativo, sem colunas extras)
NAV_ICON_LEFT = 14   # px — distância do ícone até a borda esquerda do botão
_nav_icon_files = {
    "feed":     "icon_feed.png",
    "thread":   "icon_thread.png",
    "insights": "icon_insights.png",
}
_nav_icons_b64 = {k: _icon_b64(v) for k, v in _nav_icon_files.items()}

_nav_css = ""
for _k, _b64 in _nav_icons_b64.items():
    if _b64:
        _nav_css += (
            f".st-key-nav_{_k} button{{"
            f"background-image:url('data:image/png;base64,{_b64}')!important;"
            f"background-repeat:no-repeat!important;"
            f"background-position:{NAV_ICON_LEFT}px center!important;"
            f"background-size:{NAV_ICON_SIZE_INATIVO}px {NAV_ICON_SIZE_INATIVO}px!important;"
            f"padding-left:{NAV_ICON_LEFT + NAV_ICON_SIZE_INATIVO + 12}px!important;"
            f"text-align:left!important;}}"
        )

# ── CSS em bloco único sem f-string aninhada ───────────────────────────────────
css = ("<style>"
    "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');"
    "*{font-family:'Inter',sans-serif!important;box-sizing:border-box;}"
    "[data-testid='stSidebarNav'],[data-testid='stSidebarNavItems'],footer{display:none!important;}"
    # Oculta o menu nativo do Streamlit (⋮) — depende de fonte de ícones externa
    # que falha às vezes e quebra o layout (Settings, Print, Record screen etc.)
    "[data-testid='stMainMenu']{display:none!important;}"
    "#MainMenu{visibility:hidden!important;}"
    # Botão de REABRIR a sidebar (quando ela está colapsada/fechada)
    # ícones e usa a imagem customizada (assets/icon_sidebar_toggle.png)
    "[data-testid='collapsedControl'] span,[data-testid='collapsedControl'] p{font-size:0!important;color:transparent!important;}"
    + (
        f"[data-testid='collapsedControl']{{background-image:url('data:image/png;base64,{_sidebar_toggle_b64}')!important;"
        f"background-size:18px 18px!important;background-repeat:no-repeat!important;background-position:center!important;"
        f"background-color:{SIDEBAR}!important;border-radius:0 8px 8px 0!important;}}"
        if _sidebar_toggle_b64 else
        f"[data-testid='collapsedControl']{{background:{SIDEBAR}!important;border-radius:0 8px 8px 0!important;}}"
        f"[data-testid='collapsedControl']::after{{content:'›';color:{TEAL}!important;font-size:18px!important;font-weight:700!important;font-family:Arial,sans-serif!important;}}"
    )
    # Botão de FECHAR a sidebar (quando ela já está aberta) — testid diferente!
    # É esse que mostrava "keyboard_double_arrow" quebrado no topo da sidebar
    +"[data-testid='stSidebarCollapseButton'] span,[data-testid='stSidebarCollapseButton'] p{font-size:0!important;color:transparent!important;}"
    f"[data-testid='stSidebarCollapseButton']{{background:transparent!important;}}"
    f"[data-testid='stSidebarCollapseButton']::after{{content:'‹';color:{TEXT2}!important;font-size:18px!important;font-weight:700!important;font-family:Arial,sans-serif!important;}}"
    f"[data-testid='stSidebarCollapseButton'] button{{background:transparent!important;border:none!important;}}"
    + _nav_css
    +
    f"[data-testid='stHeader']{{background:{BG}!important;border:none!important;box-shadow:none!important;height:auto!important;min-height:42px!important;}}"
    f"[data-testid='stToolbar']{{background:transparent!important;}}"
    f"[data-testid='stToolbar'] button{{color:{TEXT}!important;}}"
    f"[data-testid='stToolbar'] svg{{fill:{TEXT}!important;}}"
    f"html,body,[data-testid='stAppViewContainer'],[data-testid='stMain']{{background:{BG}!important;}}"
    f"[data-testid='stSidebar']{{background:{SIDEBAR}!important;border-right:1px solid {BORDER}!important;}}"
    "[data-testid='stSidebar']>div:first-child{padding:0!important;}"
    f"[data-testid='stSidebar'] .stButton>button{{background:transparent!important;border:none!important;box-shadow:none!important;outline:none!important;width:100%!important;padding:{NAV_ITEM_PADDING}px 12px;border-radius:8px;font-size:{NAV_LABEL_SIZE}px;color:{TEXT2};cursor:pointer;transition:background .12s,color .12s;}}"
    f"[data-testid='stSidebar'] .stButton>button:hover{{background:{TEAL_BG};color:{TEAL};}}"
    # Botão de tema — estilo "pill" destacado (alvo via classe st-key do Streamlit)
    f".st-key-toggle_tema button{{background:{TEAL_BG}!important;color:{TEAL}!important;"
    f"border:1.5px solid {TEAL}!important;border-radius:999px!important;"
    f"font-size:14px!important;font-weight:600!important;padding:12px 18px!important;"
    f"width:100%!important;transition:background .15s,color .15s!important;}}"
    f".st-key-toggle_tema button:hover{{background:{TEAL}!important;color:#fff!important;}}"
    f"[data-testid='stMain'] .stButton>button{{background:{TEAL}!important;color:#fff!important;border:none!important;border-radius:8px!important;font-size:13px!important;font-weight:500!important;padding:8px 18px!important;}}"
    f"[data-testid='stMain'] .stButton>button:hover{{background:{TEAL_DARK}!important;}}"
    f".stTextInput>div>input,.stSelectbox>div>div{{background:{CARD}!important;color:{TEXT}!important;border-color:{BORDER}!important;border-radius:8px!important;font-size:13px!important;}}"
    f"[data-testid='stMetric']{{background:{CARD}!important;border:1px solid {BORDER}!important;border-radius:12px!important;padding:16px!important;}}"
    f"[data-testid='stMetricLabel']{{color:{TEXT2}!important;font-size:12px!important;}}"
    f"[data-testid='stMetricValue']{{color:{TEXT}!important;font-size:22px!important;font-weight:500!important;}}"
    ".block-container{padding:0!important;max-width:100%!important;}"
    "::-webkit-scrollbar{width:4px;}"
    f"::-webkit-scrollbar-thumb{{background:{BORDER};border-radius:2px;}}"
    "</style>"
)
st.markdown(css, unsafe_allow_html=True)

with st.sidebar:

    # Logo
    nome_logo = "dark_logo.png" if escuro else "logo.png"
    logo_path = Path(f"assets/{nome_logo}")
    if logo_path.exists():
        st.image(str(logo_path), width=235)
    else:
        st.markdown(f"<div style='padding:16px;border-bottom:1px solid {BORDER};'><span style='font-size:14px;font-weight:600;color:{TEXT};'>🗳️ OPINATE</span><span style='font-size:11px;color:{TEAL};margin-left:6px;'>Acadêmico</span></div>", unsafe_allow_html=True)

    st.divider()

    col_t1, col_t2 = st.columns([1, 3])
    with col_t1:
        st.markdown(f"<div style='width:32px;height:32px;border-radius:6px;background:{TEAL_BG};display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:600;color:{TEAL};'>F</div>", unsafe_allow_html=True)
    with col_t2:
        st.markdown(f"<div style='font-size:12px;font-weight:500;color:{TEXT};'>Fatec Cotia</div><div style='font-size:10px;color:{TEXT2};'>Ciência de Dados</div>", unsafe_allow_html=True)

    st.divider()

    st.markdown(
        f"<p style='text-align:center;font-size:11px;font-weight:600;color:{TEXT2};"
        f"letter-spacing:0.6px;margin-bottom:10px;'>SELECIONE TEMA</p>",
        unsafe_allow_html=True
    )
    _proximo_label = "Ativar modo claro" if escuro else "Ativar modo escuro"
    _proximo_emoji = "☀️" if escuro else "🌙"
    if st.button(f"{_proximo_emoji}  {_proximo_label}", key="toggle_tema", use_container_width=True):
        st.session_state.tema = "claro" if escuro else "escuro"
        st.rerun()

    st.divider()

    pagina = st.session_state.pagina

    NAV = [
        ("feed",     "icon_feed.png",     "🏠", "Feed",     "Debates em aberto"),
        ("thread",   "icon_thread.png",   "💬", "Thread",   "Posts e análise"),
        ("insights", "icon_insights.png", "📊", "Insights", "Gráficos e padrões"),
    ]

    for key, icone_arq, emoji_fallback, label, descricao in NAV:
        ativo = pagina == key
        icone_b64 = _nav_icons_b64.get(key)

        if ativo:
            icone_html = (f"<img src='data:image/png;base64,{icone_b64}' style='width:{NAV_ICON_SIZE_ATIVO}px;height:{NAV_ICON_SIZE_ATIVO}px;object-fit:contain;'/>"
                          if icone_b64 else f"<span style='font-size:{NAV_ICON_SIZE_ATIVO-4}px;'>{emoji_fallback}</span>")
            st.markdown(
                f"<div style='background:{TEAL};border-radius:8px;padding:{NAV_ITEM_PADDING}px {NAV_ICON_LEFT}px;"
                f"margin:2px {INSET_NAVITEM}px;display:flex;align-items:center;gap:12px;'>{icone_html}"
                f"<div><div style='font-size:{NAV_LABEL_SIZE}px;font-weight:500;color:#fff;'>{label}</div>"
                f"<div style='font-size:{NAV_DESC_SIZE}px;color:#9FE1CB;'>{descricao}</div></div></div>",
                unsafe_allow_html=True
            )
        else:
            # Sem colunas — o ícone vira background-image do próprio botão via
            # CSS (_nav_css), garantindo o mesmo alinhamento do item ativo
            btn_label = label if icone_b64 else f"{emoji_fallback}  {label}"
            if st.button(btn_label, key=f"nav_{key}", use_container_width=True):
                st.session_state.pagina = key
                st.rerun()

    st.divider()
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    _gh_b64 = _icon_b64("icon_github.png")
    _li_b64 = _icon_b64("icon_linkedin.png")
    _gh_icon = f"<img src='data:image/png;base64,{_gh_b64}' style='width:{SOCIAL_ICON_SIZE}px;height:{SOCIAL_ICON_SIZE}px;object-fit:contain;'/>" if _gh_b64 else "⌥"
    _li_icon = f"<img src='data:image/png;base64,{_li_b64}' style='width:{SOCIAL_ICON_SIZE}px;height:{SOCIAL_ICON_SIZE}px;object-fit:contain;opacity:.5;'/>" if _li_b64 else "in"

    st.markdown(
        f"<p style='font-size:{SOCIAL_TITLE_SIZE}px;font-weight:600;color:{TEXT2};text-align:center;"
        f"letter-spacing:0.8px;margin-bottom:14px;'>SAIBA MAIS</p>"
        f"<div style='display:flex;flex-direction:column;gap:10px;align-items:center;'>"
        f"<a href='https://github.com/mariacamargo-ds' target='_blank' "
        f"style='width:{SOCIAL_BTN_WIDTH}px;display:flex;align-items:center;justify-content:center;gap:8px;"
        f"font-size:{SOCIAL_FONT_SIZE}px;color:{TEXT2};text-decoration:none;padding:9px 12px;"
        f"border-radius:8px;border:1px solid {BORDER};'>{_gh_icon}&nbsp;GitHub</a>"
        f"<span style='width:{SOCIAL_BTN_WIDTH}px;display:flex;align-items:center;justify-content:center;gap:8px;"
        f"font-size:{SOCIAL_FONT_SIZE}px;color:{TEXT2};padding:9px 12px;border-radius:8px;"
        f"border:1px solid {BORDER};opacity:.5;cursor:not-allowed;'>{_li_icon}&nbsp;LinkedIn</span>"
        f"</div>",
        unsafe_allow_html=True
    )

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
    st.caption("")

from utils.data import carregar_posts, resumo_sentimentos

_df      = carregar_posts()
_dist    = resumo_sentimentos(_df) if not _df.empty else {}
_n_posts = len(_df)
_n_univs = int(_df["universidade"].nunique()) if "universidade" in _df.columns else 0
_n_temas = int(_df["tema"].nunique())         if "tema"         in _df.columns else 0
_pct_pos = _dist.get("positivo", 0)
_pct_neg = _dist.get("negativo", 0)

TITULOS = {"feed": "Debates em aberto", "thread": "Thread", "insights": "Insights"}
SUBS    = {
    "feed":     "Explore e filtre os debates acadêmicos em andamento",
    "thread":   "Posts, comentários e análise de sentimentos",
    "insights": "Distribuição de sentimentos e padrões de engajamento",
}

pagina = st.session_state.pagina

st.markdown(f"<div style='background:{SIDEBAR};border-bottom:1px solid {BORDER};padding:12px 32px 10px;margin-top:4px;'>", unsafe_allow_html=True)
hc = st.columns([3, 4, 2])
with hc[0]:
    st.markdown(f"<div style='font-size:{PAGE_TITLE_SIZE}px;font-weight:600;color:{TEXT};line-height:1.3;'>{TITULOS.get(pagina,'')}</div><div style='font-size:{PAGE_SUBTITLE_SIZE}px;color:{TEXT2};margin-top:2px;'>{SUBS.get(pagina,'')}</div>", unsafe_allow_html=True)
with hc[1]:
    if pagina == "feed":
        mc = st.columns(5)
        stats = [
            (_n_posts,      "Posts",         TEXT),
            (_n_univs,      "Universidades", TEXT),
            (_n_temas,      "Temas",         TEXT),
            (f"{_pct_pos}%","Positivo",      TEAL),
            (f"{_pct_neg}%","Negativo",      "#E24B4A"),
        ]
        for i, (val, lbl, cor) in enumerate(stats):
            with mc[i]:
                st.markdown(
                    f"<div style='background:{TEAL_BG if cor==TEAL else (BORDER+'40' if cor==TEXT else '#FBEBEB')};"
                    f"border-radius:10px;padding:{KPI_PADDING};text-align:center;'>"
                    f"<div style='font-size:{KPI_VALUE_SIZE}px;font-weight:600;color:{cor};'>{val}</div>"
                    f"<div style='font-size:{KPI_LABEL_SIZE}px;color:{TEXT2};margin-top:1px;'>{lbl}</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
with hc[2]:
    st.markdown(f"<div style='display:flex;align-items:center;gap:10px;justify-content:flex-end;padding-top:2px;'><div style='width:32px;height:32px;border-radius:50%;background:{TEAL};display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:600;color:#fff;'>MC</div><div><div style='font-size:13px;font-weight:500;color:{TEXT};'>Maria Camargo</div><div style='font-size:11px;color:{TEXT2};'>Pesquisadora</div></div></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown(f"<div style='padding:24px 36px 0;'>", unsafe_allow_html=True)

if pagina == "feed":
    st.markdown(
        f"<div style='background:{TEAL_DARK};border-radius:14px;padding:20px 24px;"
        f"margin:0 {INSET_BANNER}px 20px;'>"
        f"<div style='font-size:17px;font-weight:600;color:#fff;margin-bottom:4px;'>Bem-vinda de volta, Maria! 👋</div>"
        f"<div style='font-size:13px;color:#9FE1CB;'>Você tem <b style='color:#fff;'>{_n_posts} posts</b> "
        f"em <b style='color:#fff;'>{_n_univs} universidades</b> e <b style='color:#fff;'>{_n_temas} temas</b>.</div></div>",
        unsafe_allow_html=True
    )
    from pages.feed import render
    render(CARD, TEXT, BORDER, TEAL)

elif pagina == "thread":
    from pages.thread import render
    render(CARD, TEXT, BORDER, TEAL, TEAL_DARK, escuro)

elif pagina == "insights":
    from pages.insights import render
    render(CARD, TEXT, BORDER, TEAL, escuro)

st.markdown("</div>", unsafe_allow_html=True)

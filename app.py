#ALUMNOS: ALEJANDRO JOSE ALVARADO MENDEZ
#         VALERY MICHELLE CHICAS CHACÓN
#  
#REQUISITOS DE INSTALACIÓN:
# py -m pip install streamlit textblob deep-translator plotly pandas
# COMANDO PARA EJECUTAR:
# py -m streamlit run app.py
#

import html
import re
import time
import pandas as pd
import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator, MyMemoryTranslator
import plotly.graph_objects as go

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y ESTILOS
# ---------------------------------------------------------
st.set_page_config(
    page_title="Analizador de Sentimientos",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .stApp { background-color: #0b0e17; color: #c9d1d9; }
    #MainMenu, header, footer { visibility: hidden; }
    .navbar { display: none !important; }

    /* Hero */
    .hero-title { color:#fff; font-size: 2rem; font-weight:800; margin:4px 0; text-align: center; }
    .hero-sub { color:#8b9bb4; font-size:0.9rem; max-width:700px; margin:0 auto 10px auto; text-align: center; }

    /* Botones de categoría */
    .st-key-domain_pill, .st-key-filter_pill {
        background-color: #121826; border: 1px solid #233148; border-radius: 10px; padding: 4px;
    }
    .st-key-domain_pill .stButton > button, .st-key-filter_pill .stButton > button {
        background-color: transparent !important; border:none !important; color:#8b9bb4 !important;
        border-radius:7px !important; width: 100%;
    }
    .st-key-domain_pill .stButton > button:hover, .st-key-filter_pill .stButton > button:hover {
        background-color:#1d2847 !important; color:#fff !important;
    }
    .st-key-domain_pill button[kind="primary"], .st-key-filter_pill button[kind="primary"] {
        background-color:#3b82f6 !important; color:#fff !important; font-weight:700 !important;
    }

    /* Editor tipo código */
    .st-key-editor_card { background-color:#0d121f; border:1px solid #1e293b; border-radius:12px; padding:0; overflow:hidden; }
    .editor-header { display:flex; justify-content:space-between; align-items:center; padding:10px 16px; border-bottom:1px solid #1e293b; }
    .traffic-dots span { display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:6px; }
    .dot-red{background:#ff5f56;} .dot-yellow{background:#ffbd2e;} .dot-green{background:#27c93f;}
    .editor-filename { color:#8b9bb4; font-family: monospace; font-size:0.8rem; margin-left:8px; }
    .editor-meta { color:#4b5568; font-family: monospace; font-size:0.75rem; }

    .st-key-editor_card .stTextArea textarea {
        background-color:#0d121f !important; color:#e2e8f0 !important; border:none !important;
        border-radius:0 !important; font-family: monospace !important; font-size:0.9rem !important;
        line-height:1.6rem !important; padding-top:14px !important;
    }
    .gutter { font-family: monospace; font-size:0.8rem; color:#4b5568; line-height:1.6rem; padding-top:14px; text-align:right; padding-right:10px; user-select:none; }

    .editor-footer { display:flex; justify-content:space-between; align-items:center; padding:12px 16px; border-top:1px solid #1e293b; flex-wrap: wrap; gap: 10px; }
    .status-dot { display:inline-block; width:8px; height:8px; border-radius:50%; background:#00e699; margin-right:6px; }
    .footer-info { color:#8b9bb4; font-size:0.8rem; }
    .main-btn > button {
        background-color:#3b82f6 !important; color:#fff !important; border-radius:8px !important;
        padding:8px 20px !important; font-weight:700 !important; font-size:0.9rem !important; border:none !important; width: 100%;
    }

    /* Secciones generales */
    .section-title { color:#fff; font-size:1.15rem; font-weight:800; margin: 6px 0 12px 0; }
    .section-right { color:#6b7280; font-size:0.75rem; font-family: monospace; }

    /* Tarjetas de métricas */
    .metric-card { background-color:#121826; border:1px solid #1e293b; border-radius:10px; padding:16px; height:100%; box-sizing: border-box; }
    .metric-title { font-size:0.72rem; font-weight:700; color:#8b9bb4; text-transform:uppercase; display:flex; justify-content:space-between; }
    .metric-value { font-size:1.7rem; font-weight:800; color:#fff; margin:6px 0 4px 0; word-break: break-word; }
    .metric-sub-dot { display:inline-block; width:7px; height:7px; border-radius:50%; margin-right:6px; }
    .metric-sub { font-size:0.75rem; color:#8b9bb4; }

    .polarity-track { position:relative; height:8px; border-radius:5px; margin-top:14px; background: linear-gradient(90deg, #ff4d6d 0%, #a0aab8 50%, #00e699 100%); }
    .polarity-marker { position:absolute; top:-4px; width:0; height:0; border-left:6px solid transparent; border-right:6px solid transparent; border-top:8px solid #ffffff; }

    /* Barra de prevalencia */
    .prevalence-bar { background-color:#121826; border:1px solid #1e293b; border-radius:10px; padding:14px 18px; display:flex; justify-content:space-between; align-items:center; gap:12px; flex-wrap:wrap; }
    .prevalence-badge { background-color:#0d1b2e; color:#8b9bb4; border:1px solid #233148; border-radius:8px; padding:4px 10px; font-size:0.8rem; font-weight:700; font-family: monospace; }

    /* Tarjetas de reseña */
    .review-card { background-color:#121826; border:1px solid #1e293b; border-radius:10px; padding:16px; margin-bottom:12px; word-wrap: break-word; }
    .lang-badge { background:#1c2537; color:#8b9bb4; font-size:0.72rem; padding:2px 7px; border-radius:5px; font-weight:700; font-family:monospace; }
    .domain-txt { color:#6b7280; font-size:0.75rem; font-family:monospace; margin-left:6px; }
    .sent-badge { display:inline-flex; align-items:center; gap:5px; border-radius:12px; padding:4px 12px; font-weight:bold; font-size:0.78rem; }
    .sent-badge .dot { width:7px; height:7px; border-radius:50%; }
    .badge-pos { background:#0d382c; color:#00e699; } .badge-pos .dot{background:#00e699;}
    .badge-neg { background:#3d1720; color:#ff4d6d; } .badge-neg .dot{background:#ff4d6d;}
    .badge-neu { background:#2a2e3d; color:#a0aab8; } .badge-neu .dot{background:#a0aab8;}
    .quote-txt { font-size:1rem; font-weight:600; color:#fff; margin:8px 0 4px 0; line-height: 1.4rem; }
    .trans-txt { font-size:0.82rem; color:#6b7280; font-style:italic; margin-bottom:8px; }
    .hl-pos { background-color:#0d382c; color:#8effcf; padding:1px 4px; border-radius:4px; }
    .hl-neg { background-color:#3d1720; color:#ff9fb1; padding:1px 4px; border-radius:4px; }
    .tag-emotion { background-color:#1c2537; color:#8b9bb4; padding:3px 9px; border-radius:6px; font-size:0.74rem; margin-right:5px; display:inline-block; margin-bottom:4px; }

    /* Distribución y Emociones */
    .side-card { background-color:#121826; border:1px solid #1e293b; border-radius:10px; padding:16px; }
    .emo-chip { display:inline-flex; align-items:center; gap:6px; background-color:#1c2537; color:#c9d1d9; padding:5px 11px; border-radius:14px; font-size:0.78rem; margin:3px 5px 3px 0; }
    .emo-count { background:#0b0e17; color:#8b9bb4; font-size:0.68rem; padding:1px 6px; border-radius:8px; }

    /* Reglas Responsivas Limpias para Móvil */
    @media (max-width: 768px) {
        .hero-title { font-size: 1.5rem; }
        .hero-sub { font-size: 0.85rem; }
        .gutter { display: none !important; }
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ESTADO DE SESIÓN
# ---------------------------------------------------------
if "domain_filter" not in st.session_state:
    st.session_state.domain_filter = "General"
if "results" not in st.session_state:
    st.session_state.results = None
if "filter" not in st.session_state:
    st.session_state.filter = "Todos"
if "comment_input" not in st.session_state:
    st.session_state.comment_input = (
        "La comida llegó súper fría y el servicio fue pésimo, tardaron más de una hora.\n"
        "El paquete llegó en excelente estado, súper rápido y la atención fue maravillosa.\n"
        "El producto cumple con la descripción estándar, sin sorpresas ni novedades.\n"
        "The dashboard UI is intuitive, but the API latency is driving my team crazy.\n"
        "¡Increíble soporte técnico! Resolvieron el problema del webhook en 5 minutos."
    )

# ---------------------------------------------------------
# FUNCIONES TÉCNICAS
# ---------------------------------------------------------
def esc(text):
    return html.escape(str(text), quote=True)

def translate_to_english(text, retries=1, delay=0.3):
    for _ in range(retries):
        try:
            translated = GoogleTranslator(source='es', target='en').translate(text)
            if translated:
                return translated, True
        except Exception:
            time.sleep(delay)
    try:
        translated = MyMemoryTranslator(source='es-ES', target='en-GB').translate(text)
        if translated:
            return translated, True
    except Exception:
        pass
    return text, False

def get_emotions(text, polarity):
    t = text.lower()
    if polarity > 0.05:
        if any(w in t for w in ["excelente", "love", "encantó", "increíble", "maravillosa"]):
            return ["Gratitud", "Satisfacción", "Entusiasmo"]
        return ["Admiración", "Alegría"]
    elif polarity < -0.05:
        if any(w in t for w in ["horrible", "roto", "terrible", "pésimo", "fría"]):
            return ["Frustración", "Decepción", "Enojo"]
        return ["Insatisfacción", "Reclamo"]
    return ["Indiferencia", "Calma"]

DOMAIN_KEYWORDS = {
    "Gastro": ["comida", "restaurante", "platillo", "mesero", "menú", "mesa", "cocina", "sabor", "plato"],
    "Logística": ["paquete", "envío", "entrega", "transportista", "pedido", "llegó", "repartidor"],
    "Retail": ["producto", "precio", "descripción", "tienda", "compra", "talla", "artículo"],
    "SaaS": ["api", "dashboard", "latencia", "ui", "software", "aplicación", "sistema", "app"],
    "DevOps": ["soporte técnico", "webhook", "servidor", "bug", "deploy", "infraestructura", "incidente"],
}

def classify_domain(original, translated):
    blob = f"{original} {translated}".lower()
    for domain, keywords in DOMAIN_KEYWORDS.items():
        if any(k in blob for k in keywords):
            return domain
    return "General"

POS_PHRASES = ["excelente estado", "excelente", "maravillosa", "maravilloso", "increíble", "súper rápido",
               "perfecto", "perfecta", "encantó", "genial", "fantástico", "resolvieron", "intuitive"]
NEG_PHRASES = ["súper fría", "pésimo", "horrible", "terrible", "tardaron más de una hora", "roto",
               "driving my team crazy", "mala calidad", "lenta", "fría"]

_POS_SET = {p.lower() for p in POS_PHRASES}
_ALL_PHRASES = sorted(POS_PHRASES + NEG_PHRASES, key=len, reverse=True)
_HIGHLIGHT_RE = re.compile("|".join(re.escape(p) for p in _ALL_PHRASES), re.IGNORECASE)

def highlight_quote(text):
    escaped = esc(text)
    def repl(m):
        matched = m.group(0)
        cls = "hl-pos" if matched.lower() in _POS_SET else "hl-neg"
        return f'<span class="{cls}">{matched}</span>'
    return _HIGHLIGHT_RE.sub(repl, escaped)

# ---------------------------------------------------------
# HERO Y CARGA DE ARCHIVOS
# ---------------------------------------------------------
st.markdown('''
<div style="text-align:center; margin: 15px 0 15px 0;">
    <div class="hero-title">Analizador de Sentimientos</div>
    <div class="hero-sub">Analiza los sentimientos en tiempo real con detección de emociones y polaridad.</div>
</div>
''', unsafe_allow_html=True)

uploaded_file = st.file_uploader("📁 Opcional: Carga un archivo de texto o CSV con comentarios", type=["txt", "csv"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.txt'):
            file_contents = uploaded_file.getvalue().decode("utf-8")
        elif uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
            first_col = df.columns[0]
            file_contents = "\n".join(df[first_col].dropna().astype(str).tolist())
        st.session_state.comment_input = file_contents
        st.success(f"Archivo '{uploaded_file.name}' cargado con éxito.")
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")

# ---------------------------------------------------------
# CATEGORÍAS
# ---------------------------------------------------------
DOMAINS = ["General", "Restaurante", "Tienda"]
lbl_col, tabs_col = st.columns([1, 2])
with lbl_col:
    st.markdown("<div style='padding-top:6px; color:#8b9bb4; font-size:0.85rem; font-weight:700;'>LOTE DE EVALUACIÓN</div>", unsafe_allow_html=True)
with tabs_col:
    with st.container(key="domain_pill"):
        dcols = st.columns(len(DOMAINS))
        for col, dom in zip(dcols, DOMAINS):
            with col:
                is_active = st.session_state.domain_filter == dom
                if st.button(dom, key=f"dom_{dom}", type="primary" if is_active else "secondary"):
                    st.session_state.domain_filter = dom
                    st.rerun()

# ---------------------------------------------------------
# EDITOR DE CÓDIGO
# ---------------------------------------------------------
with st.container(key="editor_card"):
    st.markdown('''
    <div class="editor-header">
        <div><span class="traffic-dots"><span class="dot-red"></span><span class="dot-yellow"></span><span class="dot-green"></span></span>
            <span class="editor-filename">Escriba lo que desea que se analice </span></div>
        <span class="editor-meta">UTF-8</span>
    </div>
    ''', unsafe_allow_html=True)

    gcol, tcol = st.columns([0.08, 0.92])
    lines_now = st.session_state.comment_input.split("\n")
    with gcol:
        nums = "".join(f"<div>{i:02d}</div>" for i in range(1, max(len(lines_now), 8) + 1))
        st.markdown(f"<div class='gutter'>{nums}</div>", unsafe_allow_html=True)
    with tcol:
        user_input = st.text_area("Comentarios", key="comment_input", height=180, label_visibility="collapsed")

    num_lines = len([l for l in user_input.split("\n") if l.strip()])
    f_left, f_right = st.columns([2, 1])
    with f_left:
        st.markdown(
            f"<div class='footer-info' style='padding-top:8px;'><span class='status-dot'></span>"
            f"{num_lines} líneas detectadas · {len(user_input)} caracteres</div>",
            unsafe_allow_html=True
        )
    with f_right:
        st.markdown('<div class="main-btn" style="text-align:right;">', unsafe_allow_html=True)
        btn_analizar = st.button("✨ Analizar Sentimientos", key="main_action")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# EJECUCIÓN DEL ANÁLISIS
# ---------------------------------------------------------
if btn_analizar:
    lines = [line.strip() for line in user_input.split("\n") if line.strip()]
    if not lines:
        st.warning("Escribe al menos un comentario para analizar.")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        start_time = time.time()

        counts = {"Positivo": 0, "Negativo": 0, "Neutral": 0}
        emotion_counts = {}
        total_polarity = 0
        results = []
        total = len(lines)

        for i, text in enumerate(lines, start=1):
            status_text.markdown(f"<span style='color:#8b9bb4; font-size:0.85rem;'>Procesando línea {i} de {total}...</span>", unsafe_allow_html=True)
            translated_text, is_trans = translate_to_english(text)
            
            blob = TextBlob(translated_text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            total_polarity += polarity

            if polarity > 0.05:
                sentiment, badge_class = "POSITIVO", "badge-pos"
                counts["Positivo"] += 1
            elif polarity < -0.05:
                sentiment, badge_class = "NEGATIVO", "badge-neg"
                counts["Negativo"] += 1
            else:
                sentiment, badge_class = "NEUTRAL", "badge-neu"
                counts["Neutral"] += 1

            emotions = get_emotions(text, polarity)
            for e in emotions:
                emotion_counts[e] = emotion_counts.get(e, 0) + 1

            lang = "ES" if is_trans and text != translated_text else "EN"
            domain = classify_domain(text, translated_text)

            results.append({
                "original": text,
                "translated": translated_text if is_trans and text != translated_text else None,
                "polarity": polarity, "subjectivity": subjectivity,
                "sentiment": sentiment, "badge_class": badge_class,
                "lang": lang, "domain": domain, "emotions": emotions,
            })
            progress_bar.progress(i / total)

        elapsed_ms = int((time.time() - start_time) * 1000)
        progress_bar.empty()
        status_text.empty()

        st.session_state.results = {
            "items": results, "counts": counts, "emotion_counts": emotion_counts,
            "avg_polarity": total_polarity / total, "total": total, "elapsed_ms": elapsed_ms,
        }
        st.session_state.filter = "Todos"

# ---------------------------------------------------------
# DESPLIEGUE DE RESULTADOS
# ---------------------------------------------------------
data = st.session_state.results
if data:
    items = data["items"]
    counts = data["counts"]
    total_rev = data["total"]
    avg_polarity = data["avg_polarity"]

    pos_pct = counts["Positivo"] / total_rev * 100
    neg_pct = counts["Negativo"] / total_rev * 100
    neu_pct = counts["Neutral"] / total_rev * 100

    def sub_label(pct, kind):
        if kind == "pos":
            return ("Alta satisfacción", "#00e699") if pct >= 40 else ("Satisfacción moderada", "#00e699")
        if kind == "neg":
            return ("Atención requerida", "#ff4d6d") if pct >= 40 else ("Revisar casos", "#ff4d6d")
        return ("Informativo", "#a0aab8")

    pos_sub, pos_c = sub_label(pos_pct, "pos")
    neg_sub, neg_c = sub_label(neg_pct, "neg")
    neu_sub, neu_c = sub_label(neu_pct, "neu")

    st.markdown("<br>", unsafe_allow_html=True)
    r_l, r_r = st.columns([2, 1])
    with r_l:
        st.markdown('<div class="section-title">📊 Resumen de Inferencia</div>', unsafe_allow_html=True)
    with r_r:
        st.markdown(f"<div class='section-right' style='text-align:right; padding-top:6px;'>Latencia: {data['elapsed_ms']}ms</div>", unsafe_allow_html=True)

    m1, m2 = st.columns(2)
    with m1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-title">POSITIVOS <span>🙂</span></div>
            <div class="metric-value">{counts["Positivo"]} <span style="font-size:0.85rem; color:#8b9bb4;">({pos_pct:.0f}%)</span></div>
            <div class="metric-sub"><span class="metric-sub-dot" style="background:{pos_c};"></span>{pos_sub}</div>
        </div>
        ''', unsafe_allow_html=True)
    with m2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-title">NEGATIVOS <span>🙁</span></div>
            <div class="metric-value">{counts["Negativo"]} <span style="font-size:0.85rem; color:#8b9bb4;">({neg_pct:.0f}%)</span></div>
            <div class="metric-sub"><span class="metric-sub-dot" style="background:{neg_c};"></span>{neg_sub}</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    m3, m4 = st.columns(2)
    with m3:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-title">NEUTROS <span>😐</span></div>
            <div class="metric-value">{counts["Neutral"]} <span style="font-size:0.85rem; color:#8b9bb4;">({neu_pct:.0f}%)</span></div>
            <div class="metric-sub"><span class="metric-sub-dot" style="background:{neu_c};"></span>{neu_sub}</div>
        </div>
        ''', unsafe_allow_html=True)
    with m4:
        marker_pct = max(0, min(100, (avg_polarity + 1) / 2 * 100))
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-title">POLARIDAD AVG <span>📈</span></div>
            <div class="metric-value">{avg_polarity:+.2f}</div>
            <div class="polarity-track"><div class="polarity-marker" style="left:calc({marker_pct}% - 6px);"></div></div>
        </div>
        ''', unsafe_allow_html=True)

    # Prevalencia
    leader_key = max(counts, key=counts.get)
    leader_pct = counts[leader_key] / total_rev * 100
    label = leader_key
    desc = f"⚖️ {leader_key} predomina con {counts[leader_key]}/{total_rev} comentarios ({leader_pct:.0f}%)."
    delta = abs(pos_pct - neg_pct) / 100

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    st.markdown(f'''
    <div class="prevalence-bar">
        <div>⚖️ <b style="color:#fff;">Sentimiento Prevalente: {esc(label)}</b><br>
        <span style="color:#8b9bb4; font-size:0.8rem;">{esc(desc)}</span></div>
        <div class="prevalence-badge">±{delta:.2f}</div>
    </div>
    ''', unsafe_allow_html=True)

    # ---- Análisis detallado ----
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 Análisis Detallado</div>', unsafe_allow_html=True)

    with st.container(key="filter_pill"):
        f1, f2, f3, f4 = st.columns(4)
        filtros = [
            ("Todos", f"Todos ({total_rev})", f1),
            ("Positivo", f"Pos. ({counts['Positivo']})", f2),
            ("Negativo", f"Neg. ({counts['Negativo']})", f3),
            ("Neutral", f"Neu. ({counts['Neutral']})", f4),
        ]
        for key, lbl, col in filtros:
            with col:
                is_active = st.session_state.filter == key
                if st.button(lbl, key=f"filter_{key}", type="primary" if is_active else "secondary"):
                    st.session_state.filter = key
                    st.rerun()

    active_filter = st.session_state.filter
    filtered = items if active_filter == "Todos" else [r for r in items if r["sentiment"].lower().startswith(active_filter.lower())]

    # COMPONENTE RENDERIZADO LIMPIO DE TARJETAS
    for idx, item in enumerate(filtered, start=1):
        emotions_html = "".join([f'<span class="tag-emotion">{esc(e)}</span>' for e in item["emotions"]])
        trans_html = f'<div class="trans-txt">"{esc(item["translated"])}"</div>' if item["translated"] else ""
        
        st.markdown(f'''
        <div class="review-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <div><span class="lang-badge">{item["lang"]}</span><span class="domain-txt">· {esc(item["domain"])}</span></div>
                <span class="sent-badge {item["badge_class"]}"><span class="dot"></span>{item["sentiment"]}</span>
            </div>
            <div class="quote-txt">"{highlight_quote(item["original"])}"</div>
            {trans_html}
            <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.8rem; margin-top:10px; flex-wrap:wrap; gap:8px;">
                <div>{emotions_html}</div>
                <div style="color:#8b9bb4; display:flex; gap:12px;">
                    <span>Polaridad: <b style="color:#fff;">{item["polarity"]:+.2f}</b></span>
                    <span>Subjetividad: <b style="color:#fff;">{item["subjectivity"]:.2f}</b></span>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    if not filtered:
        st.info("No hay comentarios en esta categoría.")

    # ---- Distribución y emociones ----
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">🌐 Distribución y Emociones</div>', unsafe_allow_html=True)

    dist_l, dist_r = st.columns([1, 1])
    with dist_l:
        fig = go.Figure(data=[go.Pie(
            labels=list(counts.keys()), values=list(counts.values()), hole=.68,
            marker_colors=['#00e699', '#ff4d6d', '#a0aab8'], textinfo='none', showlegend=False,
        )])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=10, b=10, l=10, r=10), height=200,
            annotations=[dict(text=f"<b style='font-size:20px;color:#fff;'>{total_rev}</b><br><span style='font-size:10px;color:#6b7280;'>LOTE</span>",
                               showarrow=False, font=dict(color="#fff"))]
        )
        st.plotly_chart(fig, use_container_width=True)

    with dist_r:
        emo_html = "".join(
            f'<span class="emo-chip">{esc(e)} <span class="emo-count">x{c}</span></span>'
            for e, c in sorted(data["emotion_counts"].items(), key=lambda x: -x[1])
        )
        st.markdown(f'''
        <div class="side-card">
            <div style="color:#8b9bb4; font-size:0.75rem; font-weight:700; margin-bottom:8px;">VECTORES DE EMOCIONES DETECTADAS</div>
            <div>{emo_html}</div>
        </div>
        ''', unsafe_allow_html=True)

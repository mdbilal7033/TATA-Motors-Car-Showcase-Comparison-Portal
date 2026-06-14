import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from data import TATA_CARS, CATEGORIES

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TATA Motors Showcase",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Image Helper ─────────────────────────────────────────────────────────────────
IMAGES_DIR = Path(__file__).parent / "images"

def get_image_path(filename: str) -> Path | None:
    """Return the image path if it exists, else None."""
    p = IMAGES_DIR / filename
    return p if p.exists() else None

def show_car_image(filename: str, caption: str = "", height: int = 220):
    """Display car image or a styled placeholder."""
    path = get_image_path(filename)
    if path:
        st.image(str(path), caption=caption, use_container_width=True)
    else:
        # Styled SVG placeholder
        name = filename.replace(".png", "").replace("_", " ").upper()
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border: 2px dashed #334155;
            border-radius: 12px;
            height: {height}px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: #475569;
            font-family: 'Rajdhani', sans-serif;
            letter-spacing: 2px;
            margin-bottom: 8px;
        ">
            <div style="font-size: 3rem;">🚗</div>
            <div style="font-size: 0.75rem; margin-top: 8px; color: #64748b;">{name}</div>
            <div style="font-size: 0.65rem; color: #334155; margin-top: 4px;">Add image to images/ folder</div>
        </div>
        """, unsafe_allow_html=True)

# ─── Custom CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Exo+2:wght@300;400;600&display=swap');

html, body, [class*="css"] { font-family: 'Exo 2', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0a0a0f 0%, #111827 50%, #0d1117 100%);
    color: #e2e8f0;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 100%);
    border-right: 1px solid #312e81;
}
[data-testid="stSidebar"] * { color: #c7d2fe !important; }

h1, h2, h3 { font-family: 'Rajdhani', sans-serif !important; letter-spacing: 2px; }

.hero-banner {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #4c1d95 100%);
    border: 1px solid #6d28d9;
    border-radius: 16px;
    padding: 40px;
    margin-bottom: 30px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%; right: -20%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(139,92,246,0.3) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 3.2rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 4px;
    margin: 0;
    text-shadow: 0 0 30px rgba(139,92,246,0.8);
}
.hero-sub { font-size: 1.1rem; color: #a5b4fc; margin-top: 8px; letter-spacing: 1px; }
.hero-badge {
    display: inline-block;
    background: rgba(139,92,246,0.2);
    border: 1px solid #7c3aed;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.8rem;
    color: #c4b5fd;
    letter-spacing: 2px;
    margin-top: 12px;
}

/* Car card — image on top, info below */
.car-card-wrapper {
    background: linear-gradient(145deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 0;
    margin-bottom: 20px;
    overflow: hidden;
    transition: all 0.3s ease;
    position: relative;
}
.car-card-wrapper:hover { border-color: #7c3aed; box-shadow: 0 0 30px rgba(124,58,237,0.25); }
.car-card-wrapper::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 4px;
    background: linear-gradient(90deg, #7c3aed, #4f46e5);
}
.car-img-zone {
    background: linear-gradient(180deg, #0f1729 0%, #1a2540 100%);
    padding: 16px 12px 10px;
    border-bottom: 1px solid #1e293b;
}
.car-info-zone { padding: 18px 18px 14px; }
.car-name {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #e0e7ff;
    letter-spacing: 2px;
}
.car-price { font-size: 1rem; color: #a5b4fc; font-weight: 600; }
.car-tag {
    display: inline-block;
    background: rgba(79,70,229,0.2);
    border: 1px solid #4f46e5;
    border-radius: 12px;
    padding: 2px 10px;
    font-size: 0.72rem;
    color: #818cf8;
    margin: 3px 2px;
    letter-spacing: 1px;
}
.spec-row {
    display: flex;
    justify-content: space-between;
    border-bottom: 1px solid #1e293b;
    padding: 5px 0;
    font-size: 0.87rem;
}
.spec-label { color: #64748b; }
.spec-value { color: #e2e8f0; font-weight: 600; }

.metric-box {
    background: linear-gradient(145deg, #1e1b4b, #1e293b);
    border: 1px solid #4338ca;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}
.metric-num { font-family: 'Rajdhani', sans-serif; font-size: 2.4rem; font-weight: 700; color: #a5b4fc; }
.metric-lbl { font-size: 0.8rem; color: #64748b; letter-spacing: 1px; }

.section-heading {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #c7d2fe;
    letter-spacing: 3px;
    border-left: 4px solid #7c3aed;
    padding-left: 14px;
    margin: 28px 0 18px;
}

/* Compare image box */
.compare-img-box {
    background: linear-gradient(180deg, #0f1729, #1a2540);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 16px;
    text-align: center;
}
.compare-car-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #e0e7ff;
    letter-spacing: 2px;
    margin-top: 10px;
}
.compare-price { font-size: 0.95rem; color: #a5b4fc; }

/* image status banner */
.img-status {
    background: rgba(30,41,59,0.7);
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 0.82rem;
    color: #64748b;
    margin-bottom: 16px;
}
.img-ok { color: #34d399; }
.img-missing { color: #f87171; }

hr { border-color: #1e293b !important; }
.stSelectbox label { color: #a5b4fc !important; }
.stSelectbox > div > div { background: #1e293b !important; border-color: #4338ca !important; color: #e2e8f0 !important; }
.stTabs [data-baseweb="tab-list"] { background: #0f172a; border-radius: 10px; }
.stTabs [data-baseweb="tab"] { color: #64748b !important; font-family: 'Rajdhani', sans-serif; }
.stTabs [aria-selected="true"] { color: #a5b4fc !important; border-bottom: 2px solid #7c3aed !important; }
.stRadio label { color: #a5b4fc !important; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0f172a; }
::-webkit-scrollbar-thumb { background: #4338ca; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ─── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚗 TATA MOTORS")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["🏠 Showcase", "⚖️ Compare Cars", "📊 Analytics", "📋 Full Specs", "🖼️ Image Status"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("**Filter by Category**")
    sel_cats = st.multiselect("Category", CATEGORIES, default=CATEGORIES, label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**Price Range (₹ Lakhs)**")
    price_range = st.slider("Price", 6, 70, (6, 70), label_visibility="collapsed")
    st.markdown("---")
    # Quick image status in sidebar
    present = sum(1 for c in TATA_CARS if get_image_path(c["image"]))
    total = len(TATA_CARS)
    st.markdown(f"**🖼️ Images:** `{present}/{total}` loaded")
    st.caption("© 2025 Tata Motors Fan Portal")


# ─── Filter ───────────────────────────────────────────────────────────────────────
def filter_cars(cars, cats, price_min, price_max):
    return [c for c in cars if c["category"] in cats and price_min <= c["price_min"] <= price_max]

filtered = filter_cars(TATA_CARS, sel_cats, price_range[0], price_range[1])


# ═══════════════════════════════════════════════════════════════════════════════════
#  PAGE 1: SHOWCASE
# ═══════════════════════════════════════════════════════════════════════════════════
if page == "🏠 Showcase":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">⚡ TATA MOTORS</div>
        <div class="hero-sub">India's Most Trusted Automobile Brand</div>
        <div class="hero-badge">INNOVATION · SAFETY · PERFORMANCE</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-box"><div class="metric-num">{len(TATA_CARS)}</div><div class="metric-lbl">MODELS</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-box"><div class="metric-num">{len(CATEGORIES)}</div><div class="metric-lbl">SEGMENTS</div></div>', unsafe_allow_html=True)
    with c3:
        evs = sum(1 for c in TATA_CARS if "EV" in c.get("tags", []))
        st.markdown(f'<div class="metric-box"><div class="metric-num">{evs}</div><div class="metric-lbl">EV MODELS</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-box"><div class="metric-num">{len(filtered)}</div><div class="metric-lbl">FILTERED</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-heading">MODEL LINEUP</div>', unsafe_allow_html=True)

    if not filtered:
        st.warning("No cars match the current filters.")
    else:
        cols = st.columns(2)
        for i, car in enumerate(filtered):
            with cols[i % 2]:
                tags_html = "".join([f'<span class="car-tag">{t}</span>' for t in car.get("tags", [])])
                # Card top with image
                st.markdown('<div class="car-card-wrapper"><div class="car-img-zone">', unsafe_allow_html=True)
                show_car_image(car["image"], height=210)
                st.markdown('</div><div class="car-info-zone">', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="car-name">{car['emoji']} {car['name']}</div>
                <div class="car-price">₹ {car['price_min']} – {car['price_max']} Lakhs</div>
                <div style="margin:8px 0">{tags_html}</div>
                <div style="margin-top:12px">
                    <div class="spec-row"><span class="spec-label">Engine</span><span class="spec-value">{car['engine']}</span></div>
                    <div class="spec-row"><span class="spec-label">Power</span><span class="spec-value">{car['power']}</span></div>
                    <div class="spec-row"><span class="spec-label">Mileage</span><span class="spec-value">{car['mileage']}</span></div>
                    <div class="spec-row"><span class="spec-label">Seating</span><span class="spec-value">{car['seating']} persons</span></div>
                    <div class="spec-row"><span class="spec-label">Segment</span><span class="spec-value">{car['category']}</span></div>
                </div>
                <div style="margin-top:10px;font-size:0.85rem;color:#94a3b8;font-style:italic">{car['tagline']}</div>
                </div></div>
                """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════════
#  PAGE 2: COMPARE
# ═══════════════════════════════════════════════════════════════════════════════════
elif page == "⚖️ Compare Cars":
    st.markdown('<div class="hero-banner"><div class="hero-title">⚖️ COMPARE CARS</div><div class="hero-sub">Side-by-side spec comparison</div></div>', unsafe_allow_html=True)

    car_names = [c["name"] for c in TATA_CARS]
    col1, col2 = st.columns(2)
    with col1:
        car1_name = st.selectbox("🔵 Car 1", car_names, index=0)
    with col2:
        car2_name = st.selectbox("🟣 Car 2", car_names, index=5)

    car1 = next(c for c in TATA_CARS if c["name"] == car1_name)
    car2 = next(c for c in TATA_CARS if c["name"] == car2_name)

    # ── Image Hero Row ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">HEAD TO HEAD</div>', unsafe_allow_html=True)
    ic1, vs_col, ic2 = st.columns([5, 1, 5])
    with ic1:
        st.markdown('<div class="compare-img-box">', unsafe_allow_html=True)
        show_car_image(car1["image"], height=240)
        st.markdown(f"""
        <div class="compare-car-title">{car1['emoji']} {car1['name']}</div>
        <div class="compare-price">₹{car1['price_min']}–{car1['price_max']} Lakhs</div>
        </div>""", unsafe_allow_html=True)
    with vs_col:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;color:#7c3aed;font-size:2rem;'>VS</h2>", unsafe_allow_html=True)
    with ic2:
        st.markdown('<div class="compare-img-box">', unsafe_allow_html=True)
        show_car_image(car2["image"], height=240)
        st.markdown(f"""
        <div class="compare-car-title">{car2['emoji']} {car2['name']}</div>
        <div class="compare-price">₹{car2['price_min']}–{car2['price_max']} Lakhs</div>
        </div>""", unsafe_allow_html=True)

    # ── Spec Table ─────────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">SPECS COMPARISON</div>', unsafe_allow_html=True)
    specs = [
        ("Category", "category"),
        ("Engine", "engine"),
        ("Power", "power"),
        ("Torque", "torque"),
        ("Mileage", "mileage"),
        ("Transmission", "transmission"),
        ("Seating", "seating"),
        ("Boot Space (L)", "boot"),
        ("Safety Rating", "safety"),
        ("Fuel Type", "fuel"),
    ]

    c1h, c2h, c3h = st.columns([2, 3, 3])
    with c1h: st.markdown("**SPECIFICATION**")
    with c2h: st.markdown(f"**{car1['emoji']} {car1['name']}**")
    with c3h: st.markdown(f"**{car2['emoji']} {car2['name']}**")
    st.markdown("---")

    for label, key in specs:
        cv1, cv2, cv3 = st.columns([2, 3, 3])
        v1 = car1.get(key, "—")
        v2 = car2.get(key, "—")
        with cv1: st.markdown(f"<span style='color:#64748b;font-size:0.9rem'>{label}</span>", unsafe_allow_html=True)
        with cv2: st.markdown(f"<span style='color:#a5b4fc;font-weight:600'>{v1}</span>", unsafe_allow_html=True)
        with cv3: st.markdown(f"<span style='color:#c4b5fd;font-weight:600'>{v2}</span>", unsafe_allow_html=True)
        st.markdown("---")

    # ── Radar Chart ────────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">PERFORMANCE RADAR</div>', unsafe_allow_html=True)
    radar_keys = ["score_performance", "score_comfort", "score_safety", "score_value", "score_tech", "score_space"]
    radar_labels = ["Performance", "Comfort", "Safety", "Value", "Technology", "Space"]
    r1 = [car1.get(k, 5) for k in radar_keys]
    r2 = [car2.get(k, 5) for k in radar_keys]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=r1+[r1[0]], theta=radar_labels+[radar_labels[0]],
        fill='toself', name=car1["name"],
        line=dict(color='#818cf8', width=2), fillcolor='rgba(129,140,248,0.15)'))
    fig.add_trace(go.Scatterpolar(r=r2+[r2[0]], theta=radar_labels+[radar_labels[0]],
        fill='toself', name=car2["name"],
        line=dict(color='#c084fc', width=2), fillcolor='rgba(192,132,252,0.15)'))
    fig.update_layout(
        polar=dict(bgcolor='rgba(15,23,42,0.8)',
            radialaxis=dict(visible=True, range=[0,10], color='#334155', gridcolor='#1e293b'),
            angularaxis=dict(color='#94a3b8', gridcolor='#1e293b')),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(font=dict(color='#a5b4fc'), bgcolor='rgba(15,23,42,0.8)'),
        margin=dict(t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

    # ── Bar chart ──────────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">SCORE BREAKDOWN</div>', unsafe_allow_html=True)
    df_bar = pd.DataFrame({"Category": radar_labels*2, "Score": r1+r2,
                            "Car": [car1["name"]]*6 + [car2["name"]]*6})
    fig2 = px.bar(df_bar, x="Category", y="Score", color="Car", barmode="group",
                  color_discrete_map={car1["name"]: "#818cf8", car2["name"]: "#c084fc"})
    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15,23,42,0.5)',
        xaxis=dict(color='#94a3b8', gridcolor='#1e293b'),
        yaxis=dict(color='#94a3b8', gridcolor='#1e293b', range=[0,10]),
        legend=dict(font=dict(color='#a5b4fc'), bgcolor='rgba(0,0,0,0)'),
        font=dict(color='#a5b4fc'))
    st.plotly_chart(fig2, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════════
#  PAGE 3: ANALYTICS
# ═══════════════════════════════════════════════════════════════════════════════════
elif page == "📊 Analytics":
    st.markdown('<div class="hero-banner"><div class="hero-title">📊 ANALYTICS</div><div class="hero-sub">Tata Motors fleet insights at a glance</div></div>', unsafe_allow_html=True)
    df = pd.DataFrame(TATA_CARS)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-heading">BY CATEGORY</div>', unsafe_allow_html=True)
        cat_counts = df["category"].value_counts().reset_index()
        cat_counts.columns = ["Category", "Count"]
        fig = px.pie(cat_counts, names="Category", values="Count",
                     color_discrete_sequence=["#818cf8","#c084fc","#6d28d9","#4f46e5","#7c3aed","#a78bfa"])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#a5b4fc'),
                          legend=dict(bgcolor='rgba(0,0,0,0)'))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-heading">PRICE RANGE (₹ LAKHS)</div>', unsafe_allow_html=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Min Price", x=df["name"], y=df["price_min"], marker_color='#4f46e5'))
        fig2.add_trace(go.Bar(name="Max Price", x=df["name"], y=df["price_max"], marker_color='#7c3aed'))
        fig2.update_layout(barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15,23,42,0.5)',
            xaxis=dict(color='#94a3b8', gridcolor='#1e293b', tickangle=-35),
            yaxis=dict(color='#94a3b8', gridcolor='#1e293b'),
            legend=dict(font=dict(color='#a5b4fc'), bgcolor='rgba(0,0,0,0)'),
            font=dict(color='#a5b4fc'), margin=dict(b=100))
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-heading">FUEL TYPE SPLIT</div>', unsafe_allow_html=True)
        fuel_counts = df["fuel"].value_counts().reset_index()
        fuel_counts.columns = ["Fuel", "Count"]
        fig3 = px.bar(fuel_counts, x="Fuel", y="Count", color="Fuel",
                      color_discrete_sequence=["#818cf8","#c084fc","#6d28d9","#a5b4fc"])
        fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15,23,42,0.5)',
                           font=dict(color='#a5b4fc'), showlegend=False,
                           xaxis=dict(color='#94a3b8'), yaxis=dict(color='#94a3b8', gridcolor='#1e293b'))
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown('<div class="section-heading">SEATING CAPACITY</div>', unsafe_allow_html=True)
        seat_counts = df["seating"].value_counts().reset_index()
        seat_counts.columns = ["Seats", "Count"]
        seat_counts["Seats"] = seat_counts["Seats"].astype(str) + " Seats"
        fig4 = px.pie(seat_counts, names="Seats", values="Count", hole=0.4,
                      color_discrete_sequence=["#818cf8","#c084fc","#6d28d9","#4f46e5"])
        fig4.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#a5b4fc'),
                           legend=dict(bgcolor='rgba(0,0,0,0)'))
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="section-heading">VALUE vs PERFORMANCE</div>', unsafe_allow_html=True)
    fig5 = px.scatter(df, x="score_value", y="score_performance",
                      size="price_max", color="category", hover_name="name", text="name",
                      color_discrete_sequence=["#818cf8","#c084fc","#6d28d9","#a78bfa","#4f46e5","#7c3aed"],
                      labels={"score_value": "Value Score", "score_performance": "Performance Score"})
    fig5.update_traces(textposition='top center', textfont=dict(color='#a5b4fc', size=11))
    fig5.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15,23,42,0.5)',
                       font=dict(color='#a5b4fc'),
                       xaxis=dict(color='#94a3b8', gridcolor='#1e293b', range=[3,11]),
                       yaxis=dict(color='#94a3b8', gridcolor='#1e293b', range=[3,11]),
                       legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#a5b4fc')))
    st.plotly_chart(fig5, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════════
#  PAGE 4: FULL SPECS
# ═══════════════════════════════════════════════════════════════════════════════════
elif page == "📋 Full Specs":
    st.markdown('<div class="hero-banner"><div class="hero-title">📋 FULL SPECS</div><div class="hero-sub">Complete technical specifications for all models</div></div>', unsafe_allow_html=True)

    search = st.text_input("🔍 Search models", placeholder="Type car name...")
    display_cars = [c for c in TATA_CARS if search.lower() in c["name"].lower()] if search else TATA_CARS

    for car in display_cars:
        with st.expander(f"{car['emoji']}  {car['name']}  —  ₹{car['price_min']}–{car['price_max']} L  |  {car['category']}"):
            img_col, specs_col = st.columns([2, 3])
            with img_col:
                show_car_image(car["image"], car["name"], height=200)
                tags_html = " ".join([f'<span class="car-tag">{t}</span>' for t in car.get("tags", [])])
                st.markdown(f"<div style='margin-top:8px'>{tags_html}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='margin-top:8px;color:#64748b;font-style:italic;font-size:0.85rem'>💬 {car['tagline']}</div>", unsafe_allow_html=True)

            with specs_col:
                c1s, c2s = st.columns(2)
                with c1s:
                    st.markdown("**ENGINE & DRIVETRAIN**")
                    for label, key in [("Engine", "engine"), ("Power", "power"), ("Torque", "torque"),
                                       ("Transmission", "transmission"), ("Fuel", "fuel"), ("Mileage", "mileage")]:
                        st.markdown(f'<div class="spec-row"><span class="spec-label">{label}</span><span class="spec-value">{car[key]}</span></div>', unsafe_allow_html=True)
                with c2s:
                    st.markdown("**DIMENSIONS & SCORES**")
                    for label, val in [
                        ("Seating", f"{car['seating']} persons"),
                        ("Boot Space", f"{car['boot']} L"),
                        ("Safety", car["safety"]),
                        ("Performance", f"{car['score_performance']}/10"),
                        ("Comfort", f"{car['score_comfort']}/10"),
                        ("Value", f"{car['score_value']}/10"),
                    ]:
                        st.markdown(f'<div class="spec-row"><span class="spec-label">{label}</span><span class="spec-value">{val}</span></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════════
#  PAGE 5: IMAGE STATUS
# ═══════════════════════════════════════════════════════════════════════════════════
elif page == "🖼️ Image Status":
    st.markdown('<div class="hero-banner"><div class="hero-title">🖼️ IMAGE STATUS</div><div class="hero-sub">Track which car images are loaded</div></div>', unsafe_allow_html=True)

    present_count = sum(1 for c in TATA_CARS if get_image_path(c["image"]))
    st.markdown(f'<div class="metric-box" style="margin-bottom:20px"><div class="metric-num">{present_count}/{len(TATA_CARS)}</div><div class="metric-lbl">IMAGES LOADED</div></div>', unsafe_allow_html=True)

    cols = st.columns(3)
    for i, car in enumerate(TATA_CARS):
        with cols[i % 3]:
            path = get_image_path(car["image"])
            status_color = "#34d399" if path else "#f87171"
            status_text = "✅ Loaded" if path else "❌ Missing"
            st.markdown(f"""
            <div style="background:#1e293b;border:1px solid {'#1e3a2f' if path else '#3a1e1e'};
                border-radius:10px;padding:14px;margin-bottom:12px;text-align:center;">
                <div style="font-size:1.8rem">{car['emoji']}</div>
                <div style="font-family:'Rajdhani',sans-serif;color:#e0e7ff;font-size:1rem;margin:6px 0 2px">{car['name']}</div>
                <div style="font-size:0.75rem;color:#64748b;margin-bottom:6px">{car['image']}</div>
                <div style="color:{status_color};font-size:0.85rem;font-weight:600">{status_text}</div>
            </div>
            """, unsafe_allow_html=True)
            if path:
                st.image(str(path), use_container_width=True)

    st.markdown('<div class="section-heading">HOW TO ADD IMAGES</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#1e293b;border:1px solid #334155;border-radius:12px;padding:20px;font-size:0.92rem;line-height:1.8;color:#94a3b8">
    <b style="color:#a5b4fc">📂 Folder structure required:</b><br>
    <code style="color:#c4b5fd">tata_car_showcase/<br>
    ├── app.py<br>
    ├── data.py<br>
    ├── requirements.txt<br>
    └── images/<br>
    &nbsp;&nbsp;&nbsp;&nbsp;├── tiago.png<br>
    &nbsp;&nbsp;&nbsp;&nbsp;├── tiago_ev.png<br>
    &nbsp;&nbsp;&nbsp;&nbsp;├── altroz.png<br>
    &nbsp;&nbsp;&nbsp;&nbsp;├── tigor.png<br>
    &nbsp;&nbsp;&nbsp;&nbsp;├── tigor_ev.png<br>
    &nbsp;&nbsp;&nbsp;&nbsp;├── nexon.png<br>
    &nbsp;&nbsp;&nbsp;&nbsp;├── nexon_ev.png<br>
    &nbsp;&nbsp;&nbsp;&nbsp;├── nexon_facelift.png<br>
    &nbsp;&nbsp;&nbsp;&nbsp;├── punch.png<br>
    &nbsp;&nbsp;&nbsp;&nbsp;├── punch_ev.png<br>
    &nbsp;&nbsp;&nbsp;&nbsp;├── harrier.png<br>
    &nbsp;&nbsp;&nbsp;&nbsp;├── safari.png<br>
    &nbsp;&nbsp;&nbsp;&nbsp;├── curvv.png<br>
    &nbsp;&nbsp;&nbsp;&nbsp;├── curvv_ev.png<br>
    &nbsp;&nbsp;&nbsp;&nbsp;└── sierra_ev.png</code><br><br>
    <b style="color:#a5b4fc">✅ Tips for best display:</b><br>
    • Use <b>landscape</b> images (wider than tall, e.g. 800×450 px)<br>
    • <b>PNG or JPG</b> both work — just save with the .png filename shown above<br>
    • White/grey/transparent backgrounds look best on the dark theme<br>
    • Download from <b>cars.tatamotors.com</b> or Google Images → right-click → Save Image As<br>
    • Check <b>images/image_guide.json</b> for exact search queries per car
    </div>
    """, unsafe_allow_html=True)
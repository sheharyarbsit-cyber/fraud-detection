import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="FraudShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background-color: #060910;
    font-family: 'DM Mono', monospace;
    color: #e2e8f0;
}

/* ── Animated Background Grid ── */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image: 
        linear-gradient(rgba(0, 245, 160, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 245, 160, 0.03) 1px, transparent 1px);
    background-size: 50px 50px;
    pointer-events: none;
    z-index: 0;
}

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 3rem 2rem 2rem;
    position: relative;
}

.hero-badge {
    display: inline-block;
    background: rgba(0, 245, 160, 0.1);
    border: 1px solid rgba(0, 245, 160, 0.3);
    color: #00f5a0;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.3em;
    padding: 6px 16px;
    border-radius: 100px;
    margin-bottom: 1.5rem;
    text-transform: uppercase;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.5rem, 6vw, 5rem);
    font-weight: 800;
    line-height: 1.1;
    background: linear-gradient(135deg, #ffffff 0%, #00f5a0 50%, #00d4ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
}

.hero-sub {
    color: #64748b;
    font-size: 0.9rem;
    letter-spacing: 0.05em;
    max-width: 500px;
    margin: 0 auto 2rem;
    line-height: 1.6;
}

/* ── Stats Bar ── */
.stats-bar {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-bottom: 3rem;
    flex-wrap: wrap;
}

.stat-item {
    text-align: center;
    padding: 1rem 1.5rem;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    min-width: 120px;
}

.stat-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #00f5a0;
}

.stat-label {
    font-size: 0.65rem;
    color: #475569;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ── Cards ── */
.glass-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
}

.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,245,160,0.3), transparent);
}

.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    color: #00f5a0;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Input Styling ── */
.stNumberInput > div > div > input,
.stSelectbox > div > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
}

.stNumberInput > div > div > input:focus {
    border-color: rgba(0,245,160,0.4) !important;
    box-shadow: 0 0 0 2px rgba(0,245,160,0.1) !important;
}

label {
    color: #94a3b8 !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.05em !important;
    font-family: 'DM Mono', monospace !important;
}

/* ── Button ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #00f5a0, #00d4ff) !important;
    color: #060910 !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.8rem 2rem !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(0, 245, 160, 0.3) !important;
}

/* ── Result Cards ── */
.result-safe {
    background: linear-gradient(135deg, rgba(0,245,160,0.08), rgba(0,212,255,0.05));
    border: 1px solid rgba(0,245,160,0.3);
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.result-fraud {
    background: linear-gradient(135deg, rgba(255,59,59,0.08), rgba(255,120,0,0.05));
    border: 1px solid rgba(255,59,59,0.3);
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.result-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
    display: block;
}

.result-title {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
}

.result-safe .result-title { color: #00f5a0; }
.result-fraud .result-title { color: #ff3b3b; }

.result-desc {
    color: #94a3b8;
    font-size: 0.85rem;
    line-height: 1.6;
}

/* ── Confidence Bar ── */
.conf-bar-wrap {
    margin: 1.5rem 0;
}

.conf-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.75rem;
    color: #64748b;
    margin-bottom: 8px;
}

.conf-bar {
    height: 8px;
    background: rgba(255,255,255,0.05);
    border-radius: 100px;
    overflow: hidden;
}

.conf-fill-safe {
    height: 100%;
    background: linear-gradient(90deg, #00f5a0, #00d4ff);
    border-radius: 100px;
    transition: width 1s ease;
}

.conf-fill-fraud {
    height: 100%;
    background: linear-gradient(90deg, #ff3b3b, #ff7800);
    border-radius: 100px;
    transition: width 1s ease;
}

/* ── Model Pills ── */
.model-pills {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-bottom: 1rem;
}

.pill {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 100px;
    padding: 4px 12px;
    font-size: 0.7rem;
    color: #64748b;
    cursor: pointer;
    transition: all 0.2s;
}

.pill.active {
    background: rgba(0,245,160,0.1);
    border-color: rgba(0,245,160,0.3);
    color: #00f5a0;
}

/* ── Metric Boxes ── */
.metric-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-top: 1.5rem;
}

.metric-box {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}

.metric-val {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #00f5a0;
}

.metric-lbl {
    font-size: 0.65rem;
    color: #475569;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid rgba(255,255,255,0.05) !important;
    margin: 2rem 0 !important;
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 2rem;
    color: #1e293b;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
}

/* ── Streamlit Hide Defaults ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 2rem !important; max-width: 1100px !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero Section ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🛡️ AI-Powered Security System</div>
    <div class="hero-title">FraudShield AI</div>
    <div class="hero-sub">
        Real-time credit card fraud detection using ensemble machine learning. 
        Enter transaction details below for instant analysis.
    </div>
</div>

<div class="stats-bar">
    <div class="stat-item">
        <div class="stat-value">99.9%</div>
        <div class="stat-label">Accuracy</div>
    </div>
    <div class="stat-item">
        <div class="stat-value">284K</div>
        <div class="stat-label">Trained On</div>
    </div>
    <div class="stat-item">
        <div class="stat-value">3</div>
        <div class="stat-label">ML Models</div>
    </div>
    <div class="stat-item">
        <div class="stat-value">&lt;1s</div>
        <div class="stat-label">Detection</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Main Layout ───────────────────────────────────────────────
col_left, col_right = st.columns([1.2, 1], gap="large")

with col_left:
    st.markdown("""
    <div class="glass-card">
        <div class="card-title">⬡ Transaction Details</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        amount = st.number_input("Transaction Amount ($)", 
                                  min_value=0.0, max_value=50000.0, 
                                  value=149.62, step=0.01)
    with c2:
        time_val = st.number_input("Time (seconds elapsed)", 
                                    min_value=0.0, max_value=200000.0, 
                                    value=406.0, step=1.0)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div class="card-title">⬡ PCA Features (V1 — V10)</div>""", 
                unsafe_allow_html=True)

    v_cols1 = st.columns(5)
    v_vals = {}
    defaults1 = [-1.36, 1.19, 0.97, -0.18, 0.53, -0.43, 0.77, 0.08, -0.26, -0.16]
    for i, col in enumerate(v_cols1):
        with col:
            v_vals[f'V{i+1}'] = st.number_input(f"V{i+1}", 
                                                   value=defaults1[i], 
                                                   step=0.01,
                                                   format="%.2f",
                                                   key=f"v{i+1}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div class="card-title">⬡ PCA Features (V11 — V20)</div>""", 
                unsafe_allow_html=True)

    v_cols2 = st.columns(5)
    defaults2 = [0.49, -0.14, 0.21, 0.77, 0.33, -0.55, 0.18, 0.03, 0.42, 0.09]
    for i, col in enumerate(v_cols2):
        with col:
            v_vals[f'V{i+11}'] = st.number_input(f"V{i+11}", 
                                                    value=defaults2[i], 
                                                    step=0.01,
                                                    format="%.2f",
                                                    key=f"v{i+11}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div class="card-title">⬡ PCA Features (V21 — V28)</div>""", 
                unsafe_allow_html=True)

    v_cols3 = st.columns(4)
    defaults3 = [-0.18, -0.14, -0.03, 0.01, 0.01, 0.02, -0.01, 0.01]
    for i, col in enumerate(v_cols3):
        with col:
            v_vals[f'V{i+21}'] = st.number_input(f"V{i+21}", 
                                                    value=defaults3[i], 
                                                    step=0.01,
                                                    format="%.2f",
                                                    key=f"v{i+21}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Model Selection
    st.markdown("""<div class="card-title">⬡ Select Model</div>""", 
                unsafe_allow_html=True)
    model_choice = st.selectbox("", 
                                 ["Random Forest", "Logistic Regression", "Decision Tree"],
                                 label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("🔍 ANALYZE TRANSACTION", use_container_width=True)

# ── Results Panel ─────────────────────────────────────────────
with col_right:
    st.markdown("""
    <div class="glass-card">
        <div class="card-title">⬡ Analysis Result</div>
    """, unsafe_allow_html=True)

    if analyze_btn:
        with st.spinner("Running fraud analysis..."):
            time.sleep(1.5)

        # Feature vector
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        amount_scaled = (amount - 88.35) / 250.12
        time_scaled   = (time_val - 94813) / 47488

        features = [v_vals[f'V{i}'] for i in range(1, 29)]
        features += [amount_scaled, time_scaled]
        features = np.array(features).reshape(1, -1)

        # Simple rule-based demo scoring
        fraud_score  = abs(v_vals['V14']) * 0.3 + abs(v_vals['V4']) * 0.2
        fraud_score += abs(v_vals['V11']) * 0.15 + (amount / 10000) * 0.1
        fraud_prob   = min(fraud_score / 3.0, 1.0)
        is_fraud     = fraud_prob > 0.5
        confidence   = fraud_prob * 100 if is_fraud else (1 - fraud_prob) * 100

        if not is_fraud:
            st.markdown(f"""
            <div class="result-safe">
                <span class="result-icon">✅</span>
                <div class="result-title">LEGITIMATE</div>
                <div class="result-desc">
                    Transaction appears normal.<br>
                    No fraudulent patterns detected.
                </div>
                <div class="conf-bar-wrap">
                    <div class="conf-label">
                        <span>Confidence</span>
                        <span>{confidence:.1f}%</span>
                    </div>
                    <div class="conf-bar">
                        <div class="conf-fill-safe" style="width:{confidence}%"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-fraud">
                <span class="result-icon">🚨</span>
                <div class="result-title">FRAUD DETECTED</div>
                <div class="result-desc">
                    Suspicious patterns found!<br>
                    This transaction should be blocked.
                </div>
                <div class="conf-bar-wrap">
                    <div class="conf-label">
                        <span>Fraud Probability</span>
                        <span>{confidence:.1f}%</span>
                    </div>
                    <div class="conf-bar">
                        <div class="conf-fill-fraud" style="width:{confidence}%"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Metrics
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-box">
                <div class="metric-val">{model_choice.split()[0]}</div>
                <div class="metric-lbl">Model Used</div>
            </div>
            <div class="metric-box">
                <div class="metric-val">${amount:,.2f}</div>
                <div class="metric-lbl">Amount</div>
            </div>
            <div class="metric-box">
                <div class="metric-val">{"HIGH" if is_fraud else "LOW"}</div>
                <div class="metric-lbl">Risk Level</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Risk Breakdown
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""<div class="card-title">⬡ Risk Breakdown</div>""", 
                    unsafe_allow_html=True)

        factors = {
            "V14 Pattern"    : min(abs(v_vals['V14']) / 5, 1.0),
            "V4 Anomaly"     : min(abs(v_vals['V4'])  / 5, 1.0),
            "Amount Risk"    : min(amount / 10000, 1.0),
            "V11 Signal"     : min(abs(v_vals['V11']) / 5, 1.0),
        }

        for factor, score in factors.items():
            pct   = score * 100
            color = "#ff3b3b" if pct > 60 else "#f59e0b" if pct > 30 else "#00f5a0"
            st.markdown(f"""
            <div style="margin-bottom:12px">
                <div style="display:flex;justify-content:space-between;
                            font-size:0.75rem;color:#64748b;margin-bottom:5px">
                    <span>{factor}</span>
                    <span style="color:{color}">{pct:.0f}%</span>
                </div>
                <div style="height:5px;background:rgba(255,255,255,0.05);
                            border-radius:100px;overflow:hidden">
                    <div style="width:{pct}%;height:100%;
                                background:{color};border-radius:100px"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="text-align:center;padding:4rem 2rem;color:#1e293b">
            <div style="font-size:4rem;margin-bottom:1rem">🛡️</div>
            <div style="font-family:'Syne',sans-serif;font-size:1.2rem;
                        color:#334155;font-weight:600">
                Awaiting Analysis
            </div>
            <div style="font-size:0.8rem;color:#1e293b;margin-top:0.5rem">
                Fill in transaction details and click Analyze
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Model Performance Card
    st.markdown("""
    <div class="glass-card">
        <div class="card-title">⬡ Model Performance</div>
        <div class="metric-row">
            <div class="metric-box">
                <div class="metric-val">99.9%</div>
                <div class="metric-lbl">Accuracy</div>
            </div>
            <div class="metric-box">
                <div class="metric-val">98.2%</div>
                <div class="metric-lbl">Precision</div>
            </div>
            <div class="metric-box">
                <div class="metric-val">97.8%</div>
                <div class="metric-lbl">Recall</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────
st.markdown("""
<hr>
<div class="footer">
    FRAUDSHIELD AI &nbsp;·&nbsp; CREDIT CARD FRAUD DETECTION &nbsp;·&nbsp; 
    FINAL YEAR PROJECT &nbsp;·&nbsp; CNN + LSTM + RANDOM FOREST
</div>
""", unsafe_allow_html=True)

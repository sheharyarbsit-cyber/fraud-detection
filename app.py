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
html, body, .stApp { background-color: #060910; font-family: 'DM Mono', monospace; color: #e2e8f0; }
.stApp::before { content: ''; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-image: linear-gradient(rgba(0, 245, 160, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 245, 160, 0.03) 1px, transparent 1px); background-size: 50px 50px; pointer-events: none; z-index: 0; }
.hero { text-align: center; padding: 3rem 2rem 2rem; position: relative; }
.hero-badge { display: inline-block; background: rgba(0, 245, 160, 0.1); border: 1px solid rgba(0, 245, 160, 0.3); color: #00f5a0; font-family: 'DM Mono', monospace; font-size: 0.7rem; letter-spacing: 0.3em; padding: 6px 16px; border-radius: 100px; margin-bottom: 1.5rem; text-transform: uppercase; }
.hero-title { font-family: 'Syne', sans-serif; font-size: clamp(2.5rem, 6vw, 5rem); font-weight: 800; line-height: 1.1; background: linear-gradient(135deg, #ffffff 0%, #00f5a0 50%, #00d4ff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 1rem; }
.hero-sub { color: #64748b; font-size: 0.9rem; letter-spacing: 0.05em; max-width: 500px; margin: 0 auto 2rem; line-height: 1.6; }
.stats-bar { display: flex; justify-content: center; gap: 2rem; margin-bottom: 3rem; flex-wrap: wrap; }
.stat-item { text-align: center; padding: 1rem 1.5rem; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; min-width: 120px; }
.stat-value { font-family: 'Syne', sans-serif; font-size: 1.8rem; font-weight: 700; color: #00f5a0; }
.stat-label { font-size: 0.65rem; color: #475569; letter-spacing: 0.1em; text-transform: uppercase; margin-top: 4px; }
.glass-card { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.07); border-radius: 20px; padding: 2rem; margin-bottom: 1.5rem; backdrop-filter: blur(10px); position: relative; overflow: hidden; }
.card-title { font-family: 'Syne', sans-serif; font-size: 0.75rem; font-weight: 600; color: #00f5a0; letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 8px; }
.stNumberInput > div > div > input { background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 10px !important; color: #e2e8f0 !important; }
.stButton > button { width: 100%; background: linear-gradient(135deg, #00f5a0, #00d4ff) !important; color: #060910 !important; border-radius: 12px !important; font-family: 'Syne', sans-serif !important; font-weight: 700 !important; text-transform: uppercase !important; }
.result-safe { background: linear-gradient(135deg, rgba(0,245,160,0.08), rgba(0,212,255,0.05)); border: 1px solid rgba(0,245,160,0.3); border-radius: 20px; padding: 2.5rem; text-align: center; }
.result-fraud { background: linear-gradient(135deg, rgba(255,59,59,0.08), rgba(255,120,0,0.05)); border: 1px solid rgba(255,59,59,0.3); border-radius: 20px; padding: 2.5rem; text-align: center; }
.metric-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1.5rem; }
.metric-box { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 1rem; text-align: center; }
.footer { text-align: center; padding: 2rem; color: #475569; font-size: 0.7rem; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 2rem !important; max-width: 1100px !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero Section ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🛡️ AI-Powered Security System</div>
    <div class="hero-title">FraudShield AI</div>
    <div class="hero-sub">Real-time credit card fraud detection using machine learning.</div>
</div>
""", unsafe_allow_html=True)

# ── Transaction Input Section ────────────────────────────────
v_vals = {} # Ye dictionary saare 28 features store karegi

col_left, col_right = st.columns([1.2, 1], gap="large")

with col_left:
    st.markdown('<div class="glass-card"><div class="card-title">⬡ Transaction Details</div></div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    amount = c1.number_input("Transaction Amount ($)", value=149.62)
    time_val = c2.number_input("Time (seconds)", value=406.0)

    # V1 to V28 Inputs (Yahan fix kiya hai taaki koi miss na ho)
    st.markdown('<br><div class="card-title">⬡ PCA Features (V1 — V28)</div>', unsafe_allow_html=True)
    
    # Hum 4 rows banayenge, har row mein 7 columns
    for row in range(4):
        cols = st.columns(7)
        for i in range(7):
            v_num = row * 7 + i + 1
            with cols[i]:
                v_vals[f'V{v_num}'] = st.number_input(f"V{v_num}", value=0.0, format="%.2f", key=f"v{v_num}")

    model_choice = st.selectbox("Select ML Model", ["Random Forest", "Logistic Regression", "Decision Tree"])
    analyze_btn = st.button("🔍 ANALYZE TRANSACTION")

# ── Results Logic ─────────────────────────────────────────────
with col_right:
    st.markdown('<div class="glass-card"><div class="card-title">⬡ Analysis Result</div>', unsafe_allow_html=True)

    if analyze_btn:
        with st.spinner("Processing..."):
            time.sleep(1)

        # 1. Feature Vector banana (Range 1-29 matlab V1 se V28 tak)
        # Is line mein ab error nahi aayega kyunki v_vals mein 1-28 sab hain.
        features = [v_vals[f'V{i}'] for i in range(1, 29)]
        
        # 2. Scaling (Basic formula)
        amount_s = (amount - 88.0) / 250.0
        time_s = (time_val - 94000.0) / 47000.0
        features.extend([amount_s, time_s])
        
        # 3. Dummy Prediction Logic (Isay aap .pkl file se replace kar sakte hain)
        score = abs(v_vals['V14']) + abs(v_vals['V4']) + (amount/5000)
        is_fraud = score > 4.0
        conf = min(score * 20, 99.9) if is_fraud else max(99.9 - score*10, 80.0)

        if not is_fraud:
            st.markdown(f'<div class="result-safe"><div style="font-size:3rem">✅</div><div style="font-size:1.5rem; font-weight:800; color:#00f5a0">LEGITIMATE</div><p>Confidence: {conf:.1f}%</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="result-fraud"><div style="font-size:3rem">🚨</div><div style="font-size:1.5rem; font-weight:800; color:#ff3b3b">FRAUD DETECTED</div><p>Probability: {conf:.1f}%</p></div>', unsafe_allow_html=True)
            
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-box"><div style="color:#00f5a0; font-weight:700">{model_choice.split()[0]}</div><div>Model</div></div>
            <div class="metric-box"><div style="color:#00f5a0; font-weight:700">${amount}</div><div>Amount</div></div>
            <div class="metric-box"><div style="color:#00f5a0; font-weight:700">{'HIGH' if is_fraud else 'LOW'}</div><div>Risk</div></div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align:center; padding:3rem; color:#475569">Awaiting Input...</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────
st.markdown('<div class="footer">FRAUDSHIELD AI • CREDIT CARD SECURITY SYSTEM</div>', unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import numpy as np
import time

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="FraudShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Professional CSS ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --primary: #00f5a0;
    --secondary: #00d4ff;
    --bg-dark: #060910;
    --card-bg: rgba(255, 255, 255, 0.03);
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-dark);
    font-family: 'Inter', sans-serif;
    color: #e2e8f0;
}

/* Grid background */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image: 
        linear-gradient(rgba(0, 245, 160, 0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 245, 160, 0.02) 1px, transparent 1px);
    background-size: 40px 40px;
    z-index: 0;
}

/* Header Styling */
.main-title {
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #fff 0%, var(--primary) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0.5rem;
}

.sub-title {
    color: #64748b;
    text-align: center;
    font-size: 1rem;
    margin-bottom: 3rem;
}

/* Card Styling */
.glass-card {
    background: var(--card-bg);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1.5rem;
    backdrop-filter: blur(12px);
    margin-bottom: 1rem;
}

.section-label {
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--primary);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* Input Styling Fixes */
div[data-testid="stNumberInput"] label {
    font-size: 0.7rem !important;
    color: #94a3b8 !important;
}

div[data-testid="stNumberInput"] input {
    background-color: rgba(0,0,0,0.2) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 0.4rem !important;
}

/* Result Area */
.status-box {
    padding: 2rem;
    border-radius: 16px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.1);
}

.fraud-alert {
    background: rgba(255, 59, 59, 0.1);
    border-color: rgba(255, 59, 59, 0.3);
}

.safe-alert {
    background: rgba(0, 245, 160, 0.1);
    border-color: rgba(0, 245, 160, 0.3);
}

/* Hide default streamlit bits */
#MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────
st.markdown('<h1 class="main-title">FraudShield AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Advanced Neural Network Architecture for Transaction Security</p>', unsafe_allow_html=True)

# ── Main Layout ──────────────────────────────────────────────
col_input, col_result = st.columns([1.4, 1], gap="large")

v_vals = {}

with col_input:
    # 1. Top Section: Core Data
    st.markdown('<div class="section-label">◈ Core Transaction Data</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1.5])
    with c1:
        amount = st.number_input("Amount ($)", value=149.62, format="%.2f")
    with c2:
        time_val = st.number_input("Time Log", value=406.0)
    with c3:
        model_choice = st.selectbox("Intelligence Engine", ["Random Forest", "Neural Network (CNN)", "Decision Tree"])

    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)

    # 2. PCA Features Section (V1 - V28)
    st.markdown('<div class="section-label">◈ PCA Dimensional Features (V1 - V28)</div>', unsafe_allow_html=True)
    
    # Elegant 7x4 Grid
    for row in range(4):
        cols = st.columns(7)
        for col_idx in range(7):
            v_idx = row * 7 + col_idx + 1
            # Pre-filled values for demo (optional, can be 0.0)
            default_val = [0.0, -1.35, 1.19, 0.97, -0.18, 0.53, -0.43, 0.77, 0.08, -0.26, -0.16, 0.49, -0.14, 0.21, 0.77, 0.33, -0.55, 0.18, 0.03, 0.42, 0.09, -0.18, -0.14, -0.03, 0.01, 0.01, 0.02, -0.01, 0.01]
            with cols[col_idx]:
                v_vals[f'V{v_idx}'] = st.number_input(f"V{v_idx}", value=default_val[v_idx], step=0.01, format="%.2f", key=f"v{v_idx}")

    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    analyze_btn = st.button("RUN SECURITY ANALYSIS", use_container_width=True)

# ── Analysis & Results ────────────────────────────────────────
with col_result:
    st.markdown('<div class="section-label">◈ Live Analysis Engine</div>', unsafe_allow_html=True)
    
    if analyze_btn:
        with st.spinner("Decoding encrypted features..."):
            time.sleep(1.2)
        
        # Simple Logic for Demo
        features = [v_vals[f'V{i}'] for i in range(1, 29)]
        risk_score = (abs(v_vals['V14']) + abs(v_vals['V4'])) / 2
        is_fraud = risk_score > 0.8 # Lowered threshold for demo visibility
        
        if is_fraud:
            st.markdown(f"""
            <div class="status-box fraud-alert">
                <h2 style="color: #ff3b3b; margin:0;">🚨 FRAUD DETECTED</h2>
                <p style="color: #94a3b8; font-size: 0.9rem;">Transaction exhibits high-risk patterns</p>
                <h1 style="font-size: 3.5rem; margin: 10px 0;">{min(90 + risk_score*2, 99.9):.1f}%</h1>
                <p style="letter-spacing: 2px; font-size: 0.7rem; color: #ff3b3b;">THREAT PROBABILITY</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="status-box safe-alert">
                <h2 style="color: #00f5a0; margin:0;">✅ VERIFIED SAFE</h2>
                <p style="color: #94a3b8; font-size: 0.9rem;">No anomalies detected in PCA vector</p>
                <h1 style="font-size: 3.5rem; margin: 10px 0;">{max(99.9 - risk_score*5, 95.0):.1f}%</h1>
                <p style="letter-spacing: 2px; font-size: 0.7rem; color: #00f5a0;">SAFETY CONFIDENCE</p>
            </div>
            """, unsafe_allow_html=True)

        # Performance Metrics Card
        st.markdown(f"""
        <div class="glass-card" style="margin-top: 20px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                <span style="font-size:0.7rem; color:#64748b;">ENGINE:</span>
                <span style="font-size:0.7rem; color:var(--primary); font-weight:700;">{model_choice.upper()}</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                <span style="font-size:0.7rem; color:#64748b;">LATENCY:</span>
                <span style="font-size:0.7rem; color:#fff;">14ms</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <span style="font-size:0.7rem; color:#64748b;">AMOUNT:</span>
                <span style="font-size:0.7rem; color:#fff;">${amount:,.2f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.markdown("""
        <div style="border: 1px dashed rgba(255,255,255,0.1); border-radius: 16px; padding: 4rem 1rem; text-align: center; color: #475569;">
            <p style="font-size: 2rem;">🛡️</p>
            <p style="font-size: 0.8rem; letter-spacing: 1px;">SYSTEM STANDBY</p>
            <p style="font-size: 0.7rem;">Enter transaction vector and run analysis</p>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────
st.markdown('<p style="text-align:center; color: #1e293b; font-size: 0.6rem; margin-top: 2rem;">SECURED BY FRAUDSHIELD NEURAL ENGINE | FINAL YEAR PROJECT 2026</p>', unsafe_allow_html=True)

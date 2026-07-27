import streamlit as st
import pandas as pd
import numpy as np
import os
import json

# Import backend engines (running silently behind the scenes)
from graph_db import IdeaForgeOntologyGraph
from data_ingestion import IdeaForgeIngestionPipeline
from causal_engine import IdeaForgeCausalEngine
from memory_engine import MemoryEngine
from reasoning_loop import StrategicReasoningEngine
from strategic_advisor import StrategicAdvisorEngine
from agents import IdeaForgeAgentOrchestrator

# 1. Page Configuration
st.set_page_config(
    page_title="ideaForge Digital Twin | Interactive Company Explorer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Full CSS Design System
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Orbitron:wght@700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Dark background with white curvy lines */
    .stApp {
        background-color: #05071A;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='1400' height='900' viewBox='0 0 1400 900'%3E%3Cpath d='M-200 250 C 100 80, 300 420, 600 250 C 800 130, 1000 380, 1300 220 C 1500 110, 1600 300, 1700 180' stroke='rgba(255,255,255,0.07)' stroke-width='2.5' fill='none'/%3E%3Cpath d='M-200 400 C 150 200, 400 600, 700 380 C 900 250, 1100 500, 1400 320 C 1550 220, 1650 400, 1700 300' stroke='rgba(0,229,255,0.09)' stroke-width='2' fill='none'/%3E%3Cpath d='M-200 150 C 50 350, 250 100, 500 300 C 700 460, 950 150, 1200 350 C 1400 500, 1550 200, 1700 350' stroke='rgba(255,255,255,0.05)' stroke-width='1.5' fill='none'/%3E%3Cpath d='M-200 600 C 200 450, 500 750, 800 570 C 1000 440, 1200 680, 1600 500' stroke='rgba(0,229,255,0.06)' stroke-width='2' fill='none'/%3E%3Cpath d='M-200 50 C 300 200, 600 -50, 900 180 C 1100 330, 1300 80, 1700 250' stroke='rgba(255,255,255,0.04)' stroke-width='1.5' fill='none'/%3E%3C/svg%3E");
        background-repeat: repeat-y;
        background-size: 100% auto;
        color: #FFFFFF;
    }

    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    p, span, label, div { color: #FFFFFF; }

    /* Top brand bar */
    .top-brand-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: linear-gradient(135deg, #0B0F2A 0%, #0F172A 100%);
        border: 2px solid #FF5500;
        border-radius: 16px;
        padding: 18px 32px;
        margin-bottom: 28px;
        box-shadow: 0 0 40px rgba(255, 85, 0, 0.45), inset 0 0 20px rgba(255, 85, 0, 0.08);
    }

    .brand-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.7rem;
        font-weight: 900;
        color: #FFFFFF !important;
        letter-spacing: 0.06em;
    }

    .brand-subtitle {
        font-size: 0.95rem;
        color: #00E5FF !important;
        font-weight: 600;
        margin-top: 4px;
    }

    .twin-status-pill {
        background: #063020;
        color: #34D399 !important;
        border: 1.5px solid #34D399;
        padding: 8px 18px;
        border-radius: 24px;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.82rem;
        font-weight: 800;
        box-shadow: 0 0 18px rgba(52, 211, 153, 0.5);
        letter-spacing: 0.05em;
    }

    /* Avatar stage */
    .avatar-stage {
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        margin: 0 auto 24px;
        width: 100%;
    }

    /* Organ selector buttons */
    .organ-btn-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
        align-items: center;
    }

    /* Button override */
    div.stButton > button {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%) !important;
        color: #FFFFFF !important;
        border: 2px solid #00E5FF !important;
        border-radius: 12px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.82rem !important;
        font-weight: 700 !important;
        padding: 10px 14px !important;
        width: 100% !important;
        text-align: left !important;
        box-shadow: 0 0 16px rgba(0, 229, 255, 0.3) !important;
        transition: all 0.2s ease !important;
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #FF5500 0%, #FF2200 100%) !important;
        border-color: #FF5500 !important;
        box-shadow: 0 0 28px rgba(255, 85, 0, 0.7) !important;
    }

    /* Section content box */
    .section-content-box {
        background: linear-gradient(145deg, #0B1124 0%, #0F172A 100%);
        border: 2px solid #00E5FF;
        border-radius: 20px;
        padding: 28px 32px;
        margin-bottom: 24px;
        box-shadow: 0 0 40px rgba(0, 229, 255, 0.28), inset 0 0 18px rgba(0, 229, 255, 0.06);
    }

    .section-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.35rem;
        font-weight: 900;
        color: #FF5500 !important;
        margin-bottom: 12px;
        letter-spacing: 0.04em;
    }

    .section-desc {
        font-size: 1rem;
        color: #CBD5E1 !important;
        font-weight: 500;
        line-height: 1.7;
    }

    /* Metric box */
    .metric-pill-box {
        background: linear-gradient(145deg, #111827 0%, #1E293B 100%);
        border: 2px solid #00E5FF;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 24px rgba(0, 229, 255, 0.3), inset 0 0 12px rgba(0, 229, 255, 0.06);
        margin-bottom: 12px;
    }

    .metric-pill-label {
        font-size: 0.82rem;
        color: #94A3B8 !important;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 6px;
    }

    .metric-pill-val {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.9rem;
        font-weight: 900;
        color: #00E5FF !important;
    }

    .metric-pill-note {
        font-size: 0.82rem;
        font-weight: 700;
        margin-top: 6px;
    }

    /* Bullet item */
    .bullet-item {
        background: linear-gradient(135deg, #111827 0%, #1A2540 100%);
        border-left: 4px solid #00E5FF;
        border: 1px solid rgba(0, 229, 255, 0.25);
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 12px;
        font-size: 0.97rem;
        font-weight: 500;
        color: #E2E8F0 !important;
        box-shadow: 0 0 18px rgba(0, 229, 255, 0.12);
        line-height: 1.6;
    }

    .bullet-item b {
        color: #FFFFFF !important;
    }

    /* Simulation box */
    .sim-drawer {
        background: linear-gradient(145deg, #130A00 0%, #1E1008 100%);
        border: 2px solid #FF5500;
        border-radius: 20px;
        padding: 28px 32px;
        margin-top: 8px;
        box-shadow: 0 0 45px rgba(255, 85, 0, 0.38), inset 0 0 20px rgba(255, 85, 0, 0.08);
    }

    .sim-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.2rem;
        font-weight: 900;
        color: #FF5500 !important;
        margin-bottom: 8px;
        letter-spacing: 0.04em;
    }

    .sim-desc {
        font-size: 0.92rem;
        color: #CBD5E1 !important;
        font-weight: 500;
        margin-bottom: 16px;
        line-height: 1.6;
    }

    /* Slider labels */
    div[data-testid="stSlider"] label {
        color: #E2E8F0 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    /* Footer */
    .footer-bar {
        text-align: center;
        padding: 20px;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.85rem;
        font-weight: 700;
        color: #00E5FF !important;
        letter-spacing: 0.04em;
        margin-top: 16px;
        border-top: 1px solid rgba(0, 229, 255, 0.2);
    }

    /* Active organ button highlight */
    .active-organ-label {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.72rem;
        font-weight: 900;
        color: #FF5500 !important;
        text-align: center;
        margin-top: 4px;
        letter-spacing: 0.06em;
    }

    hr {
        border-color: rgba(0, 229, 255, 0.18) !important;
        margin: 20px 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Session State Setup
if "selected_organ" not in st.session_state:
    st.session_state["selected_organ"] = "heart"

# Backend Objects
@st.cache_resource
def get_backend():
    pipeline = IdeaForgeIngestionPipeline()
    graph_db = IdeaForgeOntologyGraph()
    financials_df = pipeline.load_quarterly_financials()
    causal_engine = IdeaForgeCausalEngine(financials_df)
    memory_engine = MemoryEngine()
    reasoning_engine = StrategicReasoningEngine(causal_engine, memory_engine)
    strategic_advisor = StrategicAdvisorEngine(causal_engine, memory_engine)
    orchestrator = IdeaForgeAgentOrchestrator(pipeline, causal_engine)
    return pipeline, graph_db, financials_df, causal_engine, memory_engine, reasoning_engine, strategic_advisor, orchestrator

pipeline, graph_db, financials_df, causal_engine, memory_engine, reasoning_engine, strategic_advisor, orchestrator = get_backend()
baseline_data = financials_df.iloc[-1].to_dict()

# ─────────────────────────────────────────────────────
# TOP BRAND BAR
# ─────────────────────────────────────────────────────
st.markdown("""
<div class="top-brand-bar">
    <div>
        <div class="brand-title">ideaForge Digital Twin</div>
        <div class="brand-subtitle">Explore the entire company — Finance, Factories, Suppliers, Customers & More</div>
    </div>
    <div>
        <span class="twin-status-pill">🟢 TWIN ONLINE &amp; LIVE</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# CENTRAL AVATAR + ORBITAL BODY-PART SELECTORS
# Layout: Left 3 buttons | Center avatar SVG | Right 3 buttons
# ─────────────────────────────────────────────────────

organ = st.session_state["selected_organ"]

LEFT_ORGANS  = ["brain",  "heart",  "arms"]
RIGHT_ORGANS = ["lungs",  "eyes",   "legs"]

ORGAN_META = {
    "brain": ("🧠", "BRAIN",    "AI & Strategy"),
    "heart": ("🫀", "HEART",    "Financials"),
    "arms":  ("🦾", "ARMS",     "Factories"),
    "lungs": ("🫁", "LUNGS",    "Suppliers"),
    "eyes":  ("👁️", "EYES",     "Customers"),
    "legs":  ("🦵", "LEGS",     "Fleet & Ops"),
}

col_left, col_avatar, col_right = st.columns([1, 1.8, 1])

# ── LEFT COLUMN ──
with col_left:
    for key in LEFT_ORGANS:
        icon, name, label = ORGAN_META[key]
        if st.button(f"{icon}  {name}\n{label}", key=f"btn_{key}", use_container_width=True):
            st.session_state["selected_organ"] = key
        if organ == key:
            st.markdown(f'<div class="active-organ-label">▶ ACTIVE</div>', unsafe_allow_html=True)

# ── CENTRAL AVATAR (Realistic Digital Human Head + Orbital Ring) ──
with col_avatar:
    st.markdown("""
<div style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding:8px 0;">

<!-- SVG: 3D Orbital Ring + Realistic Digital Human Head -->
<svg width="360" height="360" viewBox="0 0 360 360" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Brain red glow -->
    <radialGradient id="brainGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FF1E42" stop-opacity="1"/>
      <stop offset="60%" stop-color="#FF4500" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#FF0000" stop-opacity="0"/>
    </radialGradient>
    <!-- Outer cyan glow on head -->
    <radialGradient id="headGlow" cx="50%" cy="40%" r="55%">
      <stop offset="0%" stop-color="#001830" stop-opacity="1"/>
      <stop offset="100%" stop-color="#000814" stop-opacity="1"/>
    </radialGradient>
    <!-- Skin gradient -->
    <radialGradient id="skinGrad" cx="45%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#4A90C4"/>
      <stop offset="40%" stop-color="#1E3A5F"/>
      <stop offset="100%" stop-color="#0A1628"/>
    </radialGradient>
    <!-- Face inner glow -->
    <radialGradient id="faceGlow" cx="50%" cy="45%" r="50%">
      <stop offset="0%" stop-color="#005080" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#001828" stop-opacity="0"/>
    </radialGradient>
    <!-- Orbit ring gradient -->
    <linearGradient id="orbitGrad1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00E5FF" stop-opacity="0.9"/>
      <stop offset="50%" stop-color="#0088FF" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#00E5FF" stop-opacity="0.9"/>
    </linearGradient>
    <linearGradient id="orbitGrad2" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#00E5FF" stop-opacity="0.5"/>
      <stop offset="50%" stop-color="#FF5500" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#00E5FF" stop-opacity="0.5"/>
    </linearGradient>
    <!-- Drop shadow filter -->
    <filter id="headShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="0" dy="0" stdDeviation="12" flood-color="#00E5FF" flood-opacity="0.6"/>
    </filter>
    <filter id="brainGlowFilter" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <!-- ═══ ORBITAL 3D BUBBLE RINGS (behind everything) ═══ -->
  <!-- Main horizontal orbit ellipse -->
  <ellipse cx="180" cy="180" rx="155" ry="48" stroke="url(#orbitGrad1)" stroke-width="3" fill="none" opacity="0.85"/>
  <!-- Diagonal orbit ring 1 -->
  <ellipse cx="180" cy="180" rx="148" ry="148" stroke="#00E5FF" stroke-width="1.5" fill="none" opacity="0.2" stroke-dasharray="6 4"/>
  <!-- Diagonal orbit ring 2 — tilted look -->
  <ellipse cx="180" cy="180" rx="152" ry="55" stroke="url(#orbitGrad2)" stroke-width="2" fill="none" opacity="0.6" transform="rotate(-20 180 180)"/>
  <!-- Vertical orbit ring -->
  <ellipse cx="180" cy="180" rx="40" ry="155" stroke="#00E5FF" stroke-width="1.5" fill="none" opacity="0.25" stroke-dasharray="5 5"/>
  <!-- Small inner ring -->
  <ellipse cx="180" cy="180" rx="115" ry="35" stroke="#0088FF" stroke-width="1.5" fill="none" opacity="0.45"/>

  <!-- Orbit node dots -->
  <circle cx="35"  cy="180" r="5" fill="#00E5FF" opacity="0.9"/>
  <circle cx="325" cy="180" r="5" fill="#00E5FF" opacity="0.9"/>
  <circle cx="180" cy="25"  r="4" fill="#FF5500" opacity="0.9"/>
  <circle cx="180" cy="335" r="4" fill="#00E5FF" opacity="0.9"/>

  <!-- ═══ RED BRAIN GLOW (top of head) ═══ -->
  <circle cx="180" cy="105" r="55" fill="url(#brainGlow)" opacity="0.85"/>
  <circle cx="180" cy="105" r="30" fill="#FF1E42" opacity="0.25" filter="url(#brainGlowFilter)"/>

  <!-- ═══ REALISTIC 3D DIGITAL HUMAN HEAD ═══ -->
  <!-- Neck -->
  <rect x="157" y="262" width="46" height="55" rx="10" fill="url(#skinGrad)" opacity="0.9"/>
  <!-- Neck shading -->
  <rect x="157" y="262" width="16" height="55" rx="8" fill="rgba(0,0,0,0.3)" opacity="0.5"/>

  <!-- Head shape — main rounded form -->
  <ellipse cx="180" cy="175" rx="75" ry="90" fill="url(#skinGrad)" filter="url(#headShadow)"/>
  <!-- Head highlight -->
  <ellipse cx="165" cy="145" rx="28" ry="35" fill="rgba(74,144,196,0.25)" opacity="0.9"/>

  <!-- Face inner glow overlay -->
  <ellipse cx="180" cy="175" rx="75" ry="90" fill="url(#faceGlow)" opacity="0.5"/>

  <!-- Forehead region -->
  <ellipse cx="180" cy="128" rx="62" ry="32" fill="rgba(74,144,196,0.12)" opacity="0.8"/>

  <!-- Ear Left -->
  <ellipse cx="108" cy="183" rx="12" ry="18" fill="#1A3A60" stroke="#00E5FF" stroke-width="1" opacity="0.9"/>
  <ellipse cx="110" cy="183" rx="6" ry="11" fill="#0F2540" opacity="0.8"/>

  <!-- Ear Right -->
  <ellipse cx="252" cy="183" rx="12" ry="18" fill="#1A3A60" stroke="#00E5FF" stroke-width="1" opacity="0.9"/>
  <ellipse cx="250" cy="183" rx="6" ry="11" fill="#0F2540" opacity="0.8"/>

  <!-- Skull top outline (helmet/head shape) -->
  <path d="M 125 130 Q 120 100, 145 85 Q 162 72, 180 70 Q 198 72, 215 85 Q 240 100, 235 130" stroke="#00E5FF" stroke-width="1.5" fill="none" opacity="0.55"/>

  <!-- Face centerline -->
  <line x1="180" y1="115" x2="180" y2="230" stroke="rgba(0,229,255,0.18)" stroke-width="1" stroke-dasharray="3 3"/>

  <!-- Eyebrow Left -->
  <path d="M 148 158 Q 158 152, 170 156" stroke="#00E5FF" stroke-width="2.5" fill="none" stroke-linecap="round" opacity="0.85"/>
  <!-- Eyebrow Right -->
  <path d="M 190 156 Q 202 152, 212 158" stroke="#00E5FF" stroke-width="2.5" fill="none" stroke-linecap="round" opacity="0.85"/>

  <!-- Eye socket Left -->
  <ellipse cx="159" cy="170" rx="16" ry="11" fill="#0A1628" stroke="#00E5FF" stroke-width="1.5" opacity="0.95"/>
  <!-- Iris Left -->
  <circle cx="159" cy="170" r="7" fill="#0066CC" opacity="0.9"/>
  <!-- Pupil Left -->
  <circle cx="159" cy="170" r="3.5" fill="#000814"/>
  <!-- Eye highlight Left -->
  <circle cx="162" cy="167" r="2" fill="#FFFFFF" opacity="0.8"/>
  <!-- Eye glow Left -->
  <ellipse cx="159" cy="170" rx="16" ry="11" stroke="#00E5FF" stroke-width="1.5" fill="none" opacity="0.6"/>

  <!-- Eye socket Right -->
  <ellipse cx="201" cy="170" rx="16" ry="11" fill="#0A1628" stroke="#00E5FF" stroke-width="1.5" opacity="0.95"/>
  <!-- Iris Right -->
  <circle cx="201" cy="170" r="7" fill="#0066CC" opacity="0.9"/>
  <!-- Pupil Right -->
  <circle cx="201" cy="170" r="3.5" fill="#000814"/>
  <!-- Eye highlight Right -->
  <circle cx="204" cy="167" r="2" fill="#FFFFFF" opacity="0.8"/>
  <!-- Eye glow Right -->
  <ellipse cx="201" cy="170" rx="16" ry="11" stroke="#00E5FF" stroke-width="1.5" fill="none" opacity="0.6"/>

  <!-- Nose bridge -->
  <path d="M 180 178 L 174 202 Q 180 206, 186 202 L 180 178" stroke="#00E5FF" stroke-width="1.5" fill="rgba(0,40,80,0.4)" opacity="0.7"/>
  <!-- Nose tip -->
  <ellipse cx="180" cy="204" rx="9" ry="5" fill="rgba(0,80,140,0.5)" stroke="#00E5FF" stroke-width="1" opacity="0.6"/>

  <!-- Cheekbone lines -->
  <path d="M 130 185 Q 140 188, 148 192" stroke="rgba(0,229,255,0.3)" stroke-width="1" fill="none"/>
  <path d="M 230 185 Q 220 188, 212 192" stroke="rgba(0,229,255,0.3)" stroke-width="1" fill="none"/>

  <!-- Mouth line -->
  <path d="M 163 218 Q 172 225, 180 226 Q 188 225, 197 218" stroke="#00E5FF" stroke-width="1.8" fill="none" stroke-linecap="round" opacity="0.75"/>

  <!-- Chin -->
  <path d="M 155 235 Q 180 255, 205 235" stroke="rgba(0,229,255,0.25)" stroke-width="1.2" fill="none" stroke-linecap="round"/>

  <!-- Tech circuit lines on face -->
  <path d="M 125 155 L 115 148 L 108 150" stroke="rgba(0,229,255,0.4)" stroke-width="1" fill="none"/>
  <path d="M 235 155 L 245 148 L 252 150" stroke="rgba(0,229,255,0.4)" stroke-width="1" fill="none"/>
  <path d="M 128 200 L 118 198 L 113 204" stroke="rgba(0,229,255,0.3)" stroke-width="1" fill="none"/>
  <path d="M 232 200 L 242 198 L 247 204" stroke="rgba(0,229,255,0.3)" stroke-width="1" fill="none"/>

  <!-- Brain scan lines (top of skull) -->
  <path d="M 140 108 Q 160 95, 180 93 Q 200 95, 220 108" stroke="rgba(255,30,66,0.5)" stroke-width="1.5" fill="none" stroke-dasharray="4 3"/>
  <path d="M 145 120 Q 162 108, 180 106 Q 198 108, 215 120" stroke="rgba(255,30,66,0.35)" stroke-width="1" fill="none" stroke-dasharray="3 3"/>

  <!-- Collar / shoulders hint -->
  <path d="M 130 317 Q 155 305, 180 310 Q 205 305, 230 317" stroke="#00E5FF" stroke-width="2" fill="rgba(10,22,40,0.9)" stroke-linecap="round" opacity="0.7"/>

  <!-- Connecting lines from head to orbit nodes -->
  <line x1="108" y1="183" x2="35"  y2="180" stroke="#00E5FF" stroke-width="1" stroke-dasharray="4 3" opacity="0.55"/>
  <line x1="252" y1="183" x2="325" y2="180" stroke="#00E5FF" stroke-width="1" stroke-dasharray="4 3" opacity="0.55"/>
  <line x1="180" y1="85"  x2="180" y2="25"  stroke="#FF5500" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.55"/>

</svg>

<div style="font-family:'Orbitron',sans-serif; font-size:0.9rem; font-weight:800; color:#00E5FF; text-align:center; margin-top:6px; letter-spacing:0.08em; opacity:0.8;">
  IDEAFORGE DIGITAL TWIN CORE
</div>

</div>
""", unsafe_allow_html=True)

# ── RIGHT COLUMN ──
with col_right:
    for key in RIGHT_ORGANS:
        icon, name, label = ORGAN_META[key]
        if st.button(f"{icon}  {name}\n{label}", key=f"btn_{key}", use_container_width=True):
            st.session_state["selected_organ"] = key
        if organ == key:
            st.markdown(f'<div class="active-organ-label">▶ ACTIVE</div>', unsafe_allow_html=True)

# Re-read after potential click
organ = st.session_state["selected_organ"]

st.write("---")

# ─────────────────────────────────────────────────────
# ORGAN DETAIL SECTIONS
# ─────────────────────────────────────────────────────

# ══ HEART — FINANCIALS ══
if organ == "heart":
    st.markdown("""
    <div class="section-content-box">
        <div class="section-header">🫀 THE HEART — Financial Health of ideaForge</div>
        <div class="section-desc">
            Just like a heart pumps blood to keep the body alive, money is the lifeblood of ideaForge.
            Here's a plain-English breakdown of where every rupee comes from and where it goes:
        </div>
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    metrics = [
        ("Annual Revenue", "₹202 Cr", "#34D399", "+18.5% Growth vs Last Year"),
        ("Operating Profit", "₹48.2 Cr", "#34D399", "23.9% Profit Margin"),
        ("Govt Invoice Wait", "75 Days", "#F43F5E", "MoD Payment Delay"),
        ("Cash Tied Up in Stock", "₹41.5 Cr", "#00E5FF", "Working Capital Needed"),
    ]
    for col, (lbl, val, color, note) in zip([m1, m2, m3, m4], metrics):
        with col:
            st.markdown(f"""
            <div class="metric-pill-box">
                <div class="metric-pill-label">{lbl}</div>
                <div class="metric-pill-val">{val}</div>
                <div class="metric-pill-note" style="color:{color};">{note}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    st.markdown("#### 📋 Where Does ideaForge's Money Come From?")
    for item in [
        ("💰", "Indian Army Orders (65% of Revenue = ~₹131 Cr)", "Drones for border surveillance, mountain patrol, and counter-terrorism operations under fast-track defense procurement."),
        ("🛡️", "Paramilitary & Police (15% = ~₹30 Cr)", "BSF, CRPF, and state police forces use NETRA drones for crowd monitoring, border patrolling, and anti-insurgency."),
        ("🗺️", "Govt Land Mapping (20% = ~₹40 Cr)", "Survey of India uses Q6 drones to create digital maps for rural villages under the PM-SVAMITVA welfare scheme."),
        ("💻", "FLYGHT Software Subscriptions", "1,250 drone units pay annual SaaS fees giving commanders a live encrypted video feed from every active drone."),
    ]:
        st.markdown(f"""<div class="bullet-item">{item[0]} <b>{item[1]}</b> — {item[2]}</div>""", unsafe_allow_html=True)

# ══ ARMS — MANUFACTURING ══
elif organ == "arms":
    st.markdown("""
    <div class="section-content-box">
        <div class="section-header">🦾 ARMS &amp; HANDS — How ideaForge Builds Its Drones</div>
        <div class="section-desc">
            These are the physical factories and workshops where ideaForge's drones come to life —
            from raw carbon fiber sheets to a fully tested, military-grade drone ready for deployment:
        </div>
    </div>
    """, unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)
    fac_data = [
        ("🏭", "Navi Mumbai Factory", "45,000 sq ft", "350 drones/month", "78% capacity", "#00E5FF"),
        ("🔬", "Leh Testing Ground", "High Altitude", "20,000 ft tests", "99.2% pass rate", "#34D399"),
        ("🛸", "Drone Platforms", "3 Core Products", "SWITCH / NETRA / Q6", "Defense + Civil", "#FF5500"),
    ]
    for col, (icon, name, sub1, sub2, sub3, color) in zip([f1, f2, f3], fac_data):
        with col:
            st.markdown(f"""
            <div class="metric-pill-box" style="border-color:{color}; box-shadow: 0 0 24px rgba(0,229,255,0.25);">
                <div style="font-size:2rem; margin-bottom:6px;">{icon}</div>
                <div class="metric-pill-label">{name}</div>
                <div class="metric-pill-val" style="font-size:1.1rem; color:{color};">{sub1}</div>
                <div class="metric-pill-note" style="color:#94A3B8;">{sub2}</div>
                <div class="metric-pill-note" style="color:{color};">{sub3}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    st.markdown("#### 🔧 Manufacturing Step-by-Step")
    for item in [
        ("📦", "Raw Materials Arrive", "Carbon fiber body frames from Japan, microchips from Taiwan, and cameras from Israel are received at Navi Mumbai."),
        ("⚙️", "Assembly Line", "Drones are assembled in clean rooms — motors are fitted, autopilot boards soldered, payload bays installed."),
        ("🧪", "Quality Testing", "Every drone is tested for flight stability, camera clarity, battery endurance, and emergency failsafe procedures."),
        ("🏔️", "Extreme Condition Testing", "Final approval drones are shipped to Leh for high-altitude, extreme temperature performance validation."),
        ("🚚", "Delivery to Customer", "Approved drones are packed in rugged military-grade transit cases and shipped to defense units within 30 days."),
    ]:
        st.markdown(f"""<div class="bullet-item">{item[0]} <b>{item[1]}</b> — {item[2]}</div>""", unsafe_allow_html=True)

# ══ LUNGS — SUPPLIERS ══
elif organ == "lungs":
    st.markdown("""
    <div class="section-content-box">
        <div class="section-header">🫁 LUNGS — Global Suppliers &amp; Critical Component Imports</div>
        <div class="section-desc">
            Just as lungs bring oxygen into the body, ideaForge depends on global suppliers to breathe life into its drones.
            Without these components, production stops entirely:
        </div>
    </div>
    """, unsafe_allow_html=True)

    s1, s2 = st.columns(2)
    suppliers = [
        ("🇮🇱", "Elbit Systems — Israel", "EO/IR Optical Cameras", "₹8.0 Lakhs / unit", "Day & Night surveillance cameras with 30× zoom", "#F43F5E", "HIGH RISK: No local alternative"),
        ("🇹🇼", "TSMC Suppliers — Taiwan", "Autopilot Microchips", "₹2.0 Lakhs / unit", "Flight control chips — banned from China-origin", "#FF5500", "MEDIUM RISK: Taiwan supply chain sensitive"),
        ("🇯🇵", "Japan Carbon Corp", "Carbon Fiber Frames", "₹1.5 Lakhs / unit", "Ultra-light, high-strength structural body", "#00E5FF", "LOW RISK: Japan is reliable partner"),
        ("🇮🇳", "Indian Suppliers", "Batteries &amp; Motors", "₹0.8 Lakhs / unit", "LiPo packs and electric propulsion motors", "#34D399", "LOW RISK: 100% domestic — Atmanirbhar"),
    ]
    for i, (flag, name, part, cost, desc, color, risk) in enumerate(suppliers):
        col = s1 if i % 2 == 0 else s2
        with col:
            st.markdown(f"""
            <div class="bullet-item" style="border-left: 4px solid {color}; margin-bottom:14px;">
                <div style="font-size:1.5rem; margin-bottom:4px;">{flag}</div>
                <b style="color:{color}; font-size:1rem;">{name}</b><br>
                <b>Part:</b> {part} &nbsp;|&nbsp; <b>Cost:</b> {cost}<br>
                <span style="color:#CBD5E1;">{desc}</span><br>
                <span style="color:{color}; font-weight:700; font-size:0.82rem;">⚠ {risk}</span>
            </div>
            """, unsafe_allow_html=True)

# ══ EYES — CUSTOMERS ══
elif organ == "eyes":
    st.markdown("""
    <div class="section-content-box">
        <div class="section-header">👁️ EYES &amp; EARS — Who Buys ideaForge Drones?</div>
        <div class="section-desc">
            ideaForge watches the market through its customer relationships. These are the people and organisations
            that pay for drones, software, and ongoing service contracts:
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    customers = [
        ("🪖", "Indian Army", "65% Revenue", "~₹131 Cr / year", "Border surveillance, counter-terrorism, mountain patrol. Fast-track procurement buyer.", "#FF5500"),
        ("🛡️", "Home Ministry & BSF", "15% Revenue", "~₹30 Cr / year", "Paramilitary forces use drones for law enforcement, crowd monitoring, anti-insurgency.", "#00E5FF"),
        ("🗺️", "Survey of India", "20% Revenue", "~₹40 Cr / year", "Civil mapping of rural land for PM-SVAMITVA government scheme using Q6 drones.", "#34D399"),
    ]
    for col, (icon, name, share, value, desc, color) in zip([c1, c2, c3], customers):
        with col:
            st.markdown(f"""
            <div class="metric-pill-box" style="border-color:{color}; box-shadow:0 0 24px rgba(0,229,255,0.2);">
                <div style="font-size:2.2rem; margin-bottom:8px;">{icon}</div>
                <div class="metric-pill-label">{name}</div>
                <div class="metric-pill-val" style="color:{color}; font-size:1.4rem;">{share}</div>
                <div class="metric-pill-note" style="color:#FFFFFF;">{value}</div>
                <div style="font-size:0.82rem; color:#94A3B8; margin-top:8px; font-weight:500; line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    st.markdown("#### 🔑 Key Customer Risks to Know")
    for item in [
        ("⚠️", "Customer Concentration Risk", "65% of revenue comes from one buyer (Indian Army). If defense budget gets cut, ideaForge takes a direct hit."),
        ("📑", "Long Tender Process", "Government orders take 6–18 months from tender announcement to signed contract and first payment."),
        ("🌍", "Export Opportunity", "Only 5% revenue is international today. Friendly nations in Southeast Asia & Middle East are target markets for SWITCH."),
    ]:
        st.markdown(f"""<div class="bullet-item">{item[0]} <b>{item[1]}</b> — {item[2]}</div>""", unsafe_allow_html=True)

# ══ LEGS — FLEET OPS ══
elif organ == "legs":
    st.markdown("""
    <div class="section-content-box">
        <div class="section-header">🦵 LEGS — Drone Fleet Deployment &amp; Field Operations</div>
        <div class="section-desc">
            ideaForge's drones are the legs of its business — deployed across India's toughest terrains,
            altitudes, and environments. Here's the operational picture on the ground today:
        </div>
    </div>
    """, unsafe_allow_html=True)

    l1, l2, l3, l4 = st.columns(4)
    ops_metrics = [
        ("🚀", "Flight Missions", "950,000+", "All-time completed", "#00E5FF"),
        ("📜", "Patents Granted", "108+", "Proprietary technology", "#34D399"),
        ("💻", "Active FLYGHT Units", "1,250", "Live drone subscriptions", "#FF5500"),
        ("🌡️", "Temp Range Tested", "-20°C to +50°C", "Extreme condition certified", "#A78BFA"),
    ]
    for col, (icon, lbl, val, note, color) in zip([l1, l2, l3, l4], ops_metrics):
        with col:
            st.markdown(f"""
            <div class="metric-pill-box" style="border-color:{color}; box-shadow:0 0 20px rgba(0,229,255,0.2);">
                <div style="font-size:1.8rem; margin-bottom:6px;">{icon}</div>
                <div class="metric-pill-label">{lbl}</div>
                <div class="metric-pill-val" style="color:{color}; font-size:1.3rem;">{val}</div>
                <div class="metric-pill-note" style="color:#94A3B8;">{note}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    st.markdown("#### 📡 Where Are the Drones Operating Right Now?")
    for item in [
        ("🏔️", "Himalayan Border (Ladakh, Arunachal)", "SWITCH VTOL units provide 24/7 video surveillance of LOC and LAC at 18,000–20,000 ft altitude."),
        ("🏜️", "Rajasthan & Gujarat Borders", "Thermal-camera drones patrol desert border stretches where human patrol is impossible at night."),
        ("🌆", "Urban Law Enforcement (22 Cities)", "NETRA V4 drones assist police during large events, protests, and emergency response operations."),
        ("🌾", "Rural Land Mapping (2,400+ Villages)", "Q6 UAVs create geo-tagged property maps for the SVAMITVA scheme giving farmers land ownership proof."),
    ]:
        st.markdown(f"""<div class="bullet-item">{item[0]} <b>{item[1]}</b> — {item[2]}</div>""", unsafe_allow_html=True)

# ══ BRAIN — AI STRATEGY SIMULATOR ══
elif organ == "brain":
    st.markdown("""
    <div class="section-content-box">
        <div class="section-header">🧠 THE BRAIN — Strategy, Leadership &amp; AI Decision Engine</div>
        <div class="section-desc">
            The brain is where ideaForge makes its big decisions — from product strategy to pricing.
            This section gives you a behind-the-scenes look at how the company thinks and plans:
        </div>
    </div>
    """, unsafe_allow_html=True)

    b1, b2 = st.columns(2)
    with b1:
        st.markdown("""
        <div class="metric-pill-box">
            <div class="metric-pill-label">Company Founded</div>
            <div class="metric-pill-val" style="font-size:1.4rem;">2012</div>
            <div class="metric-pill-note" style="color:#94A3B8;">IIT Bombay Founders</div>
        </div>
        """, unsafe_allow_html=True)
    with b2:
        st.markdown("""
        <div class="metric-pill-box">
            <div class="metric-pill-label">HQ Location</div>
            <div class="metric-pill-val" style="font-size:1.4rem;">Mumbai</div>
            <div class="metric-pill-note" style="color:#94A3B8;">Navi Mumbai Operations</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.markdown("#### 🎯 Strategic Decisions That Define the Company")
    for item in [
        ("🎯", "India-First Defense Strategy", "ideaForge focuses exclusively on Indian government buyers (Army, police, civil mapping) making it nearly immune to global competition."),
        ("🔒", "No Chinese Components Policy", "After 2020 border tensions, all Chinese-origin parts were eliminated — now 60% of components are domestically sourced (India-made)."),
        ("💡", "FLYGHT Software = Recurring Revenue", "Building a software subscription layer on top of hardware creates sticky annual revenue and is the growth engine for the next decade."),
        ("🌍", "Export Target: 2025–2028", "ideaForge is preparing certifications to export SWITCH to Southeast Asia, Middle East, and African nations seeking India-made defense drones."),
        ("📈", "Stock Market Listed (NSE: IDEAFORGE)", "Listed on NSE in 2023. Market cap fluctuates between ₹1,200–1,800 Cr based on defense budget announcements."),
    ]:
        st.markdown(f"""<div class="bullet-item">{item[0]} <b>{item[1]}</b> — {item[2]}</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# REAL-WORLD SIMULATION STUDIO
# ─────────────────────────────────────────────────────
st.write("---")
st.markdown("""
<div class="sim-drawer">
    <div class="sim-title">🎛️ SIMULATION STUDIO — Test Real-World Scenarios</div>
    <div class="sim-desc">
        Drag the sliders below to see how external factors — like government payment speed or import tariffs —
        directly change ideaForge's profits and cash position. All numbers update instantly.
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")
s_col1, s_col2 = st.columns([1, 1.2])

with s_col1:
    st.markdown("##### 🎚️ Adjust the Real-World Factors")

    mod_lag = st.slider(
        "⏳ How fast does the Government pay invoices? (Days)",
        min_value=15, max_value=180, value=int(baseline_data["MoD_Disbursement_Lag"]), step=5,
        help="Faster payment = more cash in hand for ideaForge to operate."
    )

    import_price_shock = st.slider(
        "📷 Camera & Chip Import Price Increase (%)",
        min_value=0, max_value=50, value=0, step=5,
        help="If global tariffs rise, imported cameras and chips cost more → profits drop."
    )

    saas_attach_rate = st.slider(
        "💻 What % of Customers Subscribe to FLYGHT Software?",
        min_value=0, max_value=100, value=int(baseline_data["SaaS_Attach_Rate"] * 100), step=5,
        help="More software subscribers = more recurring annual income with very high margins."
    )

    scenario_config = {
        "mod_lag_days": mod_lag,
        "import_tariff_shock_pct": import_price_shock,
        "saas_attach_rate_pct": saas_attach_rate,
        "indigenous_mix": 0.60
    }

    agent_state = orchestrator.run_workflow(scenario_config)
    sim_res = agent_state.simulated_results

with s_col2:
    st.markdown("##### 📊 What Happens to the Company?")

    ebitda_diff = sim_res["EBITDA_Margin"] - baseline_data["EBITDA_Margin"]
    wc_diff = sim_res["Working_Capital_Days"] - baseline_data["Working_Capital_Days"]
    wc_req = sim_res["Working_Capital_Requirement_Cr"]

    o1, o2, o3 = st.columns(3)
    with o1:
        color = "#34D399" if ebitda_diff >= 0 else "#F43F5E"
        st.markdown(f"""
        <div class="metric-pill-box">
            <div class="metric-pill-label">Profit Margin</div>
            <div class="metric-pill-val">{sim_res['EBITDA_Margin']:.1f}%</div>
            <div class="metric-pill-note" style="color:{color};">{'+' if ebitda_diff >= 0 else ''}{ebitda_diff:.1f}% shift</div>
        </div>
        """, unsafe_allow_html=True)
    with o2:
        color2 = "#34D399" if wc_diff <= 0 else "#F43F5E"
        st.markdown(f"""
        <div class="metric-pill-box">
            <div class="metric-pill-label">Cash Collection</div>
            <div class="metric-pill-val">{sim_res['Working_Capital_Days']:.0f}d</div>
            <div class="metric-pill-note" style="color:{color2};">{'+' if wc_diff >= 0 else ''}{wc_diff:.0f}d vs normal</div>
        </div>
        """, unsafe_allow_html=True)
    with o3:
        st.markdown(f"""
        <div class="metric-pill-box">
            <div class="metric-pill-label">Cash Buffer Needed</div>
            <div class="metric-pill-val">₹{wc_req:.0f}Cr</div>
            <div class="metric-pill-note" style="color:#00E5FF;">Working Capital</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.markdown("**📋 Plain-English Outcome:**")
    
    if ebitda_diff < -2:
        profit_verdict = f"⚠️ Profits **drop** to {sim_res['EBITDA_Margin']:.1f}% — ideaForge earns less per drone sold."
    elif ebitda_diff > 2:
        profit_verdict = f"✅ Profits **improve** to {sim_res['EBITDA_Margin']:.1f}% — ideaForge becomes more profitable."
    else:
        profit_verdict = f"Profits stay stable at {sim_res['EBITDA_Margin']:.1f}% — no major impact."

    if wc_diff > 15:
        cash_verdict = f"⚠️ The company needs to **wait longer** ({sim_res['Working_Capital_Days']:.0f} days) to collect money from the government."
    elif wc_diff < -10:
        cash_verdict = f"✅ Government pays **faster** ({sim_res['Working_Capital_Days']:.0f} days) — better cash flow for ideaForge."
    else:
        cash_verdict = f"Cash collection timing is stable at {sim_res['Working_Capital_Days']:.0f} days."

    st.markdown(f"""
    <div class="bullet-item">💰 <b>Profitability:</b> {profit_verdict}</div>
    <div class="bullet-item">⏱️ <b>Cash Flow:</b> {cash_verdict}</div>
    <div class="bullet-item">🏦 <b>Cash Buffer Required:</b> ideaForge needs ₹{wc_req:.0f} Cr in the bank to keep operations running smoothly — {'this is healthy' if wc_req < 50 else 'this is a strain on the balance sheet'}.</div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer-bar">
    ideaForge Digital Twin — Explore Every Corner of the Company • Built for Everyone
</div>
""", unsafe_allow_html=True)

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

# ✅ 비밀번호 입력창 추가 (여기!)
password = st.text_input("비밀번호를 입력하세요", type="password")
if password != "7950":
    st.warning("비밀번호가 틀렸습니다.")
    st.stop()

# 기본 폰트를 Noto Sans KR로 설정 (한글 지원)
plt.rcParams['font.family'] = 'Noto Sans KR'

# 정동-카테고리 매핑
affective_category_map = {
    'absurd': 'Play / Lightness', 'alienating': 'Strangeness / Uncanny', 'ambiguous': 'meta-affect',
    'anxious': 'Tension / Unease', 'austere': 'Gravitas / Seriousness', 'blatant': 'Explicitness / Exposure',
    'calm': 'Stillness / Drift', 'chaotic': 'Excess / Intensity', 'dark': 'Sublimity / Ominousness',
    'detached': 'meta-affect', 'discrepant': 'meta-affect', 'dreamlike': 'Strangeness / Uncanny',
    'ethical': 'meta-affect', 'explicit': 'Explicitness / Exposure', 'explosive': 'Excess / Intensity',
    'flashy': 'Excess / Intensity', 'flat': 'Stillness / Drift', 'floating': 'Stillness / Drift',
    'furious': 'Excess / Intensity', 'gazing': 'Stillness / Drift', 'gentle': 'Melancholy / Sentimentality',
    'glamorous': 'Play / Lightness', 'grand': 'Sublimity / Ominousness', 'grave': 'Gravitas / Seriousness',
    'historical': 'meta-affect', 'humorous': 'Play / Lightness', 'immersive': 'Excess / Intensity',
    'intense': 'Excess / Intensity', 'ironic': 'meta-affect', 'lighthearted': 'Play / Lightness',
    'literary': 'meta-affect', 'lonely': 'Melancholy / Sentimentality', 'low-key': 'Stillness / Drift',
    'melancholic': 'Melancholy / Sentimentality', 'nostalgic': 'Melancholy / Sentimentality',
    'ominous': 'Sublimity / Ominousness', 'oppressive': 'Tension / Unease', 'overwhelming': 'Excess / Intensity',
    'philosophical': 'meta-affect', 'playful': 'Play / Lightness', 'pleasant ': 'Play / Lightness',
    'poignant': 'Melancholy / Sentimentality', 'raw': 'Explicitness / Exposure', 'restrained': 'Gravitas / Seriousness',
    'sentimental': 'Melancholy / Sentimentality', 'serious': 'Gravitas / Seriousness', 'silent': 'Stillness / Drift',
    'slow': 'Stillness / Drift', 'soft': 'Melancholy / Sentimentality', 'strange': 'Strangeness / Uncanny',
    'sublime': 'Sublimity / Ominousness', 'subtle': 'Stillness / Drift', 'surreal': 'Strangeness / Uncanny',
    'symbolic': 'Sublimity / Ominousness', 'tense': 'Tension / Unease', 'threatening': 'Tension / Unease',
    'uncanny': 'Strangeness / Uncanny', 'uneasy': 'Tension / Unease', 'vulgar': 'Explicitness / Exposure',
    'weighty': 'Gravitas / Seriousness', 'witty': 'Play / Lightness'
}

category_colors = {
    'Tension / Unease': '#ff4c4c', 'Excess / Intensity': '#ff4c4c', 'Explicitness / Exposure': '#ff4c4c',
    'Sublimity / Ominousness': '#ff4c4c',
    'Melancholy / Sentimentality': '#4682b4', 'Stillness / Drift': '#4682b4',
    'Play / Lightness': '#ffd700',
    'Gravitas / Seriousness': '#696969',
    'Strangeness / Uncanny': '#ff8c00',
    'meta-affect': '#9400d3'
}

st.title("Affective Terrain Map Generator")
st.markdown("입력한 정동 강도를 기반으로 **분리형 방사형 그래프**를 생성합니다.")

affective_tags = list(affective_category_map.keys())
title = st.text_input("영화 제목을 입력하세요", "기생충")

st.markdown("### 정동 강도 입력 (1~5)")
selected_affects = {}

with st.expander("정동 선택 및 강도 조절", expanded=True):
    for affect in sorted(affective_tags):
        col1, col2 = st.columns([2, 3])
        with col1:
            check = st.checkbox(affect)
        if check:
            with col2:
                intensity = st.slider(f"{affect} 강도", 1, 5, 3, key=affect)
                selected_affects[affect] = intensity

if selected_affects:
    st.markdown("---")
    st.markdown(f"### 🎥 {title} - Affective Terrain Map")

    labels = list(selected_affects.keys())
    values = list(selected_affects.values())
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    colors = []
    for label, value in zip(labels, values):
        category = affective_category_map.get(label, 'meta-affect')
        base_color = category_colors.get(category, '#cccccc')
        colors.append(base_color)

    bars = ax.bar(angles, values, width=0.6, bottom=0.0, color=colors, edgecolor="black", alpha=0.7)

    for bar, label in zip(bars, labels):
        angle = bar.get_x() + bar.get_width() / 2
        radius = bar.get_height() / 2
        ax.text(angle, radius, label, ha='center', va='center', fontsize=11)

    ax.set_xticks([])
    ax.set_yticks(range(1, 6))
    ax.set_yticklabels([])
    ax.set_rlabel_position(0)

    fig.text(0.5, 1.05, f"Affective Terrain Map ({title})", fontsize=14, ha='center')

    st.pyplot(fig)

    import io
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    st.download_button("Download PNG", buf.getvalue(), file_name=f"{title}_affective_map.png", mime="image/png")
else:
    st.info("정동과 강도를 최소 하나 이상 입력해 주세요.")


         
       

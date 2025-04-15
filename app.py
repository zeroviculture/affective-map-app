import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Define affective descriptors
affective_tags = [
    'uneasy', 'tense', 'threatening', 'oppressive', 'anxious', 'melancholic', 'poignant',
    'sentimental', 'lonely', 'nostalgic', 'gentle', 'soft', 'intense', 'explosive',
    'immersive', 'overwhelming', 'furious', 'chaotic', 'flashy', 'explicit', 'ironic'
]

st.title("Affective Terrain Map Generator")
st.markdown("입력한 정동 강도를 기반으로 **분리형 방사형 그래프**를 생성합니다.")

title = st.text_input("영화 제목을 입력하세요", "기생충")

st.markdown("### 정동 강도 입력 (1~5)")
selected_affects = {}

cols = st.columns(2)
for i, affect in enumerate(affective_tags):
    with cols[i % 2]:
        intensity = st.slider(f"{affect}", 0, 5, 0)
        if intensity > 0:
            selected_affects[affect] = intensity

if selected_affects:
    st.markdown("---")
    st.markdown(f"### 🎥 {title} - Affective Terrain Map")

    labels = list(selected_affects.keys())
    values = list(selected_affects.values())
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    bars = ax.bar(angles, values, width=0.6, bottom=0.0, color="plum", edgecolor="black", alpha=0.7)

    for bar, label in zip(bars, labels):
        angle = bar.get_x() + bar.get_width() / 2
        radius = bar.get_height() / 2
        ax.text(angle, radius, label, ha='center', va='center', fontsize=11)

    ax.set_xticks([])
    ax.set_yticklabels([])
    ax.set_title(f"Affective Terrain Map ({title})", fontsize=14, pad=20)
    st.pyplot(fig)

    import io
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    st.download_button("Download PNG", buf.getvalue(), file_name=f"{title}_affective_map.png", mime="image/png")
else:
    st.info("정동과 강도를 최소 하나 이상 입력해 주세요.")

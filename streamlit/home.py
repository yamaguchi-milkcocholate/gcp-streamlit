import streamlit as st

st.title(":hammer_and_wrench: Streamlit Playground")

st.page_link(
    "pages/linedraw.py",
    label="塗り絵作成",
    icon="🔥",
    use_container_width=True,
    help="画像の線画を作成するアプリです",
)

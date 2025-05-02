from pathlib import Path

import yaml
from src.gemini import LineDrawGenerationLifecycle
from src.utils import decode_base64_to_image, encode_image_to_base64
from streamlit_image_select import image_select

import streamlit as st

# テーマ選択
thema_dir = Path(__file__).parent.parent / "thema"
with open(thema_dir / "config.yaml", "r") as f:
    themes = yaml.safe_load(f)["theme"]
for i_theme in range(len(themes)):
    themes[i_theme]["base64"] = encode_image_to_base64(
        image_path=thema_dir / themes[i_theme]["image"]
    )


theme_index = image_select(
    "テーマを選択してください",
    [thema_dir / theme["image"] for theme in themes],
    return_value="index",
)
selected_theme = themes[theme_index]
st.write(theme_index)

# 画像アップロード
uploaded_file = st.file_uploader(
    "画像をアップロードしてください", type=["jpg", "jpeg", "png"]
)

# 実行
if "run_button" in st.session_state and st.session_state.run_button:
    st.session_state.running = True
else:
    st.session_state.running = False
debug = True
if st.button("実行", disabled=st.session_state.running, key="run_button"):
    if uploaded_file is not None or debug:
        with st.spinner(text="画像を作成しています...", show_time=False):
            # 画像を保存
            image_dir = Path(__file__).parent.parent / "images"
            image_filepath = image_dir / "pokemon.png"
            # with open(image_dir / "uploaded_image.jpg", "wb") as f:
            #     f.write(uploaded_file.getbuffer())
            # st.success("画像を保存しました")

            base64_string = encode_image_to_base64(image_path=image_filepath)

            result = LineDrawGenerationLifecycle(target_base64=base64_string).run()

            first_phase = decode_base64_to_image(base64_string=result["first_phase"])
            add_color = decode_base64_to_image(base64_string=result["add_color"])
            st.image(first_phase, caption="1st", use_container_width=True)
            st.image(add_color, caption="add color", use_container_width=True)

            # img_data = debode_base64_to_image(base64_string=base64_string)
            # st.image(img_data, caption="Uploaded Image", use_container_width=True)
    else:
        st.error("画像がアップロードされていません")

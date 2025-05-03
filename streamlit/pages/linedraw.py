import shutil
import zipfile
from pathlib import Path

import yaml
from src.gemini import GeminiException, LineDrawGenerationLifecycle
from src.opencv import cv_line_draw
from src.utils import (
    base64_to_image_file,
    embed_base64_to_image,
    encode_image_to_base64,
)
from streamlit_image_select import image_select

import streamlit as st

image_dir = Path(__file__).parent.parent / "images"
thema_dir = Path(__file__).parent.parent / "thema"
uploaded_filepath = image_dir / "uploaded_image.jpg"
output_line_draw_filepath = image_dir / "output_line_draw.jpg"
output_color_filepath = image_dir / "output_color.jpg"

OUTPUT_IMAGE_WIDTH = 300


def process_gemini() -> None:
    base64_string = encode_image_to_base64(image_path=uploaded_filepath)

    result = LineDrawGenerationLifecycle(target_base64=base64_string).run()

    line_draw_base64 = result["first_phase"]
    color_base64 = result["add_color"]

    base64_to_image_file(
        base64_string=line_draw_base64, output_path=output_line_draw_filepath
    )
    base64_to_image_file(base64_string=color_base64, output_path=output_color_filepath)

    line_draw_base64 = embed_base64_to_image(base64_string=line_draw_base64)
    color_base64 = embed_base64_to_image(base64_string=color_base64)

    output_col1, output_col2 = st.columns(2)
    with output_col1:
        st.image(line_draw_base64, caption="線画", width=OUTPUT_IMAGE_WIDTH)
    with output_col2:
        st.image(color_base64, caption="カラー", width=OUTPUT_IMAGE_WIDTH)


def process_cv2() -> None:
    cv_line_draw(
        from_filepath=uploaded_filepath,
        to_filepath=output_line_draw_filepath,
        num_dilate_iter=1,
    )

    line_draw_base64 = encode_image_to_base64(
        image_path=output_line_draw_filepath, embed=False
    )
    color_base64 = encode_image_to_base64(image_path=uploaded_filepath, embed=False)

    base64_to_image_file(
        base64_string=line_draw_base64, output_path=output_line_draw_filepath
    )
    base64_to_image_file(base64_string=color_base64, output_path=output_color_filepath)

    line_draw_base64 = embed_base64_to_image(base64_string=line_draw_base64)
    color_base64 = embed_base64_to_image(base64_string=color_base64)

    output_col1, output_col2 = st.columns(2)
    with output_col1:
        st.image(line_draw_base64, caption="線画", width=OUTPUT_IMAGE_WIDTH)
    with output_col2:
        st.image(color_base64, caption="カラー", width=OUTPUT_IMAGE_WIDTH)


st.header("加工方法の選択")
st.text(
    "線画にしたい画像に合わせて加工方法を選択してください。\n"
    + "アニメなどの画像は「イラスト」を、実写の画像は「リアル」を選択するとうまく線画になりやすいです。"
)


# 加工方法の選択
with open(thema_dir / "config.yaml", "r") as f:
    themes = yaml.safe_load(f)["theme"]
theme_index = image_select(
    "加工方法を選択してください",
    [str(thema_dir / theme["image_dir"] / "org.jpg") for theme in themes],
    captions=[theme["caption"] for theme in themes],
    return_value="index",
)
selected_theme = themes[theme_index]


st.subheader("仕上がりの例")
output_col1, output_col2 = st.columns(2)
for output_type, output_name, output_col in zip(
    ["prop", "color"], ["線画", "カラー"], [output_col1, output_col2]
):
    selected_theme_filepath = (
        thema_dir / selected_theme["image_dir"] / f"{output_type}.jpg"
    )
    selected_theme_bae64 = encode_image_to_base64(
        image_path=selected_theme_filepath, embed=True
    )
    with output_col:
        st.image(selected_theme_bae64, caption=output_name, width=OUTPUT_IMAGE_WIDTH)


# 画像のアップロード
def clear_file():
    if output_line_draw_filepath.exists():
        output_line_draw_filepath.unlink()
    if output_color_filepath.exists():
        output_color_filepath.unlink()


uploaded_file = st.file_uploader(
    "画像をアップロード", type=["jpg", "jpeg", "png"], on_change=clear_file
)
if uploaded_file is not None:
    with open(uploaded_filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("アップロードに成功しました", icon="✅")
    uploaded_base64 = encode_image_to_base64(image_path=uploaded_filepath, embed=True)
    st.image(uploaded_base64, width=300)


# 実行
if selected_theme["caption"] == "リアル":
    st.caption(
        "「リアル」の処理が失敗した時は何回か試してみてください。\n"
        + "それでも失敗する場合は管理者に連絡してください。",
    )
if "run_button" in st.session_state and st.session_state.run_button:
    st.session_state.running = True
else:
    st.session_state.running = False
disable_run = st.session_state.running or (uploaded_file is None)
if st.button(
    "実行",
    help="画像をアップロードしてから実行してください",
    disabled=disable_run,
    key="run_button",
):
    if uploaded_file is not None:
        with st.spinner(text="画像を作成しています...", show_time=False):
            try:
                if selected_theme["caption"] == "イラスト":
                    process_cv2()
                elif selected_theme["caption"] == "リアル":
                    process_gemini()
                else:
                    st.error("選択された加工方法は無効です", icon="🚨")
            except GeminiException:
                st.error(
                    "「リアル」の処理に失敗しました。もう一度試してみてください。\nそれでも失敗する場合は管理者に連絡してください。",
                    icon="🚨",
                )

    else:
        st.error("画像がアップロードされていません", icon="🚨")
    st.session_state.running = False

if output_line_draw_filepath.exists() and output_color_filepath.exists():
    zip_dirpath = output_line_draw_filepath.parent / "archive"
    zip_dirpath.mkdir(exist_ok=True, parents=True)
    zip_filepath = output_line_draw_filepath.parent / "archive.zip"

    zip_line_draw_filepath = zip_dirpath / output_line_draw_filepath.name
    zip_color_filepath = zip_dirpath / output_color_filepath.name
    shutil.copy(output_line_draw_filepath, zip_line_draw_filepath)
    shutil.copy(output_color_filepath, zip_color_filepath)

    with zipfile.ZipFile(zip_filepath, "w") as zf:
        zf.write(zip_line_draw_filepath, arcname=zip_line_draw_filepath.name)
        zf.write(zip_color_filepath, arcname=zip_color_filepath.name)

    with open(zip_filepath, "rb") as file:
        st.download_button(
            label="Download",
            data=file,
            file_name="archive.zip",
            mime="application/zip",
        )

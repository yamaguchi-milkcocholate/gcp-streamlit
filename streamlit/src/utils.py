import base64
import io
from pathlib import Path

from PIL import Image


def encode_image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as image_file:
        # 画像をバイナリとして読み込み、Base64 にエンコード
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string


def decode_base64_to_image(base64_string: str) -> Image:
    image = Image.open(io.BytesIO(base64.decodebytes(bytes(base64_string, "utf-8"))))
    return image

    # with open(output_path, "wb") as image_file:
    #     image_file.write(base64.b64decode(base64_string))

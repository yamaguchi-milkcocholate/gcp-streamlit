import base64
import io
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageFile


def encode_image_to_base64(image_path: Path, embed: bool = False) -> str:
    with open(image_path, "rb") as image_file:
        # 画像をバイナリとして読み込み、Base64 にエンコード
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

    if embed:
        encoded_string = embed_base64_to_image(encoded_string)
    return encoded_string


def decode_base64_to_image(base64_string: str) -> ImageFile.ImageFile:
    image = Image.open(io.BytesIO(base64.decodebytes(bytes(base64_string, "utf-8"))))
    return image


def embed_base64_to_image(base64_string: str) -> str:
    return f"data:image/jpeg;base64, {base64_string}"


def base64_to_image_file(base64_string: str, output_path: Path) -> None:
    # バイナリデータ <- base64でエンコードされたデータ
    img_binary = base64.b64decode(base64_string)
    jpg = np.frombuffer(img_binary, dtype=np.uint8)

    # raw image <- jpg
    img = cv2.imdecode(jpg, cv2.IMREAD_COLOR)
    # 画像を保存する場合
    cv2.imwrite(output_path, img)

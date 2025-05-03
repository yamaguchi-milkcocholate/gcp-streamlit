from pathlib import Path

import cv2
import numpy as np


def cv_line_draw(from_filepath: Path, to_filepath: Path, num_dilate_iter: int) -> None:
    neiborhood8 = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], np.uint8)
    # 2値化して読み込む
    img = cv2.imread(from_filepath, 0)
    # 膨張してから差分を取り線画を作成
    img_dilate = cv2.dilate(img, neiborhood8, iterations=num_dilate_iter)
    img_diff = cv2.absdiff(img, img_dilate)
    img_diff_not = cv2.bitwise_not(img_diff)
    cv2.imwrite(to_filepath, img_diff_not)

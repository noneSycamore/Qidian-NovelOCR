"""
OCR the screenshot and reconstruct the result.
"""

from PIL import Image
import pytesseract
import re
from paddleocr import PaddleOCR
import numpy as np

# pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'
ocr = PaddleOCR(lang="ch")


def reconstruct_paragraphs_tesseract(ocr_text):
    """
    Automatically merge incorrect line feeds in OCR results that should belong to the same paragraph
    (Tesseract version)
    :param ocr_text: OCR text
    """
    lines = ocr_text.splitlines()
    paragraphs = []  # restore paragraphs
    temp_paragraph = ""

    # Handling of line breaks in the same paragraph
    for line in lines:
        line = line.strip()
        # A blank line, it means the end of the paragraph
        if not line:
            if temp_paragraph:
                paragraphs.append(temp_paragraph)
                temp_paragraph = ""
            continue
        # If not blank, add current line to the temporary paragraph
        temp_paragraph += line
    # Add the last paragraph
    if temp_paragraph:
        paragraphs.append(temp_paragraph)

    # Reconnect the paragraphs that are incorrectly split, through regular expressions
    i = 0
    while i < len(paragraphs):
        # If the last character of the paragraph is not a punctuation mark
        if not (re.search(r'[，。！？…：；“”,.!?:;"]', paragraphs[i][-1])):
            paragraphs[i] += paragraphs.pop(i + 1)
        else:
            i += 1

    return "\n\n".join(paragraphs)


def ocr_image_tesseract(image_path):
    """
    [Tesseract] OCR the image and return the text
    :param image_path: path to the image
    :return: OCR text
    """
    config = '--oem 3 --psm 6'
    with Image.open(image_path) as image:
        text = pytesseract.image_to_string(image, lang='chi_sim', config=config)
    return text


def ocr_image_paddle(image_path):
    """
    [PaddleOCR] OCR the image and return the text
    :param image_path: path to the image
    :return: OCR text
    """
    result = ocr.ocr(image_path, cls=False)
    # 提取行文本和位置坐标 (Y 轴)
    lines = []
    for line in result[0]:
        position = line[0]
        y_coordinate = np.mean([p[1] for p in position])
        text = line[1][0]
        lines.append((y_coordinate, text.strip()))

    # 按 Y 坐标排序，确保从上到下的顺序
    lines.sort(key=lambda x: x[0])

    # 根据行间距分段
    paragraphs = []
    current_paragraph = [lines[0][1]]

    for i in range(1, len(lines)):
        y_diff = lines[i][0] - lines[i - 1][0]  # 计算当前行与上一行的间距
        # print(y_diff)  # 调试用, 需要自行判断阈值
        if y_diff > 70:
            # 如果行间距超过阈值，视为新段落
            paragraphs.append("".join(current_paragraph))
            current_paragraph = [lines[i][1]]
        else:
            # 否则合并为同一段落
            current_paragraph.append(lines[i][1])

    # 添加最后一个段落
    if current_paragraph:
        paragraphs.append("".join(current_paragraph))

    # 返回重建后的文本，段落之间以换行分隔
    return "\n\n".join(paragraphs)


def output_result(ocr_text, output_path):
    """
    Output the OCR result to a txt file
    :param ocr_text: OCR text
    :param output_path: path to the output file
    """
    with open(output_path, "a", encoding="utf-8") as f:
        f.write(ocr_text)
        f.write("\n\n")

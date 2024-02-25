import base64
import os
import re
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT_DIR, "src")
INDEX_FILE = os.path.join(SRC_DIR, "index.html")
DST_DIR = os.path.join(ROOT_DIR, "build")
OUTPUT_FILE = os.path.join(DST_DIR, 'index.html')


def read_html(filepath) -> str:
    """读取html"""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    # 匹配形如 {{{{foo}}}} 的文本
    pattern = r'\{\{\{\{(.+?)\}\}\}\}'
    matches = re.findall(pattern, text)

    # 对于每一个匹配，调用func函数获取映射内容，并替换原文本
    for match in matches:
        mapped_val = get_result_file(match)  # 调用func函数
        text = text.replace("{{{{" + match + "}}}}", mapped_val)  # 替换文本

    return text


def read_png(filepath: str):
    """将png图像变为base64 uri"""
    with open(filepath, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    base64_uri = f'data:image/png;base64,{encoded_string}'
    return base64_uri


def get_result_file(filepath: str):
    assert isinstance(filepath, str)
    assert os.path.exists(filepath)

    fp = filepath.replace("\\", '/')
    assert fp.rindex(".") > (fp.rindex("/") if '/' in fp else -1)
    file_type = fp[fp.rindex(".") + 1:].lower()

    if file_type == 'png':
        return read_png(filepath)
    elif file_type == 'html':
        return read_html(filepath)
    else:
        raise RuntimeError(f"Unknown file: {filepath}")


if __name__ == "__main__":
    print("ROOT_DIR", ROOT_DIR)
    print("SRC_DIR", SRC_DIR)
    print("INDEX_FILE", INDEX_FILE)
    print("DST_DIR", DST_DIR)
    print("OUTPUT_FILE", OUTPUT_FILE)
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w+', encoding='utf-8') as f:
        f.write(get_result_file(INDEX_FILE))
else:
    raise ValueError("Can not import entry: build")

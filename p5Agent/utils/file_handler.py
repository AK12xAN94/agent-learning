import os,hashlib
from .logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader

# 获取文件的md5十六进制字符串的值
def get_file_md5_hex(file_path: str) -> str:
    if not os.path.exists(file_path):
        logger.error(f"[md5计算]文件{file_path}不存在")
        return
    if not os.path.isfile(file_path):
        logger.error(f"[md5计算]文件{file_path}不是文件")
        return

    md5_obj = hashlib.md5()

    chunk_size = 4096 # 4KB
    
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)
            return md5_obj.hexdigest()
    except Exception as e:
        logger.error(f"[md5计算]文件{file_path}读取失败: {e}")
        return None

# 返回文件夹内的文件列表（允许的文件后缀）
def listdir_with_allowed_type(
    path: str, allowed_types: tuple[str] = ["txt", "md"]
) -> list[str]:
    files = []

    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]路径{path}不是文件夹")
        return allowed_types
    for file in os.listdir(path):
        if file.endswith(allowed_types):
            files.append(os.path.join(path, file))
    return tuple(files)

def pdf_loader(file_path: str) -> list[Document]:
    loader = PyPDFLoader(
        file_path=file_path,
        encoding="utf-8",
    )
    return loader.load()

def txt_loader(file_path: str) -> list[Document]:
    loader = TextLoader(
        file_path=file_path,
        encoding="utf-8",
    )
    return loader.load()

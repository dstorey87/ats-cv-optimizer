import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logger(log_file: str, level: str = "INFO", rotate_mb: int = 5):
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("ats_app")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    handler = RotatingFileHandler(log_file, maxBytes=rotate_mb*1024*1024, backupCount=3, encoding="utf-8")
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    handler.setFormatter(fmt)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger

def read_docx_text(path):
    try:
        from docx import Document
    except Exception as e:
        raise RuntimeError("python-docx is required to read .docx files. Install with: pip install python-docx") from e
    d = Document(path)
    return "\n".join(p.text for p in d.paragraphs)

def read_text_flexible(path):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")
    if p.suffix.lower() == ".docx":
        return read_docx_text(p)
    # For PDFs: advise converting to .txt for accuracy
    return p.read_text(encoding="utf-8", errors="ignore")
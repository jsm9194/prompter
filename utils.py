from rapidfuzz import fuzz
import re

def normalize_text(s: str) -> str:
    s = s.strip()
    s = re.sub(r"\s+", " ", s)
    return s

def similarity(a: str, b: str) -> float:
    a = normalize_text(a)
    b = normalize_text(b)
    return fuzz.partial_ratio(a, b) / 100.0

from functools import lru_cache

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.config import POLICY_PATH, TOP_K

def _split_sections(text: str) -> list[str]:
    blocks = [block.strip() for block in text.split("\n\n") if block.strip()]
    chunks = []
    current = []

    for block in blocks:
        if block.startswith("## ") and current:
            chunks.append("\n\n".join(current))
            current = [block]
        else:
            current.append(block)

    if current:
        chunks.append("\n\n".join(current))

    return chunks

@lru_cache(maxsize=1)
def _build_index():
    text = POLICY_PATH.read_text(encoding="utf-8")
    chunks = _split_sections(text)

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
    )
    matrix = vectorizer.fit_transform(chunks)
    return chunks, vectorizer, matrix

def search_policy(query: str, top_k: int = TOP_K) -> list[dict]:
    chunks, vectorizer, matrix = _build_index()
    query_vector = vectorizer.transform([query])
    scores = cosine_similarity(query_vector, matrix).ravel()
    order = scores.argsort()[::-1][:top_k]

    results = []
    for index in order:
        if scores[index] <= 0:
            continue

        results.append({
            "text": chunks[index],
            "score": round(float(scores[index]), 4),
        })

    return results

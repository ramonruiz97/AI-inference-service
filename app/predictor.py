from typing import List, Tuple, Dict
from .models import Prediction

_ORDER: Dict[str, int] = {"POSITIVE": 0, "NEUTRAL": 1, "NEGATIVE": 2}

def predict_dummy(texts: List[str], top_k: int) -> List[List[dict]]:
    results: List[List[Prediction]] = []
    for text in texts:
        t = text.lower()
        candidates: List[Tuple[str, float]] = []
        if "good" in t:
            candidates.append(("POSITIVE", 0.9))
        if "bad" in t:
            candidates.append(("NEGATIVE", 0.9))
        if not candidates:
            candidates.append(("NEUTRAL", 0.5))
        
        candidates.sort(key=lambda x: (-x[1], _ORDER[x[0]]))
        k = max(1, min(top_k, len(candidates)))
        results.append([Prediction(label=label, score=score) for label, score in candidates[:k]])

    return results 






  
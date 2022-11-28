import numpy as np

def normalization(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm
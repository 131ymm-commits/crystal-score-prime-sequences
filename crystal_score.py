import numpy as np

def crystal_score(sequence, num_states=8):
    """
    Compute Crystal Score λ₂/λ₁ for a sequence of numbers.
    
    Parameters
    ----------
    sequence : list or numpy array of numbers
        The numerical sequence (must be at least 100 elements).
    num_states : int, default=8
        Number of quantization states for gaps.
        
    Returns
    -------
    float
        Crystal Score (second eigenvalue / first eigenvalue),
        or NaN if sequence is too short.
    """
    if len(sequence) < 100:
        return np.nan
    
    gaps = np.diff(sequence)
    
    # Quantize gaps by percentiles
    try:
        percentiles = np.percentile(gaps, np.linspace(0, 100, num_states + 1)[1:-1])
        quant = np.digitize(gaps, percentiles)
    except Exception:
        return np.nan
    
    # Transition matrix
    T = np.zeros((num_states, num_states))
    for i in range(len(quant) - 1):
        T[quant[i], quant[i+1]] += 1
    
    # Row normalisation
    row_sums = T.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    T_norm = T / row_sums
    
    # Eigenvalues
    eigvals = np.linalg.eigvals(T_norm)
    eig_abs = np.sort(np.abs(eigvals))[::-1]
    
    if eig_abs[0] < 1e-12:
        return 0.0
    return eig_abs[1] / eig_abs[0]

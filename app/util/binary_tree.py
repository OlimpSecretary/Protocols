def bitrev_sequence(N):
    """
    Return list of length N containing the 1-based bit-reversal permutation.
    N must be a power of two.
    """
    import math
    if N & (N-1) != 0:
        raise ValueError("N must be a power of two")
    b = int(math.log2(N))
    seq = []
    for i in range(N):               # i is 0-based index
        x = 0
        v = i
        for _ in range(b):
            x = (x << 1) | (v & 1)
            v >>= 1
        seq.append(x + 1)           # convert to 1-based
    return seq

# Examples
print(bitrev_sequence(2))
print(bitrev_sequence(8))
print(bitrev_sequence(16))
print(bitrev_sequence(32))
print(bitrev_sequence(64))   # uncomment to get 64-term list
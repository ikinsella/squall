import time


def fibonnacci(N):
    """Recursively computed the Nth number in the fibonnacci sequence"""
    assert N >= 0, "N must be a positive integer"
    if (N is 0 or N is 1):
        return N
    else:
        return fibonnacci(N-2) + fibonnacci(N-1)


def fib_prod(A, B):
    """Computes the product of the two fibonnacci numbers A and B"""
    t0 = time.time()
    fibA = fibonnacci(A)
    tA = time.time()
    fibB = fibonnacci(B)
    tB = time.time()
    return (fibA * fibB, fibA, fibB, tA-t0, tB-tA)

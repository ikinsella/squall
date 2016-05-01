#!/usr/bin/env RScript

fibonacci <- function(N) {
  if (N < 0) {
    warning("N must be a non-negative integer!")
  } else if (N == 0 || N == 1) {
    return (N)
  } else {
    return (fibonacci(N - 2) + fibonacci(N - 1))
  }
}

fib_prod <- function(A, B) {
  t0 <- proc.time()[3]
  fibA <- fibonacci(A)
  tA <- proc.time()[3]
  fibB <- fibonacci(B)
  tB <- proc.time()[3] 
  return (list(product=fibA*fibB,
               fibA=fibA, 
               fibB=fibB, 
               cpuA=tA - t0, 
               cpuB=tB - tA))
}
% Returns the sum of the two fibonnaci numbers given by parameters
% a & b
function [ product, fibA, fibB, cpuA, cpuB ] = fib(A, B)
t0 = cputime;
% Recursively Compute The First Fibonnacci Number
fibA = fibonnacci(A);
tA = cputime;
% Recursively Compute The Second Fibonnacci Number
fibB = fibonnacci(B);
tB = cputime;
% Split Elapsed CPU time
cpuA = tA - t0;
cpuB = tB - tA;
% Output
product = fibA * fibB;
end
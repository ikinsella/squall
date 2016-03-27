function [ result ] = fibonnacci( n )
if n < 0
    error('n must be a positive integer')
elseif n == 0 || n == 1
    result = n;

else
    result = fibonnacci(n - 2) + fibonnacci(n - 1);
end
end
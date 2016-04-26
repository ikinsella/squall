function [] = fibwrapper(varargin)
% Define Params
p = inputParser;
addParameter(p , 'A'  , -1     , @isscalar );
addParameter(p , 'B'  , -1     , @isscalar );

% Read Parameter Struct
if nargin > 0
    parse(p, varargin{:});
else
    param_struct = loadjson('params.json');
    param_names = fieldnames(param_struct);
    param_cell = [param_names'; struct2cell(param_struct)'];
    parse(p, param_cell{:});
end

% Parse Params
A = p.Results.A;
B = p.Results.B;

% Shuffle RNG For because running with runtime is non-random
rng('shuffle');

% Call Wrapped Function
[ product, fibA, fibB, cpuA, cpuB ] = fib(A, B);

% Create Results Struct & Write To JSON
results.Product = product;
results.fibA = fibA;
results.fibB = fibB;
results.cpuA = cpuA;
results.cpuB = cpuB;
opts.FileName = 'results.json';
savejson('', results, opts);
end
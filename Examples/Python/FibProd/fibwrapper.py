#!bin/env/python
import json
from src.fib import fib_prod

# Read params JSON delivered by HTCondor
with open('params.json', 'rb') as paramfile:
    params = json.load(paramfile)

# Compute & time fibonnacci numbers & their product
(product, fibA, fibB, cpuA, cpuB) = fib_prod(params['A'], params['B'])

# Write completed results to json to be sent back to submit node
results = {'product': product,
           'fibA': fibA,
           'fibB': fibB,
           'cpuA': cpuA,
           'cpuB': cpuB}

with open('results.json', 'w') as resultsfile:
    json.dump(results, resultsfile)

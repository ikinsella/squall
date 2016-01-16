#!/usr/bin/env python
import yaml
import json
import os
import shutil
import copy
import numpy as np


def write_json(dictionary, filename):
    """ Writes a dictionary to a json file """
    with open(filename, 'w') as writefile:
        json.dump(dictionary, writefile, sort_keys=True, indent=4)


def read_json(filename):
    """ Read a json file into a dictionary object """
    with open(filename, 'rb') as readfile:
        return json.load(readfile)

""" Job Post Script """
# read in params_file
params = read_json('params.json')
# read in results_file
results = read_json('results.json')
# extract uid
filename = params['uid'] + '.json'
del params['uid']
# combine into one jason
summary = {'params': params, 'results': results}
# write out uid.json
write_json(summary, filename)

""" Batch Post Script """

# Create json with batch details
batch_size = 10
rootdir = os.getcwd()
batchson = {}
for idx in xrange(batch_size):
    uid = str(idx).zfill(len(str(batch_size)))
    jobson = read_json(os.path.join(rootdir, uid, uid + '.json'))
    batchson[uid] = jobson

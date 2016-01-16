#!/usr/bin/env python
import yaml
import json
import os
import shutil
import copy
import numpy as np

from jinja2 import Environment, FileSystemLoader


def makedir(dirname):
    """ Creates a directory if it doesn't already exist """
    if not os.path.isdir(dirname):
        os.makedirs(dirname)


def write_json(dictionary, filename):
    """ Writes a dictionary to a json file """
    with open(filename, 'w') as writefile:
        json.dump(dictionary, writefile, sort_keys=True, indent=4)


def read_yaml(filename):
    """ Reads a yaml file into a list of dictionaries """
    with open(filename, 'rb') as readfile:
        return yaml.load(readfile)


def write_template(filename, template, **kwargs):
    """ Renders a tempalte and writes it to filename """
    with open(filename, 'w') as writefile:
        writefile.write(template.render(**kwargs))


def count_jobs(yamldata, expand_fields):
    """ Returns Array Of Field Lengths & Ensures Linked Fields Match """
    fields = np.zeros(len(expand_fields))
    for idx, field in enumerate(expand_fields):
        if isinstance(field, list) or isinstance(field, tuple):
            subfields = [len(yamldata[key]) for key in field]
            if not all(map(lambda x: x is subfields[0], subfields)):
                raise RuntimeError('Incompatible Length: ExpandFields')
            fields[idx] = len(subfields[0])
        else:
            fields[idx] = len(yamldata[field])
    return fields


def package_batch(batch):
    """ Packages the files to run a batch of jobs on HTCondor """

    # Create Template Environment
    tempalte_dir = os.path.join(os.path.dirname(__file__), 'templates')
    loader = FileSystemLoader(tempalte_dir)
    env = Environment(loader=loader)

    """ Define Local Directory Structure """

    currdir = os.getcwd()
    rootdir = os.path.join(currdir, batch.name)
    config = lambda batch: os.path.join(rootdir, os.path.basename(batch.yaml))
    sweepdag = lambda batch: os.path.join(rootdir, batch.sweep)
    sharedir = os.path.join(rootdir, 'shared')
    shareexe = lambda batch: os.path.join(sharedir,
                                          os.path.basename(batch.exe))
    sharepre = lambda batch: os.path.join(sharedir,
                                          os.path.basename(batch.pre))
    sharepost = lambda batch: os.path.join(sharedir,
                                           os.path.basename(batch.post))
    wrapper = lambda batch: os.path.join(sharedir, batch.wrapper)
    jobdir = lambda job: os.path.join(rootdir, job.uid)
    jobpre = lambda job: os.path.join(jobdir(job), os.path.basename(job.pre))
    jobpost = lambda job: os.path.join(jobdir(job), os.path.basename(job.post))
    paramfile = lambda job: os.path.join(jobdir(job), job.params_file)
    subfile = lambda job: os.path.join(jobdir(job), job.submit_file)
    subdag = lambda job: os.path.join(jobdir(job), job.uid + '.dag')
    resource = lambda filename: os.path.join(batch.resource_dir, filename)

    """ Fill Local Directory Structure """

    yamldata = expand_yaml(resource(batch.yaml))  # Enumerate Yaml File
    batch.create_jobs(batch_size=len(yamldata))  # Initialize Jobs

    makedir(rootdir)  # Setup Root Directory
    write_template(sweepdag(batch), env.get_template('sweep'), batch=batch)
    shutil.copyfile(resource(batch.yaml), config(batch))

    makedir(sharedir)  # Setup Shared Directory
    write_template(wrapper(batch), env.get_template('wrapper'), batch=batch)
    shutil.copyfile(resource(batch.exe), shareexe(batch))
    shutil.copyfile(resource(batch.pre), sharepre(batch))
    shutil.copyfile(resource(batch.post), sharepost(batch))

    for cfg, job in zip(yamldata, batch.jobs):  # Setup Job Directories
        makedir(jobdir(job))  # Create Job Directory
        cfg['uid'] = job.uid
        write_json(cfg, paramfile(job))  # Create Individual Parameters File
        # Create Submit File
        write_template(subfile(job), env.get_template('process'), job=job)
        # Create Subdag
        write_template(subdag(job), env.get_template('subdag'), job=job)
        shutil.copyfile(resource(job.pre), jobpre(job))
        shutil.copyfile(resource(job.post), jobpost(job))


def expand_yaml(yamlfile):
    """ Expands Yaml Fiels List Of Param Files For Each Job"""
    yamldata = read_yaml(yamlfile)

    try:  # If Expand Fields Exist They Must Be Enumerated
        expand_fields = yamldata['ExpandFields']
        del yamldata['ExpandFields']
    except KeyError:
        return yamldata

    static_data = copy.copy(yamldata)  # Copy Static Fields
    for field in [key for key in expand_fields]:
        del static_data[field]
    lengths = count_jobs(yamldata, expand_fields)
    param_files = [static_data for _ in xrange(int(lengths.prod()))]

    for cdx, param_file in enumerate(param_files):  # Enumerate Expand Fields
        for idx, field in zip(np.unravel_index(cdx, lengths), expand_fields):
            if isinstance(field, list) or isinstance(field, tuple):
                for k in field:
                    param_file[k] = yamldata[k][idx]
            else:
                param_file[field] = yamldata[field][idx]
    return param_files

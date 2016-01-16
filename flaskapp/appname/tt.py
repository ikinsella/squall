#!/usr/bin/env python
from jinja2 import Environment, FileSystemLoader
import os
from condortools import package_batch

# Create Template Environment
TEMPLATES_DIRECTORY = os.path.join(os.path.dirname(__file__),
                                   'condortools',
                                   'templates')
loader = FileSystemLoader(TEMPLATES_DIRECTORY)
env = Environment(loader=loader)


class Job(object):
    def __init__(self,
                 uid,
                 batch_size,
                 launch_directory,
                 executable,
                 memory,
                 disk,
                 flock,
                 glide,
                 arguments,
                 keyword_arguments,
                 wrapper,
                 submit_file,
                 params_file,
                 share_directory,
                 pre_script=None,
                 post_script=None):
        # Mandatory
        self.uid = str(uid).zfill(len(str(batch_size-1)))
        self.launch_dir = launch_directory
        self.exe = executable
        # Short Term Optional
        self.mem = memory
        self.disk = disk
        self.flock = flock
        self.glide = glide
        self.args = arguments
        self.kwargs = keyword_arguments
        # Optional
        self.wrapper = wrapper
        self.submit_file = submit_file
        self.params_file = params_file
        self.share_dir = share_directory
        self.pre = pre_script
        self.post = post_script


class Batch(object):

    def __init__(self,
                 name,
                 launch_directory,
                 resource_directory,
                 executable,
                 yaml_file,
                 data_urls,
                 code_urls,
                 memory,
                 disk,
                 flock=True,
                 glide=True,
                 arguments=None,
                 keyword_arguments=None,
                 setup_scripts=None,
                 sweep='sweep.dag',
                 wrapper='wrapper.sh',
                 submit_file='process.sub',
                 params_file='params.json',
                 share_directory='share',
                 pre_script=None,
                 job_pre=None,
                 post_script='post.sh',
                 job_post=None):
        # Mandatory
        self.size = 0
        self.name = name
        self.launch_dir = launch_directory
        self.resource_dir = resource_directory
        self.exe = executable
        self.yaml = yaml_file
        self.data_urls = data_urls
        self.code_urls = code_urls
        self.memory = memory
        self.disk = disk
        # Short Term Optional
        self.flock = flock
        self.glide = glide
        self.arguments = arguments
        self.kwargs = keyword_arguments
        self.setup_scripts = setup_scripts
        # Optional Arguments
        self.sweep = sweep
        self.wrapper = wrapper
        self.submit_file = submit_file
        self.params_file = params_file
        self.share_dir = share_directory
        self.pre = pre_script
        self.pre_base = os.path.basename(self.pre)
        self.job_pre = job_pre
        self.post = post_script
        self.post_base = os.path.basename(self.post)
        self.job_post = job_post
        # Make Jobs
        self.jobs = None

    def create_jobs(self, batch_size):
        if self.jobs is not None:
            raise RuntimeError('Jobs Already Created!')
        else:
            self.size = batch_size
            self.jobs = [  # Enumerate List Of Jobs
                Job(uid=uid,
                    batch_size=self.size,
                    launch_directory=os.path.join(self.launch_dir, self.name),
                    executable=self.exe,
                    memory=self.memory,
                    disk=self.disk,
                    flock=self.flock,
                    glide=self.glide,
                    arguments=self.arguments,
                    keyword_arguments=self.kwargs,
                    wrapper=self.wrapper,
                    submit_file=self.submit_file,
                    params_file=self.params_file,
                    share_directory=self.share_dir,
                    pre_script=self.job_pre,
                    post_script=self.job_post)
                for uid in range(self.size)]

# Create Test Batch
args = ['arg1', 'arg2', 'arg3']
kwargs = [('kw1', 'kwarg1'), ('kw2', 'kwarg2'), ('kw3', 'kwarg3')]
data_urls = ['http://proxy.chtc.wisc.edu/SQUID/path/to/s22_avg.mat',
             'http://proxy.chtc.wisc.edu/SQUID/path/to/CV_schemes_avg.mat',
             'http://proxy.chtc.wisc.edu/SQUID/path/to/CV_schemes_avg.mat',
             'http://proxy.chtc.wisc.edu/SQUID/path/to/metadata_avg.mat']
code_urls = ['http://proxy.chtc.wisc.edu/SQUID/path/to/r2013b.tar.gz',
             'http://proxy.chtc.wisc.edu/SQUID/path/to/mysrc.tar.gz']
setup_scripts = ['v82/setup.sh']
batch = Batch(name='test_batch',
              launch_directory=os.getcwd(),
              resource_directory=os.path.join(os.getcwd(), 'test_files'),
              executable='executable',
              yaml_file='test.yaml',
              data_urls=data_urls,
              code_urls=code_urls,
              memory=4000,
              disk=1e7,
              flock=True,
              glide=True,
              arguments=args,
              keyword_arguments=kwargs,
              setup_scripts=setup_scripts,
              wrapper='wrapper.sh',
              submit_file='process.sub',
              share_directory='share',
              pre_script='pre.sh',
              job_pre='pre.sh',
              post_script='post.sh',
              job_post='post.sh')

# Package For Shipping
package_batch(batch=batch)

job = batch.jobs[0]
# Evaluate Templates
print '---------------------------------------------------------------'
subdag = env.get_template('subdag')  # Load Subdag template
print subdag.render(job=job)
print '---------------------------------------------------------------'
process = env.get_template('process')  # Load Process template
print process.render(job=job)
print '---------------------------------------------------------------'
sweep = env.get_template('sweep')
print sweep.render(batch=batch)
print '---------------------------------------------------------------'
wrapper = env.get_template('wrapper')
print wrapper.render(batch=batch)
print '---------------------------------------------------------------'
print 'Creating Directory Structure'
print '---------------------------------------------------------------'

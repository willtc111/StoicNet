#!/usr/bin/env python2
import os
import time
import glob

OpenFaceExePath = '/home/will/OpenFace/build/bin/FaceLandmarkImg'

in_root = '/home/will/VM/StoicNetImages/outputs'
out_root = '/home/will/VM/StoicNetImages/analysis'
samples = glob.glob('{}/*/'.format(in_root))

#print(samples)
numSamples = len(samples)
print('{} samples'.format(numSamples))

block_size = 10.0
num_blocks = numSamples/block_size
avg_elapsed = 0.0
block_count = 0.0
start_time = time.time()
for i in range(0, numSamples):
    sample = os.path.basename(os.path.normpath(samples[i]))
    imgAnc = '{}anc.png'.format(samples[i])
    imgPos = '{}pos.png'.format(samples[i])
    imgGen = '{}gen.png'.format(samples[i])
    
    command = '{} -f {} -out_dir {} -f {} -out_dir {} -f {} -out_dir {} -aus > /dev/null'.format(
        OpenFaceExePath,
        imgAnc, '{}/{}'.format(out_root,sample),
        imgGen, '{}/{}'.format(out_root,sample),
        imgPos, '{}/{}'.format(out_root,sample)
    )
    
    os.system(command)
    #print("Executing command: " + command)
    if i > 0 and i % block_size < 0.01:
        end_time = time.time()
        elapsed = end_time - start_time
        block_count += 1.0
        avg_elapsed = ((avg_elapsed * (block_count-1.0)) + elapsed) / block_count
        remaining_blocks = (numSamples - i) / block_size
        remaining_sec = remaining_blocks * avg_elapsed
        remaining_min = remaining_sec / 60.0
        print("Analyzing {}.  {:.2f} minutes remaining.  Block time ({}) (avg ({}))".format(sample, remaining_min, elapsed, avg_elapsed))
        start_time = time.time()
print("Done")
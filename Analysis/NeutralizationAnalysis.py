#!/usr/bin/env python2
import os
import time
import glob
import csv

root = '/home/will/VM/StoicNetImages/analysis'

samples = glob.glob('{}/*/'.format(root))

#print(samples)
numSamples = len(samples)
print('{} samples'.format(numSamples))
ancTotal = 0.0
genTotal = 0.0
posTotal = 0.0
for i in range(0, numSamples):
    sample = os.path.basename(os.path.normpath(samples[i]))
    ancFile = '{}anc.csv'.format(samples[i])
    genFile = '{}gen.csv'.format(samples[i])
    posFile = '{}pos.csv'.format(samples[i])

    with open('ancFile', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data = list(reader)
        aus = data[1][2:18]
        print(aus)
        ancTotal += sum(aus)
        
    with open('genFile', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data = list(reader)
        aus = data[1][2:18]
        print(aus)
        genTotal += sum(aus)
        
    with open('posFile', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data = list(reader)
        aus = data[1][2:18]
        print(aus)
        posTotal += sum(aus)
    
    print("Analyzed {}.".format(sample))

print("Done")
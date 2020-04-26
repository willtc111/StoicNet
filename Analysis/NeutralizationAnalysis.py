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
ancMax = 0.0
genMax = 0.0
posMax = 0.0
for i in range(0, numSamples):
    sample = os.path.basename(os.path.normpath(samples[i]))
    print("Analyzing {}.".format(sample))
    ancFile = '{}anc.csv'.format(samples[i])
    genFile = '{}gen.csv'.format(samples[i])
    posFile = '{}pos.csv'.format(samples[i])

    with open(ancFile) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data = list(reader)
        aus = [float(s) for s in data[1][2:18]]
        #print(aus)
        ancTotal += sum(aus)
        ancMax += max(aus)
        
    with open(genFile) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data = list(reader)
        aus = [float(s) for s in data[1][2:18]]
        #print(aus)
        genTotal += sum(aus)
        genMax += max(aus)
        
    with open(posFile) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data = list(reader)
        aus = [float(s) for s in data[1][2:18]]
        #print(aus)
        posTotal += sum(aus)
        posMax += max(aus)
    
print("Average Totals:")
print(ancTotal/float(numSamples))
print(genTotal/float(numSamples))
print(posTotal/float(numSamples))
print("Average Max:")
print(ancMax/float(numSamples))
print(genMax/float(numSamples))
print(posMax/float(numSamples))
print("Done")
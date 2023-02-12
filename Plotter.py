#!/bin/python3 
import json
import matplotlib.pyplot as plt
from matplotlib import style
import sys

if len(sys.argv) < 2:
    print('Usage: ./a.py <input file>')
    exit(1)


style.use('bmh')
fig = plt.figure()
for i in range(len(sys.argv) - 1):
    with open(sys.argv[i + 1], 'r') as f:
        x = json.loads(f.read())
    ax = fig.add_subplot(1, len(sys.argv) - 1, i + 1)
        
    for j in range(len(x['vars'])):
        ax.plot(x['elemsy'][j], x['elemsx'][j], label=x['vars'][j])
    ax.set_title(sys.argv[i + 1])
    ax.legend(loc = 'upper right')

plt.show()

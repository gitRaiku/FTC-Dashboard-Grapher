#!/bin/python3

import sys
import json

if len(sys.argv) < 3:
    print('usage: ./convertjsonasc.py [input.json] [output.asc]')
    exit(1)

with open(sys.argv[1], 'r') as f:
    js = json.loads(f.read())

s = '# '
for i in js['vars']
    s += f'{i} '

with open(sys.argv[2], 'w') as f:
    print(s, file=f)
    for o in range(len(js['elemsx'])):
        print(s'

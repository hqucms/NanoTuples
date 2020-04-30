#!/usr/bin/env python
from __future__ import print_function

import argparse
import uproot
import numpy as np

parser = argparse.ArgumentParser('Submit crab jobs')
parser.add_argument('file1')
parser.add_argument('file2')
args = parser.parse_args()

t1 = uproot.open(args.file1)['Events']
t2 = uproot.open(args.file2)['Events']

br1 = set(t1.keys())
br2 = set(t2.keys())

print('Branches in file1 only: ', '\n'.join(sorted(br1 - br2)))
print('Branches in file2 only: ', '\n'.join(sorted(br2 - br1)))

branches = sorted(br1 & br2)

print('Diffs:')
for k in branches:
    a1 = t1.array(k)
    a2 = t2.array(k)
    if isinstance(a1, np.ndarray):
        same = np.all(a1 == a2)
    else:
        same = np.all(a1.counts == a2.counts) and np.all(a1.content == a2.content)
    if not same:
        if isinstance(a1, np.ndarray):
            close = np.allclose(a1, a2, rtol=1e-3, atol=1e-3, equal_nan=True)
        else:
            close = np.all(a1.counts == a2.counts) and np.allclose(a1.content, a2.content, rtol=1e-3, atol=1e-3, equal_nan=True)
        print(k, '(close)' if close else '')
        print(' ... a1=%s\n ... a2=%s' % (a1[:5], a2[:5]))

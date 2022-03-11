#!/usr/bin/env python3

origin = 'Downloads'
dest = 'D:'

import os, re, shutil
from itertools import combinations

re_validate = re.compile(r'^[^.].*\.[^.]{2,}')
re_tokenize = re.compile(r'([0-9]+)')

def tokenize(name):
    return tuple(
        ( int(x),len(x) ) if i%2 else x
        for i,x in enumerate(re_tokenize.split(name))
    )

def join(tokens,inc):
    return ''.join(
        f'{{:0{x[1]}}}'.format(x[0]+(i==inc)) if i%2 else x
        for i,x in enumerate(tokens)
    )

os.chdir(os.path.expanduser('~'))

for _, _, targets in os.walk(dest):
    targets = sorted( ( tokenize(x), x ) for x in targets )
    # groups = [
    #     {i,j}
    #     for (i,a),(j,b) in combinations(enumerate( x[0] for x in targets ),2)
    #     if tuple(a[0::2]) == tuple(b[0::2]) # same text
    #     and sum( abs(n-m) for n,m in zip(a[1::2],b[1::2]) ) == 1 # +1
    # ]
    # TODO: merge groups

    for target_t, target in targets:
        # print('target:',target)
        found = [ ]
        dt = os.path.join(dest,target)
        size1 = None

        for root, dirs, files in os.walk(origin):
            files = set(files)
            if target in files:
                if size1 is None:
                    size1 = os.path.getsize(dt)
                size2 = os.path.getsize(os.path.join(root,target))
                if size1 != size2:
                    continue
                for i in range(len(target_t)//2):
                    i = i*2+1
                    cand = join(target_t,i)
                    if cand in files:
                        found.append((root,cand))

        # TODO: if multiple are found
        # 1. check e0s0

        # TODO: if none are found
        # 1. check next season

        print('\nDELETE')
        print(target)
        q = None
        while q not in {'','y','n'}:
            q = input('[y]/n ? ')
        if q != 'n':
            os.remove(dt)

        for f in found:
            src = os.path.join(*f)
            print('\nCOPY')
            print(src)
            q = None
            while q not in {'','y','n'}:
                q = input('[y]/n ? ')
            if q != 'n':
                shutil.copy(src,dest)

    break

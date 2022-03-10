#!/usr/bin/env python3

origin = './test'
dest = './test'

import os, re
# from itertools import combinations

re_validate = re.compile(r'^[^.].*\.[^.]{2,}')
re_tokenize = re.compile(r'([0-9]+)')

def tokenize(name):
    return [
        [int(x),len(x)] if i%2 else x
        for i,x in enumerate(re_tokenize.split(name))
    ]

def join(tokens):
    return ''.join(
        f'{{:0{x[1]}}}'.format(x[0]) if i%2 else x
        for i,x in enumerate(tokens)
    )

for _, _, targets in os.walk(origin):
    targets = [ x for x in targets if re_validate.match(x) ]
    targets_t = [ tokenize(x) for x in targets ]
    # groups = [
    #     {i,j}
    #     for (i,a),(j,b) in combinations(enumerate(targets_t),2)
    #     if tuple(a[0::2]) == tuple(b[0::2])
    #     and sum( abs(n-m) for n,m in zip(a[1::2],b[1::2]) ) == 1
    # ]

    for target, target_t in zip(targets,targets_t):
        found = [ ]

        for root, dirs, files in os.walk(origin):
            files = set(files)
            if target in files:
                for i in range(len(target)//2):
                    i = i*2+1
                    target_t[i][0] += 1
                    cand = join(target_t)
                    if cand in files:
                        found.append((root,cand,i))
                    target_t[i][0] -= 1

        for x in found:
            print(x)

    break

#!/usr/bin/env python

import sys
import itertools

def readfq(fp): # this is a generator function

    rstrip = str.rstrip
    for aread in itertools.izip_longest(*[fp]*4):
        yield (rstrip(aread[0]),rstrip(aread[1]),rstrip(aread[3]))


if __name__ == "__main__":
    n, slen, qlen = 0, 0, 0

    for aread in readfq(sys.stdin):
        n += 1
        slen += len(aread[1])
        qlen += len(aread[2])
    print n, '\t', slen, '\t', qlen



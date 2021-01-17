#!/usr/bin/env python

BUFFER_SIZE = 1024 * 1024;

def readfq(fp): # this is a generator function
    rest = []
    newline = False
    while True:
        buffer = fp.read(BUFFER_SIZE)
        if not buffer:
            break
        lines = buffer.splitlines()
        if rest:
            if not newline:
                v = rest.pop(-1)
                lines[0] = "%s%s" % (v,lines[0])
            rest.extend(lines)
            lines = rest
        newline = True if buffer[-1] == '\n' else False
        n = len(lines)
        m = 4 * int((n-1)/4)
        r = n - m
        if newline and r == 4:
            rest = []
            m = m + 1
        else:
            rest = lines[m:n]
        for i in range(0,m,4):
            yield (lines[i], lines[i+1], lines[i+3])

if __name__ == "__main__":
    import sys
    n, slen, qlen = 0, 0, 0
    for name, seq, qual in readfq(sys.stdin):
        n += 1
        slen += len(seq)
        qlen += qual and len(qual) or 0
    print n, '\t', slen, '\t', qlen

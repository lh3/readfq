#!/usr/bin/env python

BUFFER_SIZE = 1024 * 1024;

def readfq(fp): # this is a generator function

    rest = []

    newline = False
    
    a = fp.read(1)
    if a == "@":
        # FASTQ
        rest = [a]
        while True:
            buffer = fp.read(BUFFER_SIZE)
            if not buffer:
                if rest and len(rest) == 4:
                    yield(rest[0],rest[1],rest[3])
                break
            if rest:
                if newline:
                    lines = "".join(("\n".join(rest),'\n', buffer)).splitlines()
                else:
                    lines = "".join(("\n".join(rest), buffer)).splitlines()
            else:
                lines = buffer.splitlines()
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
                
    elif a == ">":
        # FASTA
        rest = a
        while True:
            buffer = fp.read(BUFFER_SIZE)
            if not buffer:
                if rest:
                    u = rest.partition("\n")
                    yield (u[0],u[2].rstrip("\n"),"")
                break
            if rest:
                lines = "".join((rest,buffer)).splitlines()
            else:
                lines = buffer.splitlines()

            n = len(lines)
            x = [i for i,e in enumerate(map(lambda u: u[0] if u else '',lines)) if e==">"]

            newline = True if buffer[-1] == '\n' else False
            b = x[-1]
            if b==n-1:
                if newline:
                    rest = "\n".join((lines[b],"\n"))
                else:
                    rest = lines[b]
            elif newline:
                rest = "".join((lines[b],"\n","".join(lines[b+1:n]),"\n"))
            else:
                rest = "".join((lines[b],"\n","".join(lines[b+1:n])))
            for i in range(1,len(x)):
                b = x[i-1]
                c = x[i]
                yield (lines[b],"".join(lines[b+1:c]),'')


if __name__ == "__main__":
    import sys
    n, slen, qlen = 0, 0, 0
    for name, seq, qual in readfq(sys.stdin):
        n += 1
        slen += len(seq)
        qlen += qual and len(qual) or 0
    print n, '\t', slen, '\t', qlen

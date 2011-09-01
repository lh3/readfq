def readfq(fp): # this is a generator function
    import string
    finished, last = False, None
    while (True): # mimic closure; is it a bad idea?
        if (finished): return # already hit the end-of-file (EOF)
        if (last == None): # the first record or a record following a fastq
            for l in fp: # search for the start of the next record
                if (l[0] == '>' or l[0] == '@'):
                    last = l[:-1] # save this line
                    break
        if (last == None): # EOF
            finished = True
            return
        i = string.find(last, ' ') # separate the fasta/q name and the comment
        if (i < 0): i = string.find(last, '\t') # also try "\t"
        name = i > 0 and last[1:i] or last[1:] # set the fasta/q name
        seqs, last, c = [], None, None
        for l in fp: # read the sequence
            c = l[0]
            if (c == '>' or c == '@' or c == '+'):
                last = l[:-1]
                break
            seqs.append(l[:-1])
        if (last == None): finished = True # EOF
        if (c != '+'): yield name, ''.join(seqs), None # yield a fasta record
        else: # this is a fastq record
            seq, leng, seqs = ''.join(seqs), 0, []
            for l in fp: # read the quality
                seqs.append(l[:-1])
                leng += len(l) - 1
                if (leng >= len(seq)): # have read enough quality
                    last = None
                    yield name, seq, ''.join(seqs); # yield a fastq record
                    break
            if (last): # reach EOF before reading enough quality
                finished = True
                yield name, seq, None # yield a fasta record instead

import sys
n, slen, qlen = 0, 0, 0
for name, seq, qual in readfq(sys.stdin):
    n += 1
    slen += len(seq)
    qlen += qual and len(qual) or 0
print n, '\t', slen, '\t', qlen

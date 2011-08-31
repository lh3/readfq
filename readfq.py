def readfq(fp):
	import string
	finished, last = False, None
	while (True):
		if (finished): return
		if (last == None):
			for l in fp:
				if (l[0] == '>' or l[0] == '@'):
					last = l[:-1]
					break
		if (last == None):
			finished = True
			return
		i = string.find(last, ' ')
		if (i < 0): i = string.find(last, '\t')
		name = i > 0 and last[1:i] or last[1:]
		seqs, last, c = [], None, None
		for l in fp:
			c = l[0]
			if (c == '>' or c == '@' or c == '+'):
				last = l[:-1]
				break
			seqs.append(l[:-1])
		if (last == None): finished = True
		if (c != '+'): yield name, ''.join(seqs), None
		else:
			seq, leng = ''.join(seqs), 0
			seqs = []
			for l in fp:
				seqs.append(l[:-1])
				leng += len(l)
				if (leng >= len(seq)):
					last = None
					yield name, seq, ''.join(seqs);
					break
			if (last):
				finished = True
				yield name, seq, None

import sys
n, slen, qlen = 0, 0, 0
for name, seq, qual in readfq(sys.stdin):
	n += 1
	slen += len(seq)
	qlen += qual and len(qual) or 0
print n, '\t', slen, '\t', qlen

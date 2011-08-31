local function readfq(fp)
	local finished, last = false, nil;
	return function()
		local match;
		if finished then return nil end
		if last == nil then -- the first record or a record following a fastq
			for l in fp:lines() do
				if l:byte(1) == 62 or l:byte(1) == 64 then -- ">" || "@"
					last = l;
					break;
				end
			end
			if last == nil then
				finished = true;
				return nil;
			end
		end
		local tmp = last:find("%s");
		name = (tmp and last:sub(2, tmp-1)) or last:sub(2); -- sequence name
		local seqs = {};
		local c; -- the first character of the last line
		last = nil;
		for l in fp:lines() do -- read sequence
			c = l:byte(1);
			if c == 62 or c == 64 or c == 43 then
				last = l;
				break;
			end
			table.insert(seqs, l);
		end
		if last == nil then finished = true end -- end of file
		if c ~= 43 then return name, table.concat(seqs) end -- a fasta record
		local seq, len = table.concat(seqs), 0; -- prepare to parse quality
		seqs = {};
		for l in fp:lines() do -- read quality
			table.insert(seqs, l);
			len = len + #l;
			if len >= #seq then
				last = nil;
				return name, seq, table.concat(seqs);
			end
		end
		finished = true;
		return name, seq;
	end
end

function countfq() -- for testing only
	local n, slen, qlen = 0, 0, 0
	for name, seq, qual in readfq(io.stdin) do
		n, slen = n + 1, slen + #seq
		qlen = qlen + (qual and #qual or 1)
	end
	print(n, slen, qlen)
end

countfq()

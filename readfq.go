package main

import (
  "bufio"
  "bytes"
  "fmt"
  "io"
  "os"
)

func main() {
  n, sLen, qLen := 0, int64(0), int64(0)
  var fqr FqReader
  fqr.Reader = bufio.NewReader(os.Stdin)
  for r, done := fqr.Iter(); !done; r, done = fqr.Iter() {
    n += 1
    sLen += int64(len(r.Seq))
    qLen += int64(len(r.Qual))
  }
  fmt.Printf("%v\t%v\t%v\n", n, sLen, qLen)
}

// Record contains the data from a fasta fastq record
type record struct {
  Name, Seq, Qual string
}

// FqReader holds all the necessary fields that will be use during the processing
// of a fasta fastq file
type FqReader struct {
  Reader          *bufio.Reader
  last, seq, qual []byte // last line processed, temporary seq and qual values
  finished        bool
  rec             record
}

// iterLines iterates over the lines of a reader
func (fq *FqReader) iterLines() ([]byte, bool) {
  line, err := fq.Reader.ReadSlice('\n')
  if err != nil {
    if err == io.EOF {
      return line, true
    } else {
      panic(err)
    }
  }
  return line, false
}

var space = []byte(" ")

func (fq *FqReader) Iter() (record, bool) {
  if fq.finished {
    return fq.rec, fq.finished
  }
  // Read the seq id (fasta or fastq)
  if fq.last == nil {
    for l, done := fq.iterLines(); !done; l, done = fq.iterLines() {
      if l[0] == '>' || l[0] == '@' { // read id
        fq.last = l[0 : len(l)-1]
        break
      }
    }
    if fq.last == nil { // We couldn't find a valid record, no more data in file
      fq.finished = true
      return fq.rec, fq.finished
    }
  }
  fq.rec.Name = string(bytes.SplitN(fq.last, space, 1)[0])
  fq.last = nil

  // Now read the sequence
  fq.seq = fq.seq[:0]
  for l, done := fq.iterLines(); !done; l, done = fq.iterLines() {
    c := l[0]
    if c == '+' || c == '>' || c == '@' {
      fq.last = l[0 : len(l)-1]
      break
    }
    fq.seq = append(fq.seq, l[0:len(l)-1]...)
  }
  fq.rec.Seq = string(fq.seq)

  if fq.last != nil { // There are more lines
    if fq.last[0] != '+' { // fasta record
      return fq.rec, fq.finished
    }
    leng := 0
    fq.qual = fq.qual[:0]
    for l, done := fq.iterLines(); !done; l, done = fq.iterLines() {
      fq.qual = append(fq.qual, l[0:len(l)-1]...)
      leng += len(l)
      if leng >= len(fq.seq) { // we have read enough quality
        fq.last = nil
        fq.rec.Qual = string(fq.qual)
        return fq.rec, fq.finished
      }
    }
    fq.finished = true
    fq.rec.Qual = string(fq.qual)
  }
  return fq.rec, fq.finished // incomplete fastq quality, return what we have
}



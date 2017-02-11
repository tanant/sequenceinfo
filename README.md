##SequenceInfo

The `SequenceInfo` package is intended to provide a relatively simple, well documented, flexible set of tools to solve the problem of compacting a large volume of file paths into a number of compact representations of sequences.

e.g. : the set of files foo.123.png, foo.124.png, foo.125.png, foo.022.png would all belong to a sequence that could be expressed as foo.###.png [22, 123-125].

###Architectural overview

There are two major modules: `Splitter`, `Sequencer` 

####Splitter 
Responsible for taking in a string, and conforming it into a head/digit/tail) triple

- configured by regexes that are stacked in precendence order
- match patterns themeselves must define three groups
- contains no state information, strightly a function
- will fallback to a default regex match of {.*}/None/None
- module should have precanned match patterns and tests to make sure they are precisely targeted
   
####Sequencer 
- responsible for taking a stream of splitter-conformed items and building an internal state to represent these
- can be asked to 'report' on the sequences that are known in the form of Sequence objects
- can (should be) fed with additional paths as it goes. Could become a memory hog :|
- is responsible for coming up with the padding rule. 

####Sequence
- not sure if this is needed, but is the concept of a sequence. Has the pattern, knows how to convert the pattern to different padding formats,
- queries avail: first, last, padding, compact repr, frames, hasFrame(), expandtofullfrominternal, expandtofullfromexplicit, expandfrom frame

####Preprocessing
- the `Splitter` expects to be fed a single string, so we should generate

####Sources
- the `Preprocessor` just cares about mangling strings in a way that regexs might not be able to do (routing to different Sequencers for example)


###Typical Usage

would envisage this kind of thing
```
si = SequenceInfo()
# configure, for example si.setPattern("blah")
for root, dirs, files in os.walk(path):
    si.add([os.path.join(root,x) for x in files])   # accepts any iterable to digest
    
sequences = si.sequences()
print si.num_sequences
print sequences[0].first
print sequences[0].last
print str(sequences[0])  # blah.foo.####.exr [1-10,13-14x2]
```

with additional manip of add/remove/repr items

Would be nice for Sequencers to be addable themselves so you don't have to worry about making multiples and tracking them (it'd be an expensive op otherwise to unpack and repack the sequence..)
>>>>>>> Add first draft of project readme

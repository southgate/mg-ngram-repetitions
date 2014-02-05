# N-Gram Repetition Analysis

Python module to analyze repetition of n-grams up 15 words in length.

### Running

Move the Corpus directory into this directory and run the following:

```
python repetition.py
```

This will create CSV results in the `output` directory.  Global results
will live in `output/Corpus` while results specific to each work will
live in `output/Corpus/works`.

### Running the Tests

There are some rudimentary tests that just make sure the `reptition`
module runs. It doesn't contain any validation of the output *YET*. 

The `fixtures` directory contains test data.  

To run the tests:

```
python repetition_tests.py
```

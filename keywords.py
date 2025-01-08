#!/usr/bin/python3

import sys
from concurrent.futures import ProcessPoolExecutor

## output and debug section
verbosity = 0
def kwout(fmt, verbose, *args, **kwargs):
    '''main output function that understands verbosity'''
    global verbosity
    if verbose <= verbosity:
        print('#' * (verbose+1), fmt.format(*args, **kwargs), file=sys.stderr)

### helper output functions
def warn(fmt, *args, **kwargs): kwout(fmt, 0, *args, **kwargs)
def info(fmt, *args, **kwargs): kwout(fmt, 1, *args, **kwargs)
def debug1(fmt, *args, **kwargs): kwout(fmt, 2, *args, **kwargs)
def debug2(fmt, *args, **kwargs): kwout(fmt, 3, *args, **kwargs)
def debug3(fmt, *args, **kwargs): kwout(fmt, 4, *args, **kwargs)
def debug4(fmt, *args, **kwargs): kwout(fmt, 5, *args, **kwargs)

def cycle(idx, word, ls, words):
    '''recursive function that creates keywords of all the letters in the list'''
    global letters
    if idx==1:
        ## print during the 1st index - should be in a process
        info('cycle(): idx={0}, letter={1}', idx, word[0])

    debug4('cycle(): idx={}, word={}', idx, word)

    if len(word) > len(letters):
        raise ValueError(f'Word is greater than length {len(letters)}: {word}')

    if idx > len(letters):
        raise ValueError(f'Index is greater than length {len(letters)}: {idx}')

    # short circuit the recursion if we've exhausted all letters
    if idx==len(letters) or not ls:
        words.add(word)
        word=''
        debug4('cycle(): idx={}, word={}, words={}', idx, word, len(words))
        return words

    # executor section that preps to run things in a process
    tasks = []
    executor = None
    if idx == 0:
        # run in a process instead of a thread in order to manage memory
        executor = ProcessPoolExecutor()

    # iterate letters of the list
    for l in ls:
        # create a new list from old list
        nls = list(ls)
        # make sure letter is removed from new list
        li = nls.index(l)
        del nls[li]
        # add letter to new word via recursive call
        if executor:
            # run in a process
            tasks.append( executor.submit(cycle, idx+1, word+l, nls, words) )
        else:
            # do not run in a process
            # add the words to the list of words
            words.update( cycle(idx+1, word+l, nls, words) )

    if executor:
        # iterate through processes
        for task in tasks:
            # add the words to the list of words
            words.update(task.result())
        executor.shutdown(wait=True)

    debug4('cycle(): idx={}, word={}, words={}', idx, word, len(words))

    # return the list of words, breaking the recursion
    return words
    
letters = []
def create_keywords(args_letters, outfile):
    '''main creation function that calls the recurisve function above and outputs the result'''
    global letters
    letters = args_letters

    info('create_keywords(): letters={}', letters)

    words=cycle(0, '', list(letters), set())
    debug2('create_keywords(): total words: {}', len(words))
    words = list(set(words))
    debug3('create_keywords(): unique words: {}', len(words))
    debug1('create_keywords(): sorting words: {}', len(words))
    words.sort()
    info('create_keywords(): writing out words: {}', len(words))
    for i in words:
        print(i, file=outfile)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', help='increase verbosity (include multiple times)', action='count', default=0)
    parser.add_argument('letters', help='letters to use to create keywords (required)')
    parser.add_argument('--output', '-o', help='where to write output (default: stdout)', default='-')
    parser.add_argument('--force', '-f', help='force overwriting of existing output', action='store_true', default=False)

    args = parser.parse_args()

    verbosity = args.verbose
    output = None

    def get_fp(args):
        if args.output == '-':
            return sys.stdout

        try:
            return open(args.output, 'x')
        except FileExistsError as x:
            if args.force:
                warn('Overwriting output file: {}', args.output)
                return open(args.output, 'w')
            raise x

    info('Starting keywords creation, writing to {}', 'stdout' if args.output == '-' else args.output)
    with get_fp(args) as fp:
        create_keywords(args.letters, fp)

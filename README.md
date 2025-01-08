# misc-scripts
Collection of misc scripts, too small for a project or used for a single purpose.

# keywords.py

This is a script that will create a list of all possible combinations of
letters. Some of these letters might be a real word, sometimes not.

**Purpose:**

I used this to help solve crossword type cryptic clues in a game I played.
Sometimes the letters would spell a unique name. I used the combinations of
these keywords to search logs or a database of known names or items for the
answer.

**Features:**

1. Multi-threaded via multiple processes.
2. Deduplicates results on the fly to reduce memory consumption.
3. Portable as it's written in python.

**Usage:** 

```bash
usage: keywords.py [-h] [--verbose] [--output OUTPUT] [--force] letters

positional arguments:
  letters               letters to use to create keywords (required)

optional arguments:
  -h, --help            show this help message and exit
  --verbose, -v         increase verbosity (include multiple times)
  --output OUTPUT, -o OUTPUT
                        where to write output (default: stdout)
  --force, -f           force overwriting of existing output
```

**Question:** Why did I use processes via the ProcessExecutor rather than
threads via the ThreadPoolExecutor?

**Answer:** Two reasons: (1) I found the thread implementation in python not to
be consistent, so sometimes threads would not execute on all the available
virtual cores. (2) The memory consumption is harder to track via threads as
it's bundled together in a single process. The ProcessExecutor just seemed to
work more consistently, and bonus: I could easily see the memory consumption.

# DISCLAIMER

These are released for fun, nothing serious, and definitely not recommended for
production.

There are probably bugs.

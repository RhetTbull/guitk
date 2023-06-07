# Utilities

These are utilities for use while developing GUITk.

## screenshot.py

Take screenshots of a GUITk Window and save them to a file.

```
usage: screenshot.py [-h] [--overwrite] [--delay DELAY] file classname output

Take screenshot of a GUItk window and save to file

positional arguments:
  file           Python file to run
  classname      Window class to instantiate
  output         Output file name

options:
  -h, --help     show this help message and exit
  --overwrite    Overwrite output file
  --delay DELAY  Delay before screenshot in milliseconds
```
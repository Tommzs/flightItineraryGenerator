import numpy as np
import sys


def readArgs():
    None
    #TODO: Read args (filename)


def readInputData(file=None):
    #TODO: Check if there is input file given.
    # If not parse the stdin
    for line in iter(sys.stdin.readline, ''):
        print(line, end='')


if __name__ == "__main__":
    # Read args, allows input file as parameter
    file = readArgs()
    # Parse input data
    parsedData = readInputData()
    #...

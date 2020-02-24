import sys
import argparse

for line in sys.stdin:
    parsed_line = line.strip().split(" ")
    if len(parsed_line) == 3:
        if parsed_line[2] == sys.argv[1]:
            print(parsed_line[0], parsed_line[1])

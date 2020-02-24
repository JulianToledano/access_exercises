import sys
import datetime

START_TIMESTAMP = datetime.datetime.fromtimestamp(int(sys.argv[1]) / 1e3)
END_TIMESTAMP = datetime.datetime.fromtimestamp(int(sys.argv[2]) / 1e3)
for line in sys.stdin:
    parsed_line = line.strip().split(" ")
    dt = datetime.datetime.fromtimestamp(int(parsed_line[0]) / 1e3)
    if dt > START_TIMESTAMP and dt < END_TIMESTAMP:
        print(parsed_line[1])

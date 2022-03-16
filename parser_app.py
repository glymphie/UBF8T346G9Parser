#!/usr/bin/env python
from backupreader import reader
from olk15parser import parser

if __name__ == "__main__":
    backupreader_app = reader.backupreader()
    for m in backupreader_app.iterate_over_messages():
        with open(m, 'rb') as f:
            print(f.read().decode('utf-8', 'ignore'))

        break


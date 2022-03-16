#!/usr/bin/env python
from backupreader import reader
from olk15parser import parser

if __name__ == "__main__":
    backupreader_app = reader.backupreader()
    backupreader_app.iterate_over_messages()


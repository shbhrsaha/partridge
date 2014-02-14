#!/usr/bin/env python
#
# Copyright 2014 Shubhro Saha
#
# Licensed under Creative Commons Attribution 3.0 Unported. You may obtain
# a copy of the license at
#
#     http://creativecommons.org/licenses/by/3.0/deed.en_US
#
# No attribution to the original author is required.
#

"""Python library for automatically executing commands when a file changes

It is a small python script that monitors the local 
filesystem for changes and runs a command when a change
is detected. The default use case automatically
compiles a LaTeX file to PDF when it is changed.

Usage: python partridge.py [file to monitor for changes]

"""

import sys
import os
import time
import logging

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class ChangeHandler(LoggingEventHandler):
    """
        Adapts watchdog's LoggingEventHandler for Partridge's purpose
    """

    def __init__(self):
        self.stale = False

    def sync(self):
        try:
            logging.info("Executing...")
            os.system("echo x | pdflatex %s" % sys.argv[1])
            logging.info("Execution complete")
        except:
            raise
            logging.info("Execution failed")

    def on_modified(self, event):
        if sys.argv[1] in event.src_path:
            self.stale = True


if __name__ == "__main__":
    
    print "==========="
    print " PARTRIDGE "
    print "==========="

    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.getcwd(), recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
            if event_handler.stale:
                event_handler.sync()
                event_handler.stale = False
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
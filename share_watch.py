#!/usr/bin/env python3

import os
import logging
import argparse
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler, FileModifiedEvent

logger = logging.getLogger()

class ModifyEventHandler(FileSystemEventHandler):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.modified = False
        self.modify_time = time.time()
    
    def on_any_event(self, event: FileSystemEvent):
        if isinstance(event, FileModifiedEvent):
            logger.info('file %s modified', self.file_path)
            self.modified = True
            self.modify_time = time.time()


def remount_directory(dir):
    logger.info('unmount %s', dir)
    if os.system(f'umount {dir}') != 0:
        raise SystemError('umount')
    time.sleep(0.5)
    if os.system('sync') != 0:
        raise SystemError('sync')
    time.sleep(0.5)
    logger.info('mount %s', dir)
    if os.system(f'mount {dir}') != 0:
        raise SystemError('mount')
    logger.info('re-mounted %s', dir)


parser = argparse.ArgumentParser()
parser.add_argument('--watch', required=True, help='file to watch')
parser.add_argument('--mount', required=True, help='remount directory')
parser.add_argument('--timeout', type=int, default=5, help='timeout seconds (default: %(default)s)')
args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger.info('starting, watching %s, timeout=%ss', args.watch, args.timeout)

handler = ModifyEventHandler(args.watch)
observer = Observer()
observer.schedule(handler, args.watch)
observer.start()
try:
    while True:
        if handler.modified:
            if time.time() - handler.modify_time > args.timeout:
                logger.info('passed %s seconds after last modify, triggering actions', args.timeout)
                handler.modified = False
                remount_directory(args.mount)
        time.sleep(1)
except KeyboardInterrupt:
    logger.info('interrupted')
finally:
    observer.stop()
    observer.join()

logger.info('done.')

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


def remount_directory(mount_dir, sync_dir):
    logger.info('unmount %s', mount_dir)
    if os.system(f'umount {mount_dir}') != 0:
        raise SystemError('umount')
    time.sleep(1)
    if os.system('sync') != 0:
        raise SystemError('sync')
    time.sleep(1)
    logger.info('mount %s', mount_dir)
    if os.system(f'mount {mount_dir}') != 0:
        raise SystemError('mount')
    time.sleep(1)
    logger.info('syncing %s to %s', mount_dir, sync_dir)
    if os.system(f'rsync -ar {mount_dir}/. {sync_dir}/') != 0:
        raise SystemError('rsync')
    logger.info('re-mounted %s and synced to %s', mount_dir, sync_dir)


parser = argparse.ArgumentParser()
parser.add_argument('--watch', required=True, help='file to watch')
parser.add_argument('--mount', required=True, help='remount directory')
parser.add_argument('--sync', required=True, help='rsync directory')
parser.add_argument('--timeout', type=int, default=5, help='timeout seconds (default: %(default)s)')
args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger.info('starting, watching %s, timeout=%ss', args.watch, args.timeout)

remount_directory(args.mount, args.sync)

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
                remount_directory(args.mount, args.sync)
        time.sleep(1)
except KeyboardInterrupt:
    logger.info('interrupted')
finally:
    observer.stop()
    observer.join()

logger.info('done.')

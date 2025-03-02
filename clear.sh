#!/bin/bash

systemctl stop pi_usb_share.watch.service
umount /mnt/usb_share

mkfs.vfat /usb_share.img
rm -rf /srv/usb_share/*

mount /mnt/usb_share
systemctl start pi_usb_share.watch.service
systemctl status pi_usb_share.watch.service --no-pager

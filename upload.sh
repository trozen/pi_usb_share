#!/bin/bash -x

host=${1:-pi@piusbshare.dom}
rsync -arv --exclude='.git' . "$host":pi_usb_share/

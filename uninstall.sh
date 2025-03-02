#!/bin/bash

uninstall_service() {
    name=$1
    systemctl stop $name
    systemctl disable $name
}

uninstall_service pi_usb_share.modprobe.service
uninstall_service pi_usb_share.watch.service

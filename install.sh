#!/bin/bash

install_service() {
    name=$1
    ln -sv "/home/pi/pi_usb_share/$name" /etc/systemd/system
    systemctl daemon-reload
    systemctl enable $name
    systemctl start $name
    systemctl status $name --no-pager
}

install_service pi_usb_share.modprobe.service
install_service pi_usb_share.watch.service

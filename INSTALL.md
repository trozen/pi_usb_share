# Install

```
sudo apt install vim python3-watchdog samba
```

```
sudo dd bs=1M if=/dev/zero of=/usb_share.img count=1024
sudo mkfs.vfat /usb_share.img
sudo mkdir /mnt/usb_share
sudo mkdir /srv/usb_share
```

`sudo vim /boot/firmware/config.txt`
```
[cm5]
#dtoverlay=dwc2,dr_mode=host

[all]
dtoverlay=dwc2
```

`sudo vim /etc/fstab`
```
/usb_share.img /mnt/usb_share vfat loop,ro,sync,flush 0 2
```

`sudo vim /etc/samba/smb.conf`
```
[usb]
browseable = yes
path = /srv/usb_share
guest ok = yes
read only = yes
```
`sudo systemctl restart smbd.service`

Install and start services:
```
sudo ./install.sh
```

# Monitor

`journalctl -u pi_usb_share.modprobe.service -f`

# Uninstall

Services:
```
sudo ./uninstall.sh
```

# Start/stop module manually

```
sudo modprobe g_mass_storage file=/usb_share.img stall=0 removable=1
sudo modprobe -r g_mass_storage
```

# Some commands that were NOT NEEDED after all

These commands are not needed, but found in various tutorials. Leaving for future reference.

`sudo vim /etc/modules`
```
# /etc/modules: kernel modules to load at boot time.
#
# This file contains the names of kernel modules that should be loaded
# at boot time, one per line. Lines beginning with "#" are ignored.
# Parameters can be specified after the module name.
dwc2
```

`sudo vim /boot/firmware/cmdline.txt`
```
console=serial0,115200 console=tty1 root=PARTUUID=b7f2ad12-02 rootfstype=ext4 fsck.repair=yes rootwait modules-load=dwc2,g_mass_storage cfg80211.ieee80211_regdom=PL
```

`sudo vim /etc/modules`
```
g_mass_storage file=/usb_share.img stall=0 removable=1
```

`sudo vim /etc/rc.local`
```
modprobe g_mass_storage file=/usb_share.img stall=0 removable=1
```

#!/bin/bash
#run 'sudo blkid -s UUID' to get the list of drivers and partitions with teir UUID
mount UUID=00C314D32E38DB25 /mnt/HD160 -t ntfs -o rw,auto,uid=65534,gid=1001,dmode=775,fmode=775,fmask=0002,dmask=0002

#!/bin/bash
 # today=`date +%Y-%m-%d__%H:%M`; raspistill -rot 180 -o - | ssh -i ~/.ssh/id_rsa admin@192.168.30.11 -oIdentitiesOnly=yes -o "StrictHostKeyChecking no" -C " cat > '/volume1/homes/admin/plume/$today.jpg'"
today=`date +%Y-%m-%d__%H:%M`; raspistill -rot 270 -o - | ssh -o StrictHostKeyChecking=no -o GlobalKnownHostsFile=/dev/null -o UserKnownHostsFile=/dev/null admin@192.168.30.11 -C " cat > '/volume1/homes/admin/plume/$today.jpg'"



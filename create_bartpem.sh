#!/bin/bash

usage ()
{
        echo "create_bartpempb.sh -i <ip> -s <hostname> -u <use> -v <DB version> -h "
        echo "-i ip address"
        echo "-s lowercase servername"
        echo "-u Use = UAT or PROD"
        echo "-v DB version = 94 or 96"
        echo "-h HELP =  display this message"
}

options=':i:s:u:v:pnta'
while getopts $options option
do
    case $option in
        i) IPADDRESS=$OPTARG;;
        s) HOSTNAME=$OPTARG;;
        u) USEAGE=$OPTARG;;
        v) DBVER=$OPTARG;;
        \?) usage; exit 1;;
    esac
done

# Sanity check the command line arguments
if [ $OPTIND -eq 1 ]; then
        usage; exit 1
fi

CFGHOSTNAME=$USEAGE-$HOSTNAME
echo $IPADDRESS
echo $USEAGE
echo $CFGHOSTNAME
echo $DBVER

/root/scripts/create_bartpem/create_bartpem.py -i $IPADDRESS -s $HOSTNAME -u $USEAGE -v $DBVER

cd /root/chef-repo/cookbooks
git add .
git commit -m "add $CFGHOSTNAME cookbook"
knife cookbook upload bartpem
ssh -t root@SGVLGSAACbarpem "sudo chef-client"

# pyrufa
# Realtime Users For Asterisk.
## Features
The current version allows you to:
* add,
* delete,
* edit

users placed in mysql database. 
Also allows to show users by:
* number,
* callerid,
* status,
* single account.

Extra-options: 
* making configs for provisioning grandstream gxp-1xxx, gxp-2xxx. At this time only for single account.
* reboot remote phones via ip-address.

## Dependencies
* python3.4+
* python3-mysqldb
* python3-httplib2

Install all dependencies:

  sudo apt install python3-mysqldb python3-httplib2
  
## Install
  git clone https://github.com/vansatchen/pyrufa.git pyrufa
  
  cd pyrufa
  
### Edit variables
  nano vars.py

## Usage
./pyrufa.py

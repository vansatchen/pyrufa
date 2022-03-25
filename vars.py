# Simple config for pyRUFA
# Python Realtime Users For Asterisk

#--- Settings for connect to Mysql ---#
dbHost = "127.0.0.1"
dbUser = "asteriskuser"
dbPass = "asteriskpass"
dataBase = "asteriskdb"
dbCharset = "utf8"

#--- Settings for create sip account ---#
defaultContext = somecontext # Context that use for action 'add' and display as default
                             # If name of context is what your need, just tap 'Enter'-key
                             # and default context for adding user will be as context.

defaultData = pass # This option usefull if you have simple password for sip-account(number+pass),
                   # for example, if you add number '1234' and defaultpass = pass, password will be '1234pass'
                   # If you dont want use defaultpass, just comment it out or use defaultpass = 0,
                   # and password will be promt.

lenName = 4 # Length of numbers

#--- Settings for create phone config ---#
# At this time, config for single account on Grandstream phones gxp1xxx, gxp2xxx
pbxServer = "pbx.example.com"
cfgLocation = "/path/to/configs/grandstream/" # Path that use for provisioning. Use for check that config already available.
phoneAdminPass = "admin" # Admin password for access to phone WUI.
vlanEnabled = "0" # Option to enable vlan on phone. Available values: 0 or 1.
vlan = "0" # Number of vlan.
phoneLang = "ru" # Display language on phone.
phoneTZ = "MTZ-5MDT-5,M4.1.0,M11.1.0"
phoneUserPass = "userpass" # User password for access to phone WUI.
ntpServer = "pool.ntp.org"

#--- Other settings ---#
adminPass = "admin1" # Admin password for reboot phone.

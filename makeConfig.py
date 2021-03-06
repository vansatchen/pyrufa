import vars

def makeGrandstreamConfig(name, secret, macAddress):
    fileName = "cfg" + macAddress + ".xml"

    with open(fileName, "w") as file:
        file.write('<?xml version="1.0" encoding="UTF-8" ?>\n<gs_provision version="1">\n')

    with open(fileName, "a") as file:
        file.write('<mac>%s</mac>\n' % macAddress)
        file.write('  <config version="1">\n    <P271>1</P271>\n    <P270>%s</P270>\n' % name)
        file.write('    <P47>%s</P47>\n    <P35>%s</P35>\n' % (vars.pbxServer, name))
        file.write('    <P36>%s</P36>\n' % name)
        file.write('    <P34>%s</P34>\n' % secret)
        file.write('    <P3>%s</P3>\n' % name)
        file.write('    <P2>%s</P2>\n\n' % vars.phoneAdminPass)
        file.write('<!--# vlan -->\n')
        file.write('    <P22174>%s</P22174>\n' % vars.vlanEnabled)
        file.write('    <P51>%s</P51>\n\n' % vars.vlan)
        file.write('<!--# Display language -->\n    <P1362>%s</P1362>\n\n' % vars.phoneLang)
        file.write('<!--# TimeZone -->\n    <P64>customize</P64>\n')
        file.write('    <P246>%s</P246>\n\n' % vars.phoneTZ)
        file.write('<!--# NTP server -->\n    <P30>%s</P30>\n\n' % vars.ntpServer)
        file.write('<!--# User pass -->\n    <P196>%s</P196>\n\n' % vars.phoneUserPass)
        file.write('<!--# Disable SIP NOTIFY Authentication -->\n    <P4428>1</P4428>\n\n')
        file.write('<!-- Time dd-mm-yyyy  -->\n    <P122>1</P122>\n\n')
        file.write('<!-- LLDP -->\n    <P1684>0</P1684>\n\n')
        file.write('<!-- Phonebook -->\n    <P330>1</P330>\n')
        file.write('    <P331>http://pbx-unc.bngf.ru/phonebook</P331>\n')
        file.write('    <P332>720</P332>\n    <P333>0</P333>\n    <P2914>0</P2914>\n')
        file.write('  </config>\n</gs_provision>')

    print("Created as %s" % fileName)


def makePanasonicConfig(name, secret, macAddress):
    fileName = macAddress

    with open(fileName, "w") as file:
        file.write('# Panasonic SIP Phone Standard Format File # DO NOT CHANGE THIS LINE!\n\n')

    with open(fileName, "a") as file:

        file.write('# System\nTIME_ZONE="300"\nDEFAULT_LANGUAGE="{0}"\nHTTPD_PORTOPEN_AUTO="Y"\n'.format(vars.phoneLang))
        file.write('ADMIN_PASS="{0}"\nNTP_ADDR="{1}"\nDISPLAY_TIME_PATTERN="2"\n\n'.format(vars.phoneAdminPass, vars.ntpServer))
        file.write('## Firmware Update Settings\nFIRM_UPGRADE_ENABLE="Y"\n\n')
        file.write('# VoIP\nPHONE_NUMBER_1="{0}"\nSIP_AUTHID_1="{0}"\nSIP_PASS_1="{1}"\n'.format(name, secret))
        file.write('SIP_RGSTR_ADDR_1="{0}"\nSIP_PRSNC_ADDR_1="{0}"\nSIP_OUTPROXY_ADDR_1="{0}"\n'.format(vars.pbxServer))
        file.write('SIP_SVCDOMAIN_1="example.com"\nREG_EXPIRE_TIME_1="600"\n\n')
        file.write('# Codecs\nCODEC_PRIORITY3_1="1"\nCODEC_PRIORITY1_1="2"\nCODEC_PRIORITY4_1="3"\n\n')
        file.write('## Provisioning Settings\nOPTION66_ENABLE="Y"\nOPTION66_REBOOT="Y"\nPROVISION_ENABLE="Y"\nCFG_CYCLIC="Y"\n')
        file.write('CFG_CYCLIC_INTVL="3600"\nVLAN_ENABLE="{0}"\nVLAN_ID_IP_PHONE="{1}"\n'.format(vars.vlanEnabled, vars.vlan))

    print("Created as %s" % fileName)

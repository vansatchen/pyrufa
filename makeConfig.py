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
        file.write('    <P332>720</P332>\n    <P333>0</P333>\n    <P2914>0</P2914>\n\n')
        file.write('<!-- Codecs g722,PCMA,PCMu,g729-->\n')
        file.write('    <P57>9</P57>\n    <P58>8</P58>\n    <P59>0</P59>\n    <P60>18</P60>\n\n')
        file.write('<!-- Disable custom grandstream headers-->\n')
        file.write('    <P26054>0</P26054>\n    <P26058>0</P26058>\n    <P26059>0</P26059\n')
        file.write('  </config>\n</gs_provision>')

    print("Created as %s" % fileName)


def makePanasonicConfig(name, secret, macAddress):
    fileName = macAddress

    with open(fileName, "w") as file:
        file.write('# Panasonic SIP Phone Standard Format File # DO NOT CHANGE THIS LINE!\n\n')

    with open(fileName, "a") as file:

        if vars.vlanEnabled:
            vars.vlanEnabled = "Y"
        else:
            vars.vlanEnabled = "N"
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


def makeYealinkConfig(name, secret, macAddress):
    fileName = macAddress + ".cfg"

    with open(fileName, "w") as file:
        file.write('#!version:1.0.0.1\n\n')

    with open(fileName, "a") as file:
        file.write('account.1.enable = 1\naccount.1.label = {0}\naccount.1.display_name = {0}\naccount.1.auth_name = {0}\n' .format(name))
        file.write('account.1.password = {0}\naccount.1.user_name = {1}\n'.format(secret, name))
        file.write('account.1.sip_server_host = {0}\naccount.X.sip_server.Y.transport_type = 0\n'.format(vars.pbxServer))
        file.write('account.X.sip_server.1.expires = 3600\naccount.X.sip_server.1.retry_counts = 3\n\n')
        file.write('network.ip_address_mode = 0\nnetwork.internet_port.type = 0\nnetwork.lldp.enable = 0\n')
        file.write('network.vlan.dhcp_enable = {0}\nnetwork.vlan.dhcp_option = {1}\n'.format(vars.vlanEnabled, vars.vlan))
        file.write('local_time.time_zone = +5\nlocal_time.summer_time = 0\nlocal_time.manual_ntp_srv_prior = 0\n')
        file.write('local_time.ntp_server1 = {0}\nlocal_time.interval = 1000\n'.format(vars.ntpServer))
        file.write('local_time.time_format = 1\nlocal_time.date_format = 1\n')
        file.write('security.user_password = admin:{0}\nsecurity.user_password = user:{1}\n\n'.format(vars.phoneAdminPass, vars.phoneUserPass))
        file.write('account.1.codec.1.payload_type = g722\naccount.1.codec.1.rtpmap = 9\naccount.1.codec.1.enable = 1\n\n')
        file.write('account.1.codec.2.payload_type = PCMA\naccount.1.codec.2.rtpmap = 8\naccount.1.codec.2.enable = 1\n\n')
        file.write('account.1.codec.3.payload_type = PCMU\naccount.1.codec.3.rtpmap = 0\naccount.1.codec.3.enable = 1\n')

    print("Created as %s" % fileName)

import vars

def makeConfig(name, secret, macAddress):
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
        file.write('    <P331>http://%s/phonebook</P331>\n' % vars.pbxServer)
        file.write('    <P332>720</P332>\n    <P333>0</P333>\n    <P2914>0</P2914>\n')
        file.write('  </config>\n</gs_provision>')

    print("Created as %s" % fileName)

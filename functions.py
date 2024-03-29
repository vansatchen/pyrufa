import sys
import os
import httplib2
import mysqlFunc
import makeConfig
import vars

def checkCancel(string):
    if string == "quit":
        print("\033[36mCanceled. Exiting.\033[0m")
        sys.exit(0)

def addAccount(defaultContext):
    context = input("Group(context)[\033[33m%s\033[0m]: " % defaultContext)
    if context == "": context = defaultContext
    checkCancel(context)

    checkOk = False
    while checkOk == False:
        name = input("Name/number: ")
        if name == "":
            continue
        elif len(name) != vars.lenName or not name.isdigit():
            checkCancel(name)
            print("\033[31mName/number must have %s digitals only, please enter another\033[0m" % vars.lenName)
            continue

        db = mysqlFunc.Database()
        checkName = db.checkNameNotExists(name)
        if not checkName:
            print("\033[31mName/number %s already exists, please enter another\033[0m" % name)
        else:
            checkOk = True

    secret = input("Secret word[\033[33m%s%s\033[0m]: " % (name, vars.defaultData)).strip()
    if secret == "": secret = name + vars.defaultData
    checkCancel(secret)

    callerIDName = input("Callerid(\033[31mwithout number\033[0m)[\033[33m%s\033[0m]: " % name)
    if callerIDName == "": callerID = name
    else:
        checkCancel(callerIDName)
        callerID = callerIDName + " <" + name + ">"

    db.addAccount(context, name, secret, callerID)

def delAccount():
    checkOk = False
    while checkOk == False:
        name = input("Name/number: ")
        if name == "":
            continue
        elif len(name) != vars.lenName or not name.isdigit():
            checkCancel(name)
            print("\033[31mName/number must have %s digitals only, please enter another\033[0m" % vars.lenName)
            continue

        db = mysqlFunc.Database()
        checkName = db.checkNameNotExists(name)
        if checkName:
            print("\033[31mName/number %s not exists, please enter another\033[0m" % name)
        else:
            checkOk = True

    db.delAccount(name)

def editAccount():
    updateAccount = False
    checkOk = False
    while checkOk == False:
        name = input("Name/number to edit: ")
        if name == "":
            continue
        elif len(name) != vars.lenName or not name.isdigit():
            checkCancel(name)
            print("\033[31mName/number must have %s digitals only, please enter another\033[0m" % vars.lenName)
            continue

        db = mysqlFunc.Database()
        checkName = db.checkNameNotExists(name)
        if checkName:
            print("\033[31mName/number %s not exists, please enter another\033[0m" % name)
        else:
            checkOk = True

    oldContext = db.getValue(name, "context")
    newContext = input("New group(context)[\033[33m%s\033[0m]: " % oldContext)
    if newContext == "":
        newContext = oldContext
    else:
        updateAccount = True
    checkCancel(newContext)

    checkOk = False
    while checkOk == False:
        newName = input("New name/number[\033[33m%s\033[0m]: " % name)
        if newName == "":
            newName = name
            checkOk = True
            continue
        elif len(newName) != vars.lenName or not newName.isdigit():
            checkCancel(newName)
            print("\033[31mName/number must have %s digitals only, please enter another\033[0m" % vars.lenName)
            continue

        db = mysqlFunc.Database()
        checkName = db.checkNameNotExists(name)
        if not checkName:
            print("\033[31mName/number %s already exists, please enter another\033[0m" % newName)
        else:
            checkOk = True
            updateAccount = True

    if name == newName:
        oldSecret = db.getValue(name, "password")
    else:
        oldSecret = newName + vars.defaultData
    newSecret = input("New secret word[\033[33m%s\033[0m]: " % oldSecret).strip()
    if newSecret == "":
        newSecret = oldSecret
    else:
        updateAccount = True
    checkCancel(newSecret)

    oldCallerID = db.getValue(name, "callerid")
    if name != newName:
        oldCallerID = oldCallerID.replace(name, newName)
    newCallerID = input("New callerid(\033[31mwithout number\033[0m)[\033[33m%s\033[0m]: " % oldCallerID)
    if newCallerID == "":
        newCallerID = oldCallerID
    else:
        newCallerID = newCallerID + " <" + newName + ">"
        updateAccount = True
    checkCancel(newSecret)

    checkOk = False
    while checkOk == False:
        oldMaxContacts = db.getValue(name, "max_contacts")
        newMaxContacts = input("New max_contacts[\033[33m%s\033[0m]: " % oldMaxContacts)
        if newMaxContacts == "":
            newMaxContacts = oldMaxContacts
            checkOk = True
            continue
        elif not newMaxContacts.isdigit():
            checkCancel(newMaxContacts)
            print("\033[31mMax_contacts must be number.\033[0m")
        else:
            checkOk = True
            updateAccount = True
        checkCancel(newMaxContacts)

    oldPickupGroup = db.getValue(name, "named_pickup_group")
    newPickupGroup = input("New Pickup group[\033[33m%s\033[0m]: " % oldPickupGroup).strip()
    if newPickupGroup == "":
        newPickupGroup = oldPickupGroup
    else:
        updateAccount = True
    checkCancel(newPickupGroup)

    if updateAccount == True:
        db = mysqlFunc.Database()
        db.editAccount(name, newContext, newName, newSecret, newCallerID, newMaxContacts, newPickupGroup)

def showAccounts(option):
    db = mysqlFunc.Database()
    data = db.showAccounts(option)
    contextLen = 0
    passwordLen = 0
    countOnline, countOffline = 0, 0

    if data:
        for row in data:
            if len(row[0]) > contextLen: contextLen = len(row[0])
            if len(row[2]) > passwordLen: passwordLen = len(row[2])

        if contextLen <= 7:
            contextLen = 7
            contextCol = " "
        else: contextCol = " " * (contextLen - 6)
        if passwordLen <= 8:
            passwordLen = 8
            passwordCol = " "
        else: passwordCol = " " * (passwordLen - 7)
        boards = "+" + "="*(contextLen+2) + "+" + "="*(vars.lenName+2) + "+" + "="*(passwordLen+2) + "+" + "="*42 + "+" + "="*32 + "+" + "="*17 + "+"
        print(boards)
        print("| Context" + contextCol + "| Name " + "| Password" + passwordCol + "| CallerID" + " "*33 + "| Agent" + " "*26 + "| IP" + " "*14 + "|")
        print(boards)

        for row in data:
            if row[4] is None:
                agent = ip = "Offline"
                countOffline += 1
            else:
                agent = row[4]
                ip = row[5]
                countOnline += 1
            print("|", row[0].ljust(contextLen), "|", row[1].ljust(vars.lenName), "|", row[2].ljust(passwordLen), "|", row[3][:40].ljust(40), \
                  "|", agent[:30].ljust(30), "|", ip[:15].ljust(15), "|")
        print(boards)
        print("Online : " + str(countOnline) + "\nOffline: " + str(countOffline))

def showAccount():
    checkOk = False
    while checkOk == False:
        name = input("Name/number: ")
        if name == "":
            continue
        elif len(name) != vars.lenName or not name.isdigit():
            checkCancel(name)
            print("\033[31mName/number must have %s digitals only, please enter another\033[0m" % vars.lenName)
            continue
        else:
            db = mysqlFunc.Database()
            checkName = db.checkNameNotExists(name)
            if checkName:
                print("\033[31mName/number %s not exists, please enter another\033[0m" % name)
            else: checkOk = True

    db = mysqlFunc.Database()
    data = db.showAccount(name)
    optionLen = vars.lenName
    optionsName = ("Number", "Transport", "Context", "Codecs", "DTMF", "Media encryption", "CallerID", "Call group", "Pickup group", "Password", "User agent", "IP address")

    for account in data:
        for row in account:
            if row == None: continue
            if len(row) > optionLen: optionLen = len(row)

        boards = "+" + "="*19 + "+" + "="*(optionLen+4) + "+"
        print(boards)
        i = 0
        while i < len(optionsName):
            if account[i] == None:
                optionData = ""
            else: optionData = account[i]
            if optionsName[i] == "IP address" and account[i] == None:
                optionData = "Offline"
            print("| " + optionsName[i].ljust(17) + " | " + optionData.ljust(optionLen+2) + " |")
            i += 1

        print(boards)

def showContexts():
    print("")
    db = mysqlFunc.Database()
    data = db.showAccounts("callerid")
    contextsList = []

    if data:
        for row in data:
            contextsList.append(row[0])
    contextsSet = sorted(list(set(contextsList)))
    contextsSetIndex = 0

    for context in contextsSet:
        print(str(contextsSetIndex + 1) + ") " + context)
        contextsSetIndex += 1

    checkOk = False
    while checkOk == False:
        contextNum = input("Context number: ")
        if contextNum.isdigit():
            if int(contextNum) > len(contextsSet):
                print("\033[31mContext number is out of range\033[0m")
            else: checkOk = True
        else:
            print("\033[31mContext number is not a number\033[0m")
        checkCancel(contextNum)

    data = db.showContext(contextsSet[int(contextNum) - 1])
    contextLen = 0
    passwordLen = 0
    countOnline, countOffline = 0, 0

    if data:
        for row in data:
            if len(row[0]) > contextLen: contextLen = len(row[0])
            if len(row[2]) > passwordLen: passwordLen = len(row[2])

        if contextLen <= 7:
            contextLen = 7
            contextCol = " "
        else: contextCol = " " * (contextLen - 6)
        if passwordLen <= 8:
            passwordLen = 8
            passwordCol = " "
        else: passwordCol = " " * (passwordLen - 7)
        boards = "+" + "="*(contextLen+2) + "+" + "="*(vars.lenName+2) + "+" + "="*(passwordLen+2) + "+" + "="*42 + "+" + "="*32 + "+" + "="*17 + "+"
        print(boards)
        print("| Context" + contextCol + "| Name " + "| Password" + passwordCol + "| CallerID" + " "*33 + "| Agent" + " "*26 + "| IP" + " "*14 + "|")
        print(boards)

        for row in data:
            if row[4] is None:
                agent = ip = "Offline"
                countOffline += 1
            else:
                agent = row[4]
                ip = row[5]
                countOnline += 1
            print("|", row[0].ljust(contextLen), "|", row[1].ljust(vars.lenName), "|", row[2].ljust(passwordLen), "|", row[3][:40].ljust(40), \
                  "|", agent[:30].ljust(30), "|", ip[:15].ljust(15), "|")
        print(boards)
        print("Online : " + str(countOnline) + "\nOffline: " + str(countOffline))


def mkConfig(vendorNum):
    checkOk = False
    while checkOk == False:
        name = input("Name/number: ")
        if name == "":
            continue
        elif len(name) != vars.lenName or not name.isdigit():
            checkCancel(name)
            print("\033[31mName/number must have %s digitals only, please enter another one\033[0m" % vars.lenName)
            continue

        db = mysqlFunc.Database()
        checkName = db.checkNameNotExists(name)
        if checkName:
            print("\033[31mName/number %s not exists, please enter another one\033[0m" % name)
            continue
        else:
            checkOk = True

        if db.existInConfigs("name", name):
            answer = input("\033[31mNumber exists as associasion. Continue?[y/N]: \033[0m")
            if answer == "" or answer.lower() == "n":
                checkOk = False
            else:
                checkOk = True
        else:
            checkOk = True
    checkCancel(name)

    checkOk = False
    while checkOk == False:
        macAddress = input("Mac-address or \"\033[33mquit\033[0m\" to quit: ").lower().replace(":", "").replace(" ", "")
        checkCancel(macAddress)
        if len(macAddress) != 12:
            print("\033[31mMac-address must have 12 characters only(without colons).\033[0m")
        elif os.path.isfile(vars.cfgLocation + "cfg" + macAddress + ".xml"):
            answer = input("\033[36mConfig file in directory exists. Continue?[y/N]: \033[0m")
            if answer == "" or answer.lower() == "n":
                checkOk = False
            else:
                checkOk = True
        else:
            checkOk = True

        if db.existInConfigs("macAddress", macAddress):
            answer = input("\033[31mMac address exists as associasion. Continue?[y/N]: \033[0m")
            if answer == "" or answer.lower() == "n":
                checkOk = False
            else:
                checkOk = True
        else:
            checkOk = True
    checkCancel(macAddress)

    answer = input("\033[36mUse vlan 132?[Y/n]: \033[0m")
    checkCancel(answer)
    if answer == "" or answer.lower() == "y":
        vlanUsed = vars.vlan
    else:
        vlanUsed = 0

    secret = db.getValue(name, "password")
    if vendorNum == "1":
        makeConfig.makeGrandstreamConfig(name, secret, macAddress, vlanUsed)
        db.makeProvisioningAssociates(name, macAddress, vlanUsed)
    elif vendorNum == "2":
        makeConfig.makePanasonicConfig(name, secret, macAddress, vlanUsed)
    else:
        makeConfig.makeYealinkConfig(name, secret, macAddress, vlanUsed)

def rebootPhone():
    h = httplib2.Http("/tmp/cache")
    checkOk = False
    while checkOk == False:
        address = input("Enter ip or dns address: ").replace(" ", "")
        checkCancel(address)
        if address != "": checkOk = True

    checkOk = False
    while checkOk == False:
        password = input("Password?[\033[33m%s\033[0m]: " % vars.adminPass)
        checkCancel(password)
        if password == "": password = vars.adminPass

        try:
            request = "/cgi-bin/api-sys_operation?passcode=" + password + "&request=REBOOT"
            resp_headers, content = h.request("http://" + address + request, "GET")
        except:
            print("No route to host")
            return

        content = content.decode()
        if 'Unauthorized' in content:
            print("\033[31mInvalid password: Unauthorized\033[0m")
            continue
        elif '"response":"error"' in content:
            print("\033[31mError: authentication required\033[0m")
            continue
        elif "success" in content:
            print("\033[36mDone\033[0m")
            return
        else:
            print("\033[31mUnknown request: \033[0m")
            print(content)

        print(content)
        checkOk = True

def addToBlacklist():
    db = mysqlFunc.Database()
    checkNum = False
    while checkNum == False:
        number = input("Number to add[quit]: ")
        if number == "": number = "quit"
        if not number.isdecimal():
            checkCancel(number)
            print("\033[31mNumber must be numeric!\033[0m")
        else:
            if db.existInBlacklist(number):
                print("\033[31mNumber exists!\033[0m")
            else: checkNum = True

    db.addToBlacklist(number)

def delFromBlacklist():
    db = mysqlFunc.Database()
    checkNum = False
    while checkNum == False:
        number = input("Number to delete[quit]: ")
        if number == "": number = "quit"
        if not number.isdecimal():
            checkCancel(number)
            print("\033[31mNumber must be numeric!\033[0m")
        else:
            if not db.existInBlacklist(number):
                print("\033[31mNumber is not exists!\033[0m")
            else: checkNum = True

    db.delFromBlacklist(number)

def showBlacklist():
    db = mysqlFunc.Database()
    data = db.showBlacklist()

    numberLen = 0

    if data:
        for row in data:
            if len(row[0]) > numberLen: numberLen = len(row[0])
        if numberLen < 8: numberLen = 8

        boards = "+" + "="*(numberLen+2) + "+"
        print(boards)
        print("|" + " number " + " "*(numberLen-6) + "|")
        print(boards)

        for row in data:
            print("| " + row[0] + " "*(numberLen-len(row[0])) + " |")

        print(boards)
    else: print("Empty")

def showProvisioningAssociates(option):
    db = mysqlFunc.Database()
    data = db.showProvisioningAssociates(option)

    numberLen = 0
    vlanLen = 0
    count = 0

    if data:
        for row in data:
            if len(row[0]) > numberLen: numberLen = len(row[0])
            if len(row[2]) > vlanLen: vlanLen = len(row[2])
        if numberLen < 6: numberLen = 6
        if vlanLen < 4: vlanLen = 4

        boards = "+" + "="*(numberLen+2) + "+" + "="*14 + "+" + "="*(vlanLen+2) + "+"
        print("\n" + boards)
        print("|" + " number " + " "*(numberLen-6) + "|" + " mac address  " + "|" + " vlan " + "|")
        print(boards)

        for row in data:
            print("| " + row[0] + " "*(numberLen-len(row[0])) + " | " + row[1] + " | " + row[2] + " "*(vlanLen-len(row[2])) + " |")
            count += 1

        print(boards)
        print("Total: " + str(count))
    else: print("Empty")

def delProvisioningAssociate():
    db = mysqlFunc.Database()
    checkOk = False
    while checkOk == False:
        name = input("Name/number: ")
        if name == "":
            continue
        elif len(name) != vars.lenName or not name.isdigit():
            checkCancel(name)
            print("\033[31mName/number must have %s digitals only, please enter another one\033[0m" % vars.lenName)
            continue

        checkName = db.existInConfigs("name", name)
        if not checkName:
            print("\033[31mName/number %s not exists, please enter another one\033[0m" % name)
        else:
            checkOk = True

    db.deleteProvisioningAssociate(name)

def editProvisioningAssociate():
    db = mysqlFunc.Database()
    updateConfig = False
    checkOk = False
    while checkOk == False:
        name = input("Name/number to edit: ")
        if name == "":
            continue
        elif len(name) != vars.lenName or not name.isdigit():
            checkCancel(name)
            print("\033[31mName/number must have %s digitals only, please enter another\033[0m" % vars.lenName)
            continue

        checkName = db.existInConfigs("name", name)
        if not checkName:
            print("\033[31mName/number %s not exists, please enter another\033[0m" % name)
            continue
        else:
            checkOk = True

    oldMacAddresses = db.getConfig(name)
    checkOk = False
    while checkOk == False:
        if len(oldMacAddresses) < 2:
            newMacAddress = input("New mac address[\033[33m%s\033[0m] or \"\033[33mquit\033[0m\" to quit: " % oldMacAddresses[0][1]).lower().replace(":", "").replace(" ", "")
            if newMacAddress == '':
                newMacAddress = oldMacAddresses[0][1]
                oldMacAddress = newMacAddress
                break
            else:
                checkCancel(newMacAddress)
                if len(newMacAddress) != 12:
                    print("\033[31mMac-address must have 12 characters only(without colons).\033[0m")
                    continue
                else:
                     oldMacAddress = oldMacAddresses[0][1]
                     checkOk = True
                     updateConfig = True
        else:
            for i in range(0, len(oldMacAddresses)):
                print(str(i+1) + ") " + str(oldMacAddresses[i][1]))
            try:
                macAddress = int(input("Editing mac address: "))
                assert 0 < macAddress < len(oldMacAddresses)+1
            except:
                print("\033[33mIgnoring invalid value. Editing mac address is: \033[0m" + oldMacAddresses[0][1])
                macAddress = 1
                oldMacAddress = oldMacAddresses[0][1]

            newMacAddress = input("New mac address[\033[33m%s\033[0m] or \"\033[33mquit\033[0m\" to quit: " % oldMacAddresses[int(macAddress)-1][1]).lower().replace(":","").replace(" ", "")
            if newMacAddress == '':
                newMacAddress = oldMacAddresses[int(macAddress)-1][1]
                oldMacAddress = newMacAddress
                break
            else:
                checkCancel(newMacAddress)
                if len(newMacAddress) != 12:
                    print("\033[31mMac-address must have 12 characters only(without colons).\033[0m")
                    continue
                else:
                    oldMacAddress = oldMacAddresses[int(macAddress)-1][1]
                    checkOk = True
                    updateConfig = True

    for assoc in oldMacAddresses:
        if oldMacAddress == assoc[1]:
            oldVlan = assoc[2]
    variants = "Y/n"
    if oldVlan == '0': variants = "N/y"
    answer = input("\033[36mUse vlan 132?[%s]: \033[0m" % variants)
    checkCancel(answer)
    if answer == "" or answer.lower() == variants.split('/')[0].lower():
        vlanUsed = oldVlan
    else:
        if answer != variants.split('/')[1].lower():
            print("\033[33mIgnoring invalid value. Using default variant.\033[0m")
            vlanUsed = oldVlan
        elif answer.lower() == "y": vlanUsed = vars.vlan
        elif answer.lower() == "n": vlanUsed = "0"
        updateConfig = True

    if updateConfig:
        db.editProvisioningAssociate(name, oldMacAddress, newMacAddress, vlanUsed)
    else:
        print("\033[33mNo changes. Exiting.\033[0m")

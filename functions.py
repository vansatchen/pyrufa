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

        checkName = mysqlFunc.checkNameNotExists(name)
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

    mysqlFunc.addAccount(context, name, secret, callerID)

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

        checkName = mysqlFunc.checkNameNotExists(name)
        if checkName:
            print("\033[31mName/number %s not exists, please enter another\033[0m" % name)
        else:
            checkOk = True

    mysqlFunc.delAccount(name)

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

        checkName = mysqlFunc.checkNameNotExists(name)
        if checkName:
            print("\033[31mName/number %s not exists, please enter another\033[0m" % name)
        else:
            checkOk = True

    oldContext = mysqlFunc.getValue(name, "context")
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

        checkName = mysqlFunc.checkNameNotExists(newName)
        if not checkName:
            print("\033[31mName/number %s already exists, please enter another\033[0m" % newName)
        else:
            checkOk = True
            updateAccount = True

    if name == newName:
        oldSecret = mysqlFunc.getValue(name, "password")
    else:
        oldSecret = newName + vars.defaultData
    newSecret = input("New secret word[\033[33m%s\033[0m]: " % oldSecret).strip()
    if newSecret == "":
        newSecret = oldSecret
    else:
        updateAccount = True
    checkCancel(newSecret)

    oldCallerID = mysqlFunc.getValue(name, "callerid")
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
        oldMaxContacts = mysqlFunc.getValue(name, "max_contacts")
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

    if updateAccount == True:
        mysqlFunc.editAccount(name, newContext, newName, newSecret, newCallerID, newMaxContacts)

def showAccounts(option):
    mysqlFunc.showAccounts(option)

def mkConfig():
    checkOk = False
    while checkOk == False:
        name = input("Name/number: ")
        if name == "":
            continue
        elif len(name) != vars.lenName or not name.isdigit():
            checkCancel(name)
            print("\033[31mName/number must have %s digitals only, please enter another\033[0m" % vars.lenName)
            continue

        checkName = mysqlFunc.checkNameNotExists(name)
        if checkName:
            print("\033[31mName/number %s not exists, please enter another\033[0m" % name)
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
            answer = input("\033[36mConfig file exists. Continue?[y/N]: \033[0m")
            if answer == "" or answer.lower() == "n":
                checkOk = False
            else:
                checkOk = True
        else:
            checkOk = True

    secret = mysqlFunc.getValue(name, "password")
    makeConfig.makeConfig(name, secret, macAddress)

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

        request = "/cgi-bin/api-sys_operation?passcode=" + password + "&request=REBOOT"
        resp_headers, content = h.request("http://" + address + request, "GET")
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

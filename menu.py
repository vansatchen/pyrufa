import sys
import functions
import mysqlFunc

def showMenu():
    print("\n1) Show by name")
    print("2) Show by callerID")
    print("3) Show by status")
    print("4) Show account")
    print("5) Show context\'s users")
    print("0) back")

    choiceShow = input("Please enter an action[1]: ")

    if choiceShow == "1":
        functions.showAccounts("username")
    elif choiceShow == "2":
        functions.showAccounts("callerid")
    elif choiceShow == "3":
        functions.showAccounts("via_addr DESC")
    elif choiceShow == "4":
        functions.showAccount()
    elif choiceShow == "5":
        functions.showContexts()
    elif choiceShow == "0":
        return
    elif choiceShow == "":
        functions.showAccounts("username")
    else:
        functions.checkCancel(choiceShow)
        print("\033[31mI don't understand your choice.\033[0m")
        choiceShow = '0'

def makeConfigMenu():
    print("1) For Grandstream")
    print("2) For Panasonic")
    print("3) For Yealink")

    choiceMenu = input("Please enter vendor[1]: ")

    if choiceMenu == "1" or choiceMenu == "":
        functions.mkConfig("1")
    elif choiceMenu == "2" or choiceMenu == "3":
        functions.mkConfig(choiceMenu)
    else:
        functions.checkCancel(choiceMenu)
        print("\033[31mI don't understand your choice.\033[0m")
        choiceMenu = '0'

def blacklistMenu():
    while True:
        print("\n1) Add")
        print("2) Delete")
        print("3) Show")
        print("0) back")

        choiceBl = input("Please enter an action[quit]: ")

        if choiceBl =="1":
            functions.addToBlacklist()
        elif choiceBl =="2":
            functions.delFromBlacklist()
        elif choiceBl =="3":
            functions.showBlacklist()
        elif choiceBl == "0":
            return
        elif choiceBl =="":
            print("\033[36mNo action. Exiting\033[0m\n")
            sys.exit(0)
        else:
            functions.checkCancel(choiceBL)
            print("\033[31mI don't understand your choice.\033[0m")
            choiceBL ='0'

def provisioningMenu():
    while True:
        print("\n1) Make associate number + mac address")
        print("2) Delete associate")
        print("3) Edit associate")
        print("4) Show associates order by number")
        print("5) Show associates order by mac address")
        print("0) back")

        choicePM = input("Please enter an action[quit]: ")

        if choicePM =="1":
            makeConfigMenu()
        elif choicePM =="2":
            functions.delProvisioningAssociate()
        elif choicePM =="3":
            functions.editProvisioningAssociate()
        elif choicePM =="4":
            functions.showProvisioningAssociates("name")
        elif choicePM =="5":
            functions.showProvisioningAssociates("macAddress")
        elif choicePM =="0":
            return
        elif choicePM =="":
            print("\033[36mNo action. Exiting\033[0m\n")
            sys.exit(0)
        else:
            functions.checkCancel(choice)
            print("\033[31mI don't understand your choice.\033[0m")
            choice ='0'

def mainMenu(defaultContext):
    while True:
        print("\n1) Add")
        print("2) Delete")
        print("3) Edit")
        print("4) Show")
        print("5) Provisioning")
        print("6) Reboot telephone")
        print("7) Blacklist")

        choice = input("Please enter an action[quit]: ")

        if choice =="1":
            functions.addAccount(defaultContext)
        elif choice =="2":
            functions.delAccount()
        elif choice =="3":
            functions.editAccount()
        elif choice =="4":
            showMenu()
        elif choice =="5":
            provisioningMenu()

#            while True:
#                answer = input("\033[36mMake another one?[Y/n]: \033[0m")
#                functions.checkCancel(answer)
#                if answer == "" or answer.lower() == "y":
#                    makeConfigMenu()
#                else:
#                    break

        elif choice =="6":
            functions.rebootPhone()

            while True:
                answer = input("\033[36mReboot another one?[Y/n]: \033[0m")
                functions.checkCancel(answer)
                if answer == "" or answer.lower() == "y":
                    functions.rebootPhone()
                else:
                    break

        elif choice =="7":
            blacklistMenu()

        elif choice =="":
            print("\033[36mNo action. Exiting\033[0m\n")
            sys.exit(0)
        else:
            functions.checkCancel(choice)
            print("\033[31mI don't understand your choice.\033[0m")
            choice ='0'

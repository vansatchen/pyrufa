import sys
import functions
import mysqlFunc

def showMenu():
    print("\n1) Show by name")
    print("2) Show by callerID")
    print("3) Show by status")
    print("4) Show account")
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

    choiceMenu = input("Please enter vendor[1]: ")

    if choiceMenu == "1" or choiceMenu == "":
        functions.mkConfig("1")
    elif choiceMenu == "2":
        functions.mkConfig("2")
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
        elif choiceBL =="":
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
        print("5) Make config")
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
            makeConfigMenu()

            while True:
                answer = input("\033[36mMake another one?[Y/n]: \033[0m")
                functions.checkCancel(answer)
                if answer == "" or answer.lower() == "y":
                    makeConfigMenu()
                else:
                    break

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

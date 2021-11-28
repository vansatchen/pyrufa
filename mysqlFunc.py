import MySQLdb
import sys
import vars

def checkNameNotExists(name):
    try:
        db = MySQLdb.connect(user = vars.dbUser, passwd = vars.dbPass, host = vars.dbHost, db = vars.dataBase, charset = vars.dbCharset)
        cursor = db.cursor()
        cursor.execute("SELECT username FROM ps_auths WHERE username = %s", (name,))
        data = cursor.fetchall()
        return False if data else True
    except:
        print("\033[31mConnection to MySQL error. Exiting.\033[0m")
        sys.exit(1)
    finally:
        if db: db.close()

def addAccount(context, name, secret, callerID):
    try:
        db = MySQLdb.connect(user = vars.dbUser, passwd = vars.dbPass, host = vars.dbHost, db = vars.dataBase, charset = vars.dbCharset)
        cursor = db.cursor()
        cursor.execute("INSERT INTO ps_aors (id,max_contacts) VALUES (%s,'1')", (name,))
        cursor.execute("INSERT INTO ps_auths (id,auth_type,password,username) \
                        VALUES (%s,'userpass',%s,%s)", (name, secret, name))
        cursor.execute("INSERT INTO ps_endpoints (id,aors,auth,context,callerid,mailboxes) \
                        VALUES (%s,%s,%s,%s,%s,%s'@'%s)", (name, name, name, context, callerID, name, context))
        db.commit()
        print("\033[36mDone.\033[0m")
    except:
        if db: db.rollback()
        print("\033[31mWrite to MySQL error. Exiting.\033[0m")
        sys.exit(1)
    finally:
        if db: db.close()

def delAccount(name):
    try:
        db = MySQLdb.connect(user = vars.dbUser, passwd = vars.dbPass, host = vars.dbHost, db = vars.dataBase, charset = vars.dbCharset)
        cursor = db.cursor()
        cursor.execute("DELETE FROM ps_aors WHERE id = %s", (name,))
        cursor.execute("DELETE FROM ps_auths WHERE id = %s", (name,))
        cursor.execute("DELETE FROM ps_endpoints WHERE id = %s", (name,))
        db.commit()
        print("\033[36mDone.\033[0m")
    except:
        if db: db.rollback()
        print("\033[31mWrite to MySQL error. Exiting.\033[0m")
        sys.exit(1)
    finally:
        if db: db.close()

def getValue(value, option):
    if option == "context" or option == "callerid": table = "ps_endpoints"
    elif option == "max_contacts": table = "ps_aors"
    else: table = "ps_auths"
    try:
        db = MySQLdb.connect(user = vars.dbUser, passwd = vars.dbPass, host = vars.dbHost, db = vars.dataBase, charset = vars.dbCharset)
        cursor = db.cursor()
        cursor.execute("SELECT %s FROM %s WHERE id = %s" % (option, table, value))
        data = cursor.fetchall()
        return data[0][0]
    except:
        print("\033[31mConnection to MySQL error. Exiting.\033[0m")
        sys.exit(1)
    finally:
        if db: db.close()

def editAccount(name, newContext, newName, newSecret, newCallerID, newMaxContacts):
    try:
        db = MySQLdb.connect(user = vars.dbUser, passwd = vars.dbPass, host = vars.dbHost, db = vars.dataBase, charset = vars.dbCharset)
        cursor = db.cursor()
        cursor.execute("UPDATE ps_aors SET id = %s, max_contacts = %s WHERE id = %s", (newName, newMaxContacts, name))
        cursor.execute("UPDATE ps_auths SET id = %s, username = %s, password = %s WHERE id = %s", (newName, newName, newSecret, name))
        cursor.execute("UPDATE ps_endpoints SET context = %s, mailboxes = %s'@'%s, id = %s, aors = %s, auth = %s, callerid = %s \
                        WHERE id = %s", (newContext, newName, newContext, newName, newName, newName, newCallerID, name))
        db.commit()
        print("\033[36mDone.\033[0m")
    except:
        if db: db.rollback()
        print("\033[31mWrite to MySQL error. Exiting.\033[0m")
        sys.exit(1)
    finally:
        if db: db.close()

def showAccounts(option):
    contextLen = 0
    passwordLen = 0

    try:
        db = MySQLdb.connect(user = vars.dbUser, passwd = vars.dbPass, host = vars.dbHost, db = vars.dataBase, charset = vars.dbCharset)
        cursor = db.cursor()
        cursor.execute("SELECT ps_endpoints.context, ps_auths.username, ps_auths.password, ps_endpoints.callerid, "
                       "ps_contacts.user_agent, ps_contacts.via_addr FROM ps_auths INNER JOIN "
                       "ps_endpoints USING(id) LEFT JOIN ps_contacts ON ps_auths.username = "
                       "ps_contacts.endpoint ORDER BY %s" % option)
        data = cursor.fetchall()
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
            else:
                agent = row[4]
                ip = row[5]
            print("|", row[0].ljust(contextLen), "|", row[1].ljust(vars.lenName), "|", row[2].ljust(passwordLen), "|", row[3][:40].ljust(40), \
                  "|", agent[:30].ljust(30), "|", ip[:15].ljust(15), "|")
        print(boards)
    except:
        print("\033[31mConnection to MySQL error. Exiting.\033[0m")
        sys.exit(1)
    finally:
        if db: db.close()

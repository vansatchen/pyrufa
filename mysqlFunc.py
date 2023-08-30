import MySQLdb
import sys
import vars

class Database:
    host = vars.dbHost
    user = vars.dbUser
    passwd = vars.dbPass
    db = vars.dataBase
    charset = vars.dbCharset

    def __init__(self):
        try:
            self.db = MySQLdb.connect(user = self.user, passwd = self.passwd, host = self.host, db = self.db, charset = self.charset)
            self.cursor = self.db.cursor()
        except:
            print("\033[31mConnection to MySQL error. Exiting.\033[0m")
            sys.exit(1)

    def checkNameNotExists(self, name):
        self.cursor.execute("SELECT username FROM ps_auths WHERE username = %s", (name,))
        data = self.cursor.fetchall()
        return False if data else True

    def addAccount(self, context, name, secret, callerID):
        self.cursor.execute("INSERT INTO ps_aors (id,max_contacts) VALUES (%s,'1')", (name,))
        self.cursor.execute("INSERT INTO ps_auths (id,auth_type,password,username) \
                            VALUES (%s,'userpass',%s,%s)", (name, secret, name))
        self.cursor.execute("INSERT INTO ps_endpoints (id,aors,auth,context,callerid,mailboxes) \
                            VALUES (%s,%s,%s,%s,%s,%s'@'%s)", (name, name, name, context, callerID, name, context))
        self.db.commit()
        print("\033[36mDone.\033[0m")

    def delAccount(self, name):
        self.cursor.execute("DELETE FROM ps_aors WHERE id = %s", (name,))
        self.cursor.execute("DELETE FROM ps_auths WHERE id = %s", (name,))
        self.cursor.execute("DELETE FROM ps_endpoints WHERE id = %s", (name,))
        self.db.commit()
        print("\033[36mDone.\033[0m")

    def getValue(self, value, option):
        if option == "context" or option == "callerid" or option == "named_pickup_group": table = "ps_endpoints"
        elif option == "max_contacts": table = "ps_aors"
        else: table = "ps_auths"
        self.cursor.execute("SELECT %s FROM %s WHERE id = %s" % (option, table, value))
        data = self.cursor.fetchall()
        return data[0][0]

    def editAccount(self, name, newContext, newName, newSecret, newCallerID, newMaxContacts, newPickupGroup):
        self.cursor.execute("UPDATE ps_aors SET id = %s, max_contacts = %s WHERE id = %s", (newName, newMaxContacts, name))
        self.cursor.execute("UPDATE ps_auths SET id = %s, username = %s, password = %s WHERE id = %s",
                           (newName, newName, newSecret, name))
        self.cursor.execute("UPDATE ps_endpoints SET context = %s, mailboxes = %s'@'%s, id = %s, \
                             aors = %s, auth = %s, callerid = %s, named_call_group = %s, named_pickup_group = %s WHERE id = %s",
                           (newContext, newName, newContext, newName, newName, newName, newCallerID,
                            newPickupGroup, newPickupGroup, name))
        self.db.commit()
        print("\033[36mDone.\033[0m")

    def showAccounts(self, option):
        self.cursor.execute("SELECT ps_endpoints.context, ps_auths.username, ps_auths.password, ps_endpoints.callerid, "
                            "ps_contacts.user_agent, ps_contacts.via_addr FROM ps_auths INNER JOIN "
                            "ps_endpoints USING(id) LEFT JOIN ps_contacts ON ps_auths.username = "
                            "ps_contacts.endpoint ORDER BY %s" % option)
        return self.cursor.fetchall()

    def showAccount(self, account):
        self.cursor.execute("SELECT ps_endpoints.id, ps_endpoints.transport, ps_endpoints.context, ps_endpoints.allow, "
                            "ps_endpoints.dtmf_mode, ps_endpoints.media_encryption, ps_endpoints.callerid, "
                            "ps_endpoints.named_call_group, ps_endpoints.named_pickup_group, ps_auths.password, "
                            "ps_contacts.user_agent, ps_contacts.via_addr FROM ps_auths INNER JOIN "
                            "ps_endpoints USING(id) LEFT JOIN ps_contacts ON ps_auths.username = "
                            "ps_contacts.endpoint where ps_auths.username = '%s' ORDER BY username" % account);
        return self.cursor.fetchall()

    def showContext(self, context):
        self.cursor.execute("SELECT ps_endpoints.context, ps_auths.username, ps_auths.password, ps_endpoints.callerid, "
                             "ps_contacts.user_agent, ps_contacts.via_addr FROM ps_auths INNER JOIN "
                             "ps_endpoints USING(id) LEFT JOIN ps_contacts ON ps_auths.username = "
                             "ps_contacts.endpoint WHERE ps_endpoints.context = '%s' ORDER BY username" % context)
        return self.cursor.fetchall()

    def showBlacklist(self):
        self.cursor.execute("SELECT name FROM blacklist")
        return self.cursor.fetchall()

    def addToBlacklist(self, name):
        self.cursor.execute("INSERT INTO blacklist(name) VALUES(%s)", (name,))
        self.db.commit()

    def delFromBlacklist(self, name):
        self.cursor.execute("DELETE FROM blacklist WHERE name = %s", (name,))
        self.db.commit()

    def existInBlacklist(self, number):
        self.cursor.execute("SELECT name FROM blacklist WHERE name = %s", (number,))
        data = self.cursor.fetchall()
        return True if data else False

    def showProvisioningAssociates(self, option):
        self.cursor.execute("SELECT name, macAddress, vlan FROM configs ORDER BY %s" % option)
        return self.cursor.fetchall()

    def existInConfigs(self, option, data):
        self.cursor.execute("SELECT " + option + " FROM configs WHERE " + option + " = %s", (data,))
        data = self.cursor.fetchall()
        return True if data else False

    def makeProvisioningAssociates(self, name, mac, vlan):
        self.cursor.execute("INSERT INTO configs(name, macAddress, vlan) VALUES(%s,%s,%s)", (name, mac, vlan))
        self.db.commit()

    def deleteProvisioningAssociate(self, name):
        self.cursor.execute("DELETE FROM configs WHERE name = %s", (name,))
        self.db.commit()
        print("\033[36mDone.\033[0m")

    def getConfig(self, value):
        self.cursor.execute("SELECT name, macAddress, vlan FROM configs WHERE name = %s" % (value))
        return self.cursor.fetchall()

    def editProvisioningAssociate(self, name, oldMacAddress, newMacAddress, vlan):
        self.cursor.execute("UPDATE configs SET macAddress = %s, vlan = %s WHERE name = %s AND macAddress = %s", (newMacAddress, vlan, name, oldMacAddress))
        self.db.commit()
        print("\033[36mDone.\033[0m")

    def __del__(self):
        self.cursor.close()
        self.db.close()

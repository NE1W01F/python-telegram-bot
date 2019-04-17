import sqlite3
import datetime
import os

def allfile():
    allfiles = []
    for root, subfiles, files in os.walk(os.getcwd()):
        for names in files:
            allfiles.append(os.path.join(root, names))

    return allfiles

def checkname(name):
    notdata = ['bot.py', 'database.db', 'trainer.py', 'reader.py', 'setup.py', 'modules.xml', 'telegram-bot.iml', 'workspace.xml', 'misc.xml']
    for names in notdata:
        if os.path.basename(name) == names:
            return True
        #elif os.path.basename(name) == "task_{}".format(str(datetime.date.today())):
            #return True
    return False

def main():
    files = allfile()
    datafiles = []
    for names in files:
        a = checkname(names)
        if a:
            pass
        else:
            datafiles.append(names)

    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    for file in datafiles:
        read = open(file, 'r')
        data = read.readlines()
        for msg in data:
            w = msg
            a = w.split('|')
            q = a[2].replace('Message:', '').replace(' ', '')
            response = raw_input("User response: {} Enter your response:".format(str(q)))
            inputdata = response.replace(' ', '')
            cursor.execute('''INSERT INTO messages(message, response)VALUES(?, ?)''', ('hi', 'Hello'))
            db.commit()

    db.close()

def deldata():
    dataid = raw_input("enter data id to be deleted:")
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute('''DELETE FROM blacklist WHERE id = ?''', (int(dataid),))
    db.commit()
    db.close()

def adddata():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute('''INSERT INTO messages(message, response)VALUES(?, ?)''', ('no i am fine', 'Ok well i am here if you need me'))
    db.commit()
    db.close()

#adddata()
#main()
deldata()
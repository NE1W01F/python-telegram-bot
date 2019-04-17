import sqlite3

def main():
    db = sqlite3.connect('database.db')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute('''SELECT id, chat_id, username FROM members''')
    db.commit()
    print "Table members | ID |  User ID  | Username"
    for user in cursor:
        print("                {}    {}    {}".format(str(user['id']), str(user['chat_id']), str(user['username'])))

    cursor.execute('''SELECT id, message, response FROM messages''')
    db.commit()
    print ('')
    for data in cursor:
        print str(data['id']) + " | " + data['message'] + " | " + data['response']

    print ''
    cursor.execute('''SELECT id, chat_id, username FROM blacklist''')
    db.commit()
    for black in cursor:
        print black['chat_id'] + " | " + black['username']

main()
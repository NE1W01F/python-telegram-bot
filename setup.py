import sqlite3

def main():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE blacklist(id INTEGER PRIMARY KEY, chat_id TEXT, username TEXT)''')
    cursor.execute('''CREATE TABLE messages(id INTEGER PRIMARY KEY, message TEXT, response TEXT)''')
    cursor.execute('''CREATE TABLE members(id INTEGER PRIMARY KEY, chat_id TEXT, username TEXT)''')
    db.commit()
    db.close()

main()
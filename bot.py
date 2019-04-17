import telepot
import sqlite3
import datetime
from Crypto.Hash import MD5
import os

def banuser(username):
    db = sqlite3.connect('database.db')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute('''SELECT chat_id, username FROM members''')
    db.commit()
    for user in cursor:
        if user['username'] == username:
            return user['chat_id']
    return ''

def blacklist(username, user_id, act):
    db = sqlite3.connect('database.db')
    if act:
        cursor = db.cursor()
        cursor.execute('''INSERT INTO blacklist(chat_id, username)VALUES(?, ?)''', (user_id, username))
        db.commit()
    else:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute('''SELECT chat_id, username FROM blacklist''')
        db.commit()
        for user in cursor:
            if user['username'] == username or user['chat_id'] == user_id:
                return True

        return False



def images(chat_id, text):
    q = text.split(' ')
    query = q[0]
    query2 = q[1]
    site = "https://source.unsplash.com/featured/?{},{}".format(str(query), str(query2))
    bot.sendPhoto(chat_id, site, caption="Enjoy the photo")

def dataset(message):
    db = sqlite3.connect('database.db')
    db.row_factory = sqlite3.Row
    data = db.cursor()
    data.execute('''SELECT message, response FROM messages''')
    db.commit()
    response = ""
    for dataq in data:
        if message.lower() == str(dataq["message"]).lower():
            response = str(dataq["response"])

    db.close()
    return response

def addmember(chat_id, username):
    db = sqlite3.connect('database.db')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute('''INSERT INTO members(chat_id, username)VALUES(?, ?)''', (chat_id, username))
    db.commit()
    db.close()

def members(chat_id, username):
    db = sqlite3.connect('database.db')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute('''SELECT chat_id, username FROM members''')
    db.commit()
    for user in cursor:
        if chat_id == user["chat_id"]:
            if username == user["username"]:
                return True, True

    return False, False

def updateUserInfo(chat_id, username):
    db = sqlite3.connect('database.db')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute('''SELECT id, chat_id, username FROM members''')
    db.commit()
    for user in cursor:
        if chat_id == user["chat_id"]:
            if username != user["username"]:
                cursor.execute('''INSERT INTO members(username)''', (username,))
                db.commit()
                db.close()

    return True


Token = ""
bot = telepot.Bot(Token)
task = open('tasks/task_{}'.format(str(datetime.date.today())), 'w')

def createTask(chat_id, message):
    task.write("Time: {} | UserID: {} | Message: {}\n".format(str(datetime.datetime.now()), str(chat_id), str(message)))
    return "Sorry I don't understand your input, i have contacted the master to update me."

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        try:
            message = msg['text']
            if chat_type == "private":
                usercheck = blacklist(str(msg['from']['username']), str(msg['from']['id']), False)
                if usercheck:
                    if '/appeal' in message.lower():
                        bot.sendMessage(chat_id, "Your appeal has been sent please wait\nof an admin to contact you.")
                        bot.sendMessage('736627724', "User @{} has requested an appeal".format(msg['from']['username']))
                    else:
                        bot.sendMessage(chat_id, "You have been banned from talking to this bot\n\nYou can appeal the ban by sending /appeal\nan admin will contact you and will decide")
                if usercheck is not True:
                    if message.lower() == '/start':
                        bot.sendMessage(chat_id, 'Hello @' + str(msg['from']['username']) + " Welcome to the hacker chat bot")
                        a, b = members(str(msg['from']['id']), str(msg['from']['username']))
                        if a and b:
                            pass
                        elif a and b is not True:
                            updateUserInfo(str(msg['from']['id']), str(msg['from']['username']))
                            bot.sendMessage(chat_id, "Why did you change your username? I don't care.")
                        elif a != True:
                            addmember(str(msg['from']['id']), str(msg['from']['username']))
                            bot.sendMessage(chat_id, "You not in hacker chat yet. please join\n\nhttps://t.me/WIFIHacker2019")
                    else:
                        response = dataset(message)
                        if len(response) == 0:
                            userinput = createTask(chat_id, message)
                            bot.sendMessage(chat_id, userinput)
                        else:
                            bot.sendMessage(chat_id, response)
            else:
                if "hack wifi" in message.lower():
                    bot.sendMessage(chat_id, "Please use google and search '{}' or follow the link below\n\nhttps://www.onlinehashcrack.com/how-to-crack-WPA-WPA2-networks.php".format(str(message)))
                elif message.lower() == '/start':
                    bot.sendMessage(chat_id, "Welcome to the hackers chat bot")
                elif '/kick' in message:
                    if msg['from']['username'] == 'webdev2019':
                        ban = str(message).replace('/kick', '').replace(' ', '')
                        a = banuser(ban)
                        blacklist(ban, a, True)
                        bot.kickChatMember(chat_id, str(a))
                    else:
                        bot.sendMessage(chat_id, "Sorry can't do that")
                elif '/image' in message.lower():
                    W = message.lower()
                    S = str(W).replace('/image ', '')
                    if len(S) > 5:
                        images(chat_id, S)
                    else:
                        pass
                elif '/hashme' in message.lower():
                    V = message.lower()
                    n = str(V).replace('/hashme', '').replace(' ', '')
                    if len(n) == 0:
                        pass
                    else:
                        u = MD5.new(n).hexdigest()
                        bot.sendMessage(chat_id, "Here is you MD5 hash for '{}'\n\nHash:*{}*".format(str(n), str(u)), parse_mode='Markdown')
                elif message.lower() == '/stop':
                    bot.sendMessage(chat_id, "Stopping bot")
                elif '/getid' in message.lower():
                    bot.sendMessage(chat_id, "Your ID is {}\nYour username is @{}".format(str(msg['from']['id']), str(msg['from']['username'])))
                else:
                    a, b = members(str(msg['from']['id']), str(msg['from']['username']))
                    if a and b:
                        pass
                    elif a and b != True:
                        updateUserInfo(str(msg['from']['id']), str(msg['from']['username']))
                        bot.sendMessage(chat_id, "Why did you change your username? i don't care.")
                    elif a != True:
                        addmember(str(msg['from']['id']), str(msg['from']['username']))
                        bot.sendMessage(chat_id, "Welcome to hackers chat,\nyou seam new around here\nNice to meet you")
        except:
            pass

def sendinghiddenmessages():
    db = sqlite3.connect('database.db')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute('''SELECT chat_id, username FROM members''')
    db.commit()
    print("\n")
    for user in cursor:
        print("UserId: {}|Username: {}".format(str(user['chat_id']), str(user['username'])))

    print("\n")
    cd = raw_input("Enter Chat ID:")
    sd = raw_input("Enter Message:")
    if len(cd) == 0:
        pass
    else:
        try:
            bot.sendMessage(cd, sd)
            print("Message has been sent..\n")
        except:
            print "Error sending message..\n"

bot.message_loop(handle)
print('listening... Bot is Online\n')
print("Enter 'q' to exit or 's' to send message")
while True:
    chat_command = raw_input("Enter Command:")
    if chat_command == 'q':
        task.close()
        break
    elif chat_command == 's':
        sendinghiddenmessages()
    elif chat_command == 'clear' or chat_command == 'c' or chat_command == 'cls':
        os.system('clear')
    else:
        pass
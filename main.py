import discord
import os
import sqlite3

client = discord.Client()
conn = sqlite3.connect('data.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS usershard(
   userid TEXT PRIMARY KEY,
   strenght INT,
   stealth INT,
   speed INT,
   intel INT,
   spell1 INT,
   spell2 INT
   );
""")
conn.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS balance(
   userid TEXT PRIMARY KEY,
   bal INT
   );
""")
conn.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS spells(
   spell TEXT PRIMARY KEY,
   spellid INT,
   damage INT,
   mana INT,
   speed INT,
   gif TEXT
   );
""")
conn.commit()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return



    if (message.channel.id == 861135728574201857):
        cur.execute("""INSERT INTO balance(userid, bal) VALUES(?, ?);""", (message.author.id, 0))
        conn.commit()

    if message.content.startswith('?кто лох'):
        await message.channel.send('Саитхи лох')

#    if message.content.startswith('?screate'):
#      if message.author.top_role == message.server:
#        sp = message.content
#        sp.replace('?screate ','')
#        f1, f2, f3, f4 = map(str, sp.split())
#        f2 = int(f2)
#        f3 = int(f3)
#        await message.channel.send('Заклинание с названием ' + f1 + " наносящее " + str(f2) + " урона, требующее " + str(f3) + "маны. /n С анимацией :" + f4)


    if message.content.startswith('?bal'):
      if message.mentions == []:
        cur.execute("SELECT bal FROM balance WHERE userid=?;", [(message.author.id)])
        result = cur.fetchone()[0]
        await message.channel.send('У пользователя ' + message.author.name + ' на счету: ' + str(result) + ' валюты')
      else:
        ping = message.mentions[0]
        cur.execute("SELECT bal FROM balance WHERE userid=?;", [(ping.id)])
        result = cur.fetchone()[0]
        await message.channel.send('У пользователя ' + ping.name + ' на счету: ' + str(result) + ' валюты')
    if message.content.startswith('?pay'):
        buf = message.content
        ping = message.mentions[0]
        while(not buf.isnumeric()):
            buf = buf[1:]
        cur.execute("SELECT bal FROM balance WHERE userid=?;", [(message.author.id)])
        result = cur.fetchone()[0]
        buf = int(buf)
        if (buf <= result):
            await message.channel.send('Переведено ' + str(buf) + " пользователю: " + ping.name)
            result1=result-int(buf)
            cur.execute("UPDATE balance SET bal=? WHERE userid=?", [result1, (message.author.id)])
            conn.commit()
            cur.execute("SELECT bal FROM balance WHERE userid=?;", [(ping.id)])
            result = cur.fetchone()[0]
            result1 = result + int(buf)
            cur.execute("UPDATE balance SET bal=? WHERE userid=?", [int(result1), (ping.id)])
            conn.commit()


client.run(os.getenv('TOKEN'))
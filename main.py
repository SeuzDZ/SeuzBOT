import discord
import os
import sqlite3

client = discord.Client()
conn = sqlite3.connect('data.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS usershard(
   userid TEXT PRIMARY KEY,
   strenght INT,
   speed INT,
   intel INT,
   spell1 INT,
   spell2 INT,
   spell3 INT,
   spell4 INT,
   spell5 INT,
   spell6 INT,
   spell7 INT,
   spell8 INT,
   spell9 INT,
   spell10 INT,
   spell11 INT,
   spell12 INT,
   spell13 INT,
   spell14 INT,
   spell15 INT,
   spell16 INT,
   spell17 INT,
   spell18 INT,
   spell19 INT,
   spell20 INT
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
   mana INT,
   damage INT,
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

    if message.content.startswith('?s'):
        sp = message.content
        sp = sp.replace('?s ', '')
        cur.execute("SELECT * FROM usershard WHERE userid=?;", [(message.author.id)])
        result = cur.fetchone()[0]
        if(not (result.count(sp) == 0)):
            cur.execute("SELECT gif FROM spells WHERE spell=?;", [(sp)])
            result = cur.fetchone()[0]
            sp = sp.replace('_',' ')
            await message.channel.send("Заклинание " + sp + " было использованно. \n Анимация: " + str(result) )


    if message.content.startswith('?screate'):
      if message.author.top_role.id == 861130313169633300:
        sp = message.content
        sp = sp.replace('?screate ','')
        f = sp.split()
        await message.channel.send('Заклинание с названием ' + f[0] + " наносящее " + f[1] + " урона, требующее " + f[2] + " маны и требующее " + f[3] +" скорости. \n С анимацией : " + f[4])
        cur.execute("INSERT INTO spells(spell, damage , mana, speed, gif) VALUES (?, ?, ?, ?, ?)", (f[0], int(f[1]), int(f[2]), int(f[3]), f[4]))
        conn.commit()

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


client.run('ODYxMTM3ODM0NTg0OTY1MTMx.YOFbGg.oRg1xGf_G4cFzJgPOv3N7CLRmE8')
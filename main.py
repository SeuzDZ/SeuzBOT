import discord
import os
import sqlite3

client = discord.Client()
conn = sqlite3.connect('data.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS usershard(
   userid INT PRIMARY KEY,
   strenght INT,
   stealth INT,
   speed INT,
   intel INT
   );
""")
conn.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS balance(
   userid TEXT PRIMARY KEY,
   bal INT
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
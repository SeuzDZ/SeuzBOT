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
    
    if (message.channel.name == 'новобранцы'):
        cur.execute("""INSERT INTO balance(userid, bal) VALUES(?, ?);""", (message.author.id, 0))
        conn.commit()

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(os.getenv('TOKEN'))
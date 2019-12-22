import discord 
from discord.ext import commands 
from pymongo import MongoClient as mcl 
import os 
import sys 
from datetime import datetime 

TOKEN = "NjQ0MzIxMTg5Mzk3MDA0Mjg5.XfwYEA.mi6ai-k4_sV9fbiqbyV1uS2xRRM"

cogs = [
    "cogs.drops",
    "cogs.loot",
    "cogs.blacklist",
    "cogs.inv",
    "cogs.leaderboard",
    "cogs.help"
]

def get_prefix():
    prefixes = [
       "!", 
       "<@644321189397004289>",
       "<@!644321189397004289>"
    ]
    return prefixes 

class Christmas(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=get_prefix(), case_insensitive=True)

        self.candy = "<:candy_cane:657386020320444426>"
        self.candle = "<:christmas_candle:657384456017149955>"
        self.cross = "<:christmas_cross:657385915974549544>"
        self.gift = "<:christmas_gift:657393185378664448>"
        self.wreath = "<:christmas_wreath:657394127360753688>"

        self.embed = 0xf23333

        self.client = mcl("mongodb://brendan:BS103261@ds061199.mlab.com:61199/bad_santa?retryWrites=false")
        self.db = self.client['bad_santa']
        self.user_col = self.db['users']
        self.banned = self.db['banned']

        self.admin = [
            367492468578582539,  #air
            319593881182404608,   #rev
            292749706407182337,   #teddy  
            280052443956379658,   #hunter
            601846796662210570   #brendan
            # 404310500336205826    #encor
        ]

        self.add_check(self.command_check)

    async def on_ready(self):
        print("Christmas special bot is now online.")
        for cog in cogs:
            try:
                bot.load_extension(cog)
                print(f"Loaded {cog}")
            except Exception as e:
                print(e)

    async def command_check(self, ctx):
        self.data = self.banned.find_one()
        users = self.data['blacklisted_users']
        if len(users) == 0:
            return True
        if str(ctx.author.id) in users:
            await ctx.author.send(f"You have been blacklisted from using Santa's Sleigh, please appeal the ban with an Admin or Manager.")
            return False
        else:
            return True

bot = Christmas()

@commands.is_owner()
@bot.command()
async def restart(ctx):
    await ctx.send(F"Restarting now! This may take 10+ seconds..")
    await bot.change_presence(status=discord.Status.idle)
    os.execv(sys.executable, ['python3.6'] + sys.argv)

@commands.is_owner()
@bot.command(aliases=['r'])
async def reload(ctx):
    cogs_list = ""
    for cog in cogs:
        try:
            bot.reload_extension(cog)
            cogs_list += f"{bot.cross} **{cog}**\n"
        except Exception as e:
            cogs_list += f"{bot.candle} **{cog}** ({e})\n"
    await ctx.send(cogs_list)

bot.run(TOKEN)

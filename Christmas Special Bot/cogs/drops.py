import discord 
from discord.ext import commands 
from pymongo import MongoClient as mcl 
from datetime import datetime 
from collections import defaultdict
import random
import asyncio

class Drops(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.client = self.bot.client
        self.db = self.bot.db 
        self.col = self.bot.user_col
        self.bot.messages = defaultdict(int)
        self.bot.codes = 0
        self.current_crate = ""

    @commands.command()
    async def messages(self, ctx):
        if not ctx.author.id == 601846796662210570 or ctx.author.id == 292749706407182337:
            return
        await ctx.send(f"There are **{self.bot.messages[ctx.channel]}** messages found.")

    @commands.command(aliases=['l', 'pickup'], usage=['loot <crate-number>'])
    async def loot(self, ctx, code: int = None):
        self.data = self.col.find_one()
        server = ctx.guild 
        if not code:
            return
        if not code == self.bot.codes:
            return
        possible_messages = [
            f":man_detective: {ctx.author.mention} has looted a home and stole all the christmas gifts!",
            f":man_detective: {ctx.author.mention} has shacked the christmas tree of another unsuspecting home!",
            f"{self.bot.gift} {ctx.author.mention} has successfully looted the crate, congratulations!"
        ]
        message = random.choice(possible_messages)
        if self.current_crate == "regular":
            if not str(ctx.author.id) in self.data:
                doc = {"$set": {str(ctx.author.id):{
                    "crates": 1,
                    "candles": 0,
                    "crosses": 0,
                    "candy": 0,
                    "items": []
                }}}
                self.col.update_one({"auth": True}, doc)
                await ctx.send(message)
                self.bot.codes = 0
                return
            doc = {"$set": {str(ctx.author.id):{
                "crates": self.data[str(ctx.author.id)]['crates'] + 1,
                "candles": self.data[str(ctx.author.id)]['candles'],
                "crosses": self.data[str(ctx.author.id)]['crosses'],
                "candy": self.data[str(ctx.author.id)]['candy'],
                "items": self.data[str(ctx.author.id)]['items']
            }}}
            self.col.update_one({"auth": True}, doc)
            await ctx.send(message)
            self.bot.codes = 0
            self.current_crate = ""
            return
        if self.current_crate == "candle":
            if not str(ctx.author.id) in self.data:
                doc = {"$set": {str(ctx.author.id):{
                    "crates": 0,
                    "candles": 1,
                    "crosses": 0,
                    "candy": 0,
                    "items": []
                }}}
                self.col.update_one({"auth": True}, doc)
                await ctx.send(message)
                self.bot.codes = 0
                return
            doc = {"$set": {str(ctx.author.id):{
                "crates": self.data[str(ctx.author.id)]['crates'],
                "candles": self.data[str(ctx.author.id)]['candles'] + 1,
                "crosses": self.data[str(ctx.author.id)]['crosses'],
                "candy": self.data[str(ctx.author.id)]['candy'],
                "items": self.data[str(ctx.author.id)]['items']
            }}}
            self.col.update_one({"auth": True}, doc)
            await ctx.send(message)
            self.bot.codes = 0
            self.current_crate = ""
            
    @commands.command(hidden=True)
    async def drop(self, ctx):
        if not ctx.author.id in self.bot.admin:
            return 
        await ctx.message.delete()
        secure_code1 = random.randint(1001, 100000000000)
        secure_code2 = random.randint(1001, 1000000)
        if drop_type == "candle":
            self.bot.codes = secure_code1
            self.current_crate = "candle"
            embed = discord.Embed(color=self.bot.embed)
            embed.title = "New Candle Drop!"
            embed.description = f"{self.bot.candle} Use the command `!loot {secure_code1}` to pick up this christmas crate!")
            await ctx.send(embed=embed)
         else:
            self.bot.codes = secure_code2
            self.current_crate = "regular"
            embed = discord.Embed(color=self.bot.embed)
            embed.title = "New Crate Drop!"
            embed.description = f"{self.bot.candle} Use the command `!loot {secure_code2}` to pick up this christmas crate!")
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id != 606974489397559326:
            return
        self.data = self.col.find_one()
        code = random.randint(100, 1000)
        secure_code = random.randint(1001, 10000)
        gem_code = random.randint(10000, 20000)
        server = message.guild
        self.bot.messages[message.channel] += 1 #add .id if needed
        if self.bot.messages[message.channel]%100 == 0:
            await server.get_member(601846796662210570).send(f"!loot {secure_code}")
            await asyncio.sleep(5)
            self.bot.codes = secure_code
            self.current_crate = "regular"
            embed = discord.Embed(color=self.bot.embed)
            embed.title = "New Crate Drop!"
            embed.description = f"{self.bot.gift} Use the command `!loot {secure_code}` to pick up this christmas crate!"
            await message.channel.send(embed=embed)
            # await message.channel.send(f"{self.bot.present} **|** Dropped a crate! Use the command `!loot {code}` to pick it up..")
            return
            
def setup(bot):
    bot.add_cog(Drops(bot))

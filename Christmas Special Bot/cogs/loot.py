import discord 
from discord.ext import commands 
from discord import Webhook, AsyncWebhookAdapter
from pymongo import MongoClient as mcl 
from datetime import datetime 
import asyncio 
import random 
import aiohttp


class Crates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.client = self.bot.client
        self.db = self.bot.db 
        self.users = self.bot.user_col

    @commands.command()
    async def crates(self, ctx):
        self.data = self.users.find_one()
        if not str(ctx.author.id) in self.data:
            doc = {"$set": {str(ctx.author.id):{
                "crates": 1,
                "candles": 0,
                "crosses": 0,
                "candy": 0,
                "items": []
            }}}
            self.users.update_one({"auth": True}, doc)
            await ctx.send(f"You currently have no crates.")
        else:
            crates = self.data[str(ctx.author.id)]['crates']
            c = ""
            for crate in range(crates):
                c += f"{self.bot.gift} "
            user = ctx.author
            if not c:
                c = ""
            crates = f"{c}"
            if not crates:
                crates = "You currently have no crates."
            try:
                await ctx.send(f"**__Crates__ ({self.data[str(user.id)]['crates']})**\n{crates}")
            except discord.HTTPException:
                await ctx.send(F"You currently have **{self.data[str(user.id)]['crates']}** crates unopened.")

    @commands.command()
    async def open(self, ctx, type: str = None):
        self.data = self.users.find_one()
        types = [
            'regular',
        ]
        if not type:
            return await ctx.send(f"You need to specify the what you want to open. Use the command form `c!open <regular>` to open a crate.")
        if not type.lower() in types:
            return await ctx.send("That is not a current loot crate that you can open. Use the command form `c!open <regular>` to open a crate.")
        if not str(ctx.author.id) in self.data:
            doc = {"$set": {str(ctx.author.id):{
                "crates": 1,
                "candles": 0,
                "crosses": 0,
                "candy": 0,
                "items": []
            }}}
            self.users.update_one({"auth": True}, doc)
            await ctx.send(f"You currently have no crates.")
        if type.lower() == "regular":
            if not str(ctx.author.id) in self.data:
                doc = {"$set": {str(ctx.author.id):{
                    "crates": 0,
                    "candles": 0,
                    "crosses": 0,
                    "candy": 0,
                    "items": []
                }}}
                self.users.update_one({"auth": True}, doc)
                await ctx.send(f"You currently have no crates.")
            else:
                chance = random.randint(0,1)
                crates = self.data[str(ctx.author.id)]['crates']
                crosses = self.data[str(ctx.author.id)]['crosses']
                candles = self.data[str(ctx.author.id)]['candles']
                if crates == 0:
                    return await ctx.send(f"You currently have no crates.")
                candy = self.data[str(ctx.author.id)]['candy']
                user_items = self.data[str(ctx.author.id)]['items']
                crates -= 1
                items = [
                    'Snow Globe',
                    'Christmas Tree',
                    'Stocking'
                ]
                print(chance)
                ran = random.random()
                print(ran)
                if ran <= .20:
                    num = random.randint(75, 100)
                    candles += 1        
                    candle_math = candles * .5
                    new = num * candle_math + num
                    candy += round(new)
                    message = f"""
{self.bot.candle} **1** 

{self.bot.candy} **{round(new)}**

:scroll: **You have gotten a new candle! Which means that you will be able to max out at 50% multplier, this will multiply your candy by 50%.**

:chart_with_downwards_trend: **40% chance of getting this package.**                 
                    """
                    doc = {"$set": {str(ctx.author.id):{
                        "crates": crates,
                        "candles": candles,
                        "crosses": crosses,
                        "candy": candy,
                        "items": user_items
                    }}}
                    self.users.update_one({"auth": True}, doc)
                    async with aiohttp.ClientSession() as session:
                        webhook = Webhook.from_url('https://discordapp.com/api/webhooks/659514233632980992/OVXyaWOEHbFlZnT4ogvVUgKbGz70FDZFNkcRUuRTiJQETpFg1CqsqppHzppce16zHp-_', adapter=AsyncWebhookAdapter(session))
                        await webhook.send(message)
                    return 
#                 if ran == .70 or ran == .80:
#                     num = random.randint(75, 100)
#                     item = random.choice(items)
#                     user_items.append(item)
#                     if candles == 0:
#                         new = num 
#                     else:
#                         candle_math = candles * .5
#                         new = num * candle_math + num
#                     candy += round(new)
#                     message = f"""
# :card_box: **{item}**

# {self.bot.candy} **{round(new)}**

# :scroll: **You have gotten the `{item}`! This has no effect nor advantage against other users, this is just a cool antique!**

# :chart_with_downwards_trend: **70% chance of getting this package.**
#                     """
#                     doc = {"$set": {str(ctx.author.id):{
#                         "crates": crates,
#                         "candles": candles,
#                         "crosses": crosses,
#                         "candy": candy,
#                         "items": user_items
#                     }}}
#                     self.users.update_one({"auth": True}, doc)
#                     msg = await ctx.send(f"<a:loading:657407274301784074> Opening crate....")
#                     await asyncio.sleep(1.5)
#                     await msg.delete()
#                     embed = discord.Embed(color=0x0066ff)
#                     embed.title = "Opened crate!"
#                     embed.description = message 
#                     await ctx.send(embed=embed)
#                     return 
                else:
                    num = random.randint(75, 100)
                    if candles == 0:
                        new = num + num
                    else:
                        candle_math = candles * .5
                        print(candle_math)
                        new = round(num * candle_math + num)
                    candy += new
                    message = f"""
{self.bot.candy} **{new}**
                    """
                    doc = {"$set": {str(ctx.author.id):{
                        "crates": crates,
                        "candles": candles,
                        "crosses": crosses,
                        "candy": candy,
                        "items": user_items
                    }}}
                    self.users.update_one({"auth": True}, doc)
                    async with aiohttp.ClientSession() as session:
                        webhook = Webhook.from_url('https://discordapp.com/api/webhooks/659514233632980992/OVXyaWOEHbFlZnT4ogvVUgKbGz70FDZFNkcRUuRTiJQETpFg1CqsqppHzppce16zHp-_', adapter=AsyncWebhookAdapter(session))
                        await webhook.send(message)
                # doc = {"$set": {str(ctx.author.id):{
                #     "crates": crates,
                #     "candles": candles,
                #     "crosses": crosses,
                #     "candy": candy,
                #     "items": user_items
                # }}}
                # self.users.update_one({"auth": True}, doc)
                # msg = await ctx.send(f"<a:loading:657407274301784074> Opening crate....")
                # await asyncio.sleep(1.5)
                # await msg.delete()
                # embed = discord.Embed(color=0x0066ff)
                # embed.title = "Opened crate!"
                # embed.description = message 
                # await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Crates(bot))

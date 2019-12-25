import discord 
from discord.ext import commands 
from pymongo import MongoClient as mcl 
from datetime import datetime 
import asyncio 
import random 

class Inventory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.client = self.bot.client
        self.db = self.bot.db 
        self.users = self.bot.user_col 

    @commands.command(aliases=['inv'])
    async def inventory(self, ctx, user: discord.Member = None):
        self.data = self.users.find_one()
        if not user:
            user = ctx.author
        if not str(ctx.author.id) in self.data:
            doc = {"$set": {str(ctx.author.id):{
                "crates": 0,
                "candles": 0,
                "crosses": 0,
                "candy": 0,
                "items": []
            }}}
            self.users.update_one({"auth": True}, doc)
            embed = discord.Embed(color=0x0F8A5F, timestamp=datetime.utcnow())
            embed.set_author(name=f"{user.name} Inventory", icon_url=user.avatar_url)
            embed.add_field(name=f"{self.bot.settings_icon} Items (0)", value=f"You currently have no items.", inline=False)
            embed.add_field(name=f"{self.bot.candles} Candles", value=f"You have 0 candles.", inline=False)
            embed.add_field(name=f"{self.bot.candy} Candy", value="You have 0 candy.", inline=False)
            embed.add_field(name=f":mailbox_with_mail: Presents (0)", value=f"You currently have no christmas presents.")
            await ctx.send(embed=embed)
        else:
            c = ""
            for crate in range(self.data[str(user.id)]['crates']):
                c += f"{self.bot.gift}"
            if not c:
                c = ""
            crates = f"{c}"
            if not crates:
                crates = "You currently have no crates."
            items = ""
            for item in self.data[str(user.id)]['items']:
                if item == "Snow Globe":
                    items += f"<:snow_globe:657790748657451008> "
                    pass
                if item == "Stocking":
                    items += "<:stocking:657790748569108490> "
                    pass
                if item == "Christmas Tree":
                    items += "<:christmas_tree1:657790748707651602> "
                    pass
                if item == "Air's Throne":
                    items += ":crown: "
            if not items:
                items="You currently have no items."
            candy = "{:,}".format(self.data[str(user.id)]['candy'])
            try:
                embed = discord.Embed(color=0x0F8A5F, timestamp=datetime.utcnow())
                embed.set_author(name=f"{user.name} Invetory", icon_url=user.avatar_url)
                embed.add_field(name=f":card_box: Items (0)", value=items, inline=False)
                embed.add_field(name=f"{self.bot.candle} Candles", value=f"You have {self.data[str(user.id)]['candles']} candles.", inline=False)
                embed.add_field(name=f"{self.bot.candy} Candy", value=f"You have {candy} candy", inline=False)
                embed.add_field(name=f":mailbox_with_mail: Crates ({self.data[str(user.id)]['crates']})", value=crates, inline=False)
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(color=0x0F8A5F, timestamp=datetime.utcnow())
                embed.set_author(name=f"{user.name} Invetory", icon_url=user.avatar_url)
                embed.add_field(name=f":card_box: Items ({len(self.data[str(user.id)]['items'])})", value=items, inline=False)
                embed.add_field(name=f"{self.bot.candle} Candles", value=f"You have {self.data[str(user.id)]['candles']} candles.", inline=False)
                embed.add_field(name=f"{self.bot.candy} Candy", value=f"You have {candy} candy", inline=False)
                embed.add_field(name=f":mailbox_with_mail: Crates ({self.data[str(user.id)]['crates']})", value=f"""
                {self.bot.gift} **__{self.data[str(user.id)]['crates']}__**
                """, inline=False)
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Inventory(bot))

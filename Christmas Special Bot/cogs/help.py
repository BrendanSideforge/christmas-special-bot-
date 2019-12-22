import discord 
from discord.ext import commands 
from collections import deque 

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.command()
    async def guide(self, ctx):
        server = ctx.guild
        embed1 = discord.Embed(color=self.bot.embed)
        embed1.set_author(name=f"Santa's Sleigh", icon_url=self.bot.user.avatar_url)
        embed1.add_field(name=f"<:snow_globe:657790748657451008> What is it?", value=f"""
        Santa's Sleigh is a bot for Feudal, we are currently having an event for the bot.
        Who ever has the most coins at the end of the year wins!
        """, inline=False)
        embed1.add_field(name=f":tada: Prizes", value=f"""
        **1st Place**: Nitro
        **2nd Place**: Custom role
        **3rd Place**: Role of recognition.
        """)
        embed1.set_thumbnail(url=self.bot.user.avatar_url)
        embed1.set_footer(text=f"Use the reactions to flip between pages. Page (1/2)")

        embed2 = discord.Embed(color=self.bot.embed)
        embed2.set_author(name=f"Santa's Sleigh Commands", icon_url=self.bot.user.avatar_url)
        embed2.add_field(name=f"!crates", value="Show all of your crates.", inline=False)
        embed2.add_field(name=f"!open <regular>", value=f"Open a crate for the goodies inside it.", inline=False)
        embed2.add_field(name=f"!loot <code>", value=f"Loot a crate that has been dropped in general.", inline=False)
        embed2.add_field(name=f"!inventory [@User]", value=f"See what you have in your inventory, such as items, candy, and crates.", inline=False)
        embed2.set_thumbnail(url=self.bot.user.avatar_url)
        embed2.set_footer(text=f"Use the reactions to flip between pages. Page (2/2)")

        pages = deque((embed1, embed2))
        embed = pages[0]
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("◀")
        await msg.add_reaction("❌")
        await msg.add_reaction("▶")
        def reactioncheck(reaction, user):
            if user == ctx.author:
                if reaction.message.id == msg.id:
                    if reaction.emoji == "▶" or reaction.emoji == "❌" or reaction.emoji == "◀":
                        return True
        x = 0
        while True:
            reaction, user3 = await self.bot.wait_for("reaction_add", check=reactioncheck)
            if reaction.emoji == "▶":
                pages.rotate(-1)
                embed = pages[0]
                await msg.edit(embed=embed)
                await msg.remove_reaction("▶", user3)
            elif reaction.emoji == "◀":
                pages.rotate(1)
                embed = pages[0]
                await msg.edit(embed=embed)
                await msg.remove_reaction("◀", user3)
            elif reaction.emoji == "❌":
                await msg.delete()


def setup(bot):
    bot.add_cog(Help(bot))
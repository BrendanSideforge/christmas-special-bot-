import discord 
from discord.ext import commands 
from pymongo import MongoClient as mcl 
from datetime import datetime 

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.client = self.bot.client
        self.db = self.bot.db 
        self.users = self.bot.user_col

    async def leaderboardData(self, ctx):
        self.data = self.users.find_one()
        server_users = self.data
        top = list(enumerate(sorted([(server_users[user]["candy"], user) for user in server_users if len(user) == 18], reverse=True), start=1))
   
        async def leader_embed(eggs):
            embed = discord.Embed(color=self.bot.embed)
            embed.title = "Leaderboard"
            desc = ""
            for pos, score in eggs:
                    user = await self.bot.fetch_user(score[1])
                    embed.add_field(name=f"**{pos}**. **__{user}__**", value="{} {:,} coins".format(self.bot.candy, score[0]), inline=False)
            return embed
           
        message = await ctx.send(embed=await leader_embed(top[:10]))
       
       
        if len(top) > 10:
              await message.add_reaction("◀")
              await message.add_reaction("❌")
              await message.add_reaction("▶")
 
        def reactioncheck(reaction, user):
            if user == ctx.author:
                if reaction.message.id == message.id:
                    if reaction.emoji == "▶" or reaction.emoji == "❌" or reaction.emoji == "◀":
                        return True
        x = 0
        while True:
            reaction, user3 = await self.bot.wait_for("reaction_add", check=reactioncheck)
            if reaction.emoji == "◀":
                await message.remove_reaction("◀", user3)
                x -= 10
                if x < 0:
                    x = 0
            elif reaction.emoji == "❌":
                await message.delete()
            elif reaction.emoji == "▶":
                await message.remove_reaction("▶", user3)
                x += 10
                if x > len(top):
                    x = len(top) - 10
            embed = await leader_embed(top[x:x+10])
            await message.edit(embed=embed)

    @commands.command(aliases=["lb", "leading"])
    async def leaderboard(self, ctx):
        await self.leaderboardData(ctx)

def setup(bot):
    bot.add_cog(Shop(bot))
import discord 
from discord.ext import commands 
import pymongo 
from pymongo import MongoClient as mcl 
import random
import datetime 
from datetime import datetime 

class Blacklisting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.client = self.bot.client
        self.db = self.bot.db 
        self.col = self.bot.banned
        
    @commands.command(description='Ban a user from Santa\'s Sleigh, not allowing them to access any of the commands.', aliases=['bl'], usage='c!blacklist @User <reason>')
    async def blacklist(self, ctx, user: discord.Member = None, *, reason = None):
        self.data = self.col.find_one()
        server = ctx.guild 
        skulls = [
            ":skull_crossbones:",
            ":skull:"
        ]
        if not ctx.author.id in self.bot.admin:
            if ctx.author.id in self.bot.devs:
                pass 
            else:
                return await ctx.send(f":no_entry_sign: **{ctx.author.name}**, you are not an administrator!", delete_after=2)
        if not user:
            return await ctx.send(f":no_entry_sign: **{ctx.author.name}**, you need to specify the user you need to ban.", delete_after=3)
        blacklisted_users = self.data['blacklisted_users']
        document = {"$set": {
            "blacklisted_users": {**blacklisted_users, str(user.id):{"reason": reason, "mod": ctx.author.id}}
        }}
        self.col.update_one({"auth": True}, document)
        skull = random.choice(skulls)
        await ctx.send(f"{skull}  Successfully terminated **{user}**. The user will not be allowed to use Santa's Sleigh commands.")


    @commands.command(description="Veiw a ban that a mod or admin has made on a user.", aliases=['vb', 'baninfo'], usage='c!view-blacklist @User')
    async def viewban(self, ctx, user: discord.Member = None):
        self.data = self.col.find_one()
        server = ctx.guild 
        skulls = [
            ":skull_crossbones:",
            ":skull:"
        ]
        if not ctx.author.id in self.bot.admin:
            if ctx.author.id in self.bot.devs:
                pass 
            else:
                return await ctx.send(f":no_entry_sign: **{ctx.author.name}**, you are not an administrator!", delete_after=2)
        if not user:
            return await ctx.send(f":no_entry_sign: **{ctx.author.name}**, you need to specify the user you need to see.", delete_after=3)        
        if not str(user.id) in self.data["blacklisted_users"]:
            return await ctx.send(f":no_entry_sign: **{ctx.author.name}**, that user is not banned.")
        else:
            blacklisted_users = self.data["blacklisted_users"]
            reason = blacklisted_users[str(user.id)]['reason']
            mod1 = blacklisted_users[str(user.id)]['mod']
            mod = await self.bot.fetch_user(mod1)
            embed = discord.Embed(color=self.bot.embed, timestamp=datetime.utcnow())
            embed.set_author(name=f"{user.name}'s ban information", icon_url=user.avatar_url)
            embed.description = f"""
            **Administrator:** {mod.name} `{mod.id}`
            **Reason:** {reason}
            """
            embed.set_footer(text=user.id)
            await ctx.send(embed=embed)

    @commands.command(description='Whitelist a user, which means allowing access to use the commands.', aliases=['lift'], usage="c!whitelist @User")
    async def whitelist(self, ctx, user: discord.Member = None):
        self.data = self.col.find_one()
        server = ctx.guild 
        skulls = [
            ":skull_crossbones:",
            ":skull:"
        ]
        if not ctx.author.id in self.bot.admin:
            if ctx.author.id in self.bot.devs:
                pass 
            else:
                return await ctx.send(f":no_entry_sign: **{ctx.author.name}**, you are not an administrator!", delete_after=2)
        if not user:
            return await ctx.send(f":no_entry_sign: **{ctx.author.name}**, you need to specify the user you need to unban.", delete_after=3)  
        blacklisted_users = self.data["blacklisted_users"]
        if not str(user.id) in blacklisted_users:
            return await ctx.send(f":no_entry_sign: **{ctx.author.name}**, that user is not banned from the bot.")
        else:
            document = {"$set": {
                "blacklisted_users": {k:v for k,v in blacklisted_users.items() if k != str(user.id)}
            }}
            self.col.update_one({"auth": True}, document)
            await ctx.send(f":pushpin: Successfully unbanned **{user}**!")

def setup(bot):
    bot.add_cog(Blacklisting(bot))
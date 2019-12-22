# import discord 
# from discord.ext import commands 
# import asyncio
# import re
# import datetime

# def convtime(time: str):
#     lw = 604800
#     ld = 86400
#     lh = 3600
#     lm = 60
#     ls = 1
#     letters = {
#         "w": lw,
#         "d": ld,
#         "h": lh,
#         "m": lm,
#         "s": ls
#     }
#     timet = [i for i in re.split(r'(\d+)', time) if i]
#     timelst = [int(i)*letters[j] for i,j in zip(timet[::2],timet[1::2])]
#     return sum(timelst)

# class Testing(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#         self.loop = bot.loop.create_task(self.checker()) 

#     async def checker(self):
#         while True:
#             server = self.bot.get_guild(649031271955300372)
#             channel = server.get_channel(650508787219955712)
#             voice_channel = server.get_channel(649031272877785091) # i believe this is correct idk 
#             print("got here 1")
#             print(datetime.datetime.utcnow().timestamp())
#             async for message in channel.history(limit=1): 
#                 time = message.created_at
#                 print(time)
#                 user = message.author
#                 pass
#             print("got here 2")
#             time1 = convtime(datetime.datetime.utcnow().timestamp() - time)
#             print("here")
#             minutes, seconds = divmod(time1, 60)
#             hours, minutes = divmod(minutes, 60)
#             days, hours = divmod(hours, 24)
#             tm_format = ('weeks','days','hours','minutes','seconds')
#             time_str = " ".join(sorted((f'{y} {x}' for x,y in vars().items() if x in tm_format if y > 0)))
#             await voice_channel.edit(name = f"{time_str} - {user}")
#             await asyncio.sleep(3)

# def setup(bot):
#     bot.add_cog(Testing(bot))
from discord.ext import commands

class ImpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def first_night(self, ctx):
        input("First night!")
        return

    async def night(self, ctx):
        input("Regular night!")
        return

def setup(bot):
    bot.add_cog(ImpCog(bot))
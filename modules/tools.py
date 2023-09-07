import discord
from discord.ext import commands
from discord.commands import slash_command

class ToolsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def hola(self, ctx):
        await ctx.send(f"Hola!")

def setup(bot):
    bot.add_cog(ToolsCog(bot))
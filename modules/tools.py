import discord
from discord.ext import commands
from discord.commands import slash_command

class ToolsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def ping(self, ctx):
        print("Pong")
        await ctx.send(f"Pong!")

def setup(bot):
    bot.add_cog(ToolsCog(bot))
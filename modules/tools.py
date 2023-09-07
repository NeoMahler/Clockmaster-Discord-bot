from discord.ext import commands

class ToolsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def hola(self, ctx):
        await ctx.reply(f"Hola!")

def setup(bot):
    bot.add_cog(ToolsCog(bot))
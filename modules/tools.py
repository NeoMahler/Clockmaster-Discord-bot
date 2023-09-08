from discord.ext import commands

class ToolsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utilities = self.bot.get_cog("UtilitiesCog")
    
    @commands.command()
    async def hola(self, ctx):
        await ctx.reply(f"Hola!")
    
    @commands.command(aliases=['jugadors'])
    async def players(self, ctx):
        players = self.utilities.get_players_names(ctx)
        status = self.utilities.get_state_item("status")
        if status == "join":
            await ctx.reply(f"Hi ha {len(players)} inscrits: **{', '.join(players)}**")
        elif status == "off":
            await ctx.reply(f"El joc no ha començat. Fes !noujoc per començar.")
        else:
            await ctx.reply(f"Encara no he implementat aquesta funció :)")

def setup(bot):
    bot.add_cog(ToolsCog(bot))
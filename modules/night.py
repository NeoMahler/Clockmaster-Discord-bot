from discord.ext import commands

class NightCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utilities = self.bot.get_cog("UtilitiesCog")
    
    async def process_night(self, ctx, first_night = False):
        pass
    

def setup(bot):
    bot.add_cog(NightCog(bot))
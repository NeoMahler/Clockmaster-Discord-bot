from discord.ext import commands

class ControllerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utilities = self.bot.get_cog("UtilitiesCog")
    
    async def game_setup(self, ctx):
        """
        Sets up the game: gives out roles, demon bluffs, and goes to first night.
        """
        if self.utilities.get_state_item('status') == 'on':
            channel = self.bot.get_channel(int(self.bot.config['game_channel']))
            all_pings = " ".join(self.utilities.get_players_pings(ctx))
            await channel.send(f"{all_pings} Comença el joc!")
        return

def setup(bot):
    bot.add_cog(ControllerCog(bot))
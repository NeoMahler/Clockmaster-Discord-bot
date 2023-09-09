from discord.ext import commands

class ControllerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utilities = self.bot.get_cog("UtilitiesCog")
    
    async def game_setup(self, ctx):
        """
        Sets up the game: gives out roles, demon bluffs, and goes to first night.
        """
        if self.utilities.get_config_item("config/game_state.json", 'status') == 'on':
            channel = self.bot.get_channel(int(self.bot.config['game_channel']))
            all_pings = " ".join(self.utilities.get_player_data(ctx, "mention"))
            await channel.send(f"{all_pings} Comença el joc!")

        players = self.utilities.get_player_data(ctx, "username")
        player_num = len(players)
        print(f"There are {player_num} players.")

        # TODO:
        # - get number of players
        # - choose script
        # - choose characters (be mindful of player count for team proportions)
        # - give out characters

def setup(bot):
    bot.add_cog(ControllerCog(bot))
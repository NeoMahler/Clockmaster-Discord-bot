from discord.ext import commands

class ControllerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utilities = self.bot.get_cog("UtilitiesCog")
    
    def game_setup(self):
        if self.utilities.get_config_item('status') == 'on':
            channel = self.bot.get_channel(int(self.bot.config['game_channel']))
            print(self.bot.config['game_channel'] + " " + str(channel))
            channel.send("Comença el joc!")
        return

def setup(bot):
    bot.add_cog(ControllerCog(bot))
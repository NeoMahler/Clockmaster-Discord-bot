from discord.ext import commands
import json

class UtilitiesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def read_game_state(self):
        with open("config/game_state.json", 'r') as f:
            state = json.load(f)
        return state

    def get_config_item(self, key):
        state = self.read_game_state()
        return state[key]
    
    def modify_config_item(self, key, value):
        state = self.read_game_state()
        state[key] = value
        with open("config/game_state.json", 'w') as f:
            json.dump(state, f)

    def add_player(self, player):
        state = self.read_game_state()
        state['players'][str(player)] = {}
        with open("config/game_state.json", 'w') as f:
            json.dump(state, f)
        return
 
def setup(bot):
    bot.add_cog(UtilitiesCog(bot))
import discord
from discord.ext import commands
import subprocess
import random
import json

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utilities = self.bot.get_cog("UtilitiesCog")

    @commands.command()
    @commands.is_owner()
    async def update(self, ctx):
        """
        Pulls the lastest version from GitHub.
        """
        output = subprocess.check_output("git pull", shell=True)
        await ctx.send("Pulling latest version from GitHub: ```" + str(output) + "``` Remember to use the reload command for the changes to take effect.")

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, cog):
        """
        Loads an unloaded module.

        Parameters:
            cog (str): The name of the module to load
        """
        module = "modules." + cog
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send(f':scream: Error: {type(e).__name__} - {e}')
        else:
            await ctx.send('Module loaded! :tada:')
    
    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, cog):
        """
        Unloads a loaded module.
        
        Parameters:
            cog (str): The name of the module to unload
        """
        module = "modules." + cog
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await ctx.send(f':scream: Error: {type(e).__name__} - {e}')
        else:
            await ctx.send('Module unloaded! :tada:')
    
    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog):
        """
        Reloads a module.
        
        Parameters:
            cog (str): The name of the module to reload
        """
        module = "modules." + cog
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send(f':scream: Error: {type(e).__name__} - {e}')
        else:
            await ctx.send('Module reloaded! :tada:')
    
    @commands.command()
    @commands.is_owner()
    async def fjoin(self, ctx, player: discord.User):
        """
        Forcefully adds a user to the game.
        
        Parameters:
            player (discord.User): The user to add to the game.
        """
        self.utilities.add_player(player)
        await ctx.reply(f"Has afegit <@{player.id}> al joc.")
    
    @commands.command()
    @commands.is_owner()
    async def fleave(self, ctx, player: discord.User):
        """
        Forcefully removes a user from the game.
        
        Parameters:
            player (discord.User): The user to remove from the game.
        """
        self.utilities.remove_player(player)
        await ctx.reply(f"Has tret a <@{player.id}> del joc.")
    
    @commands.command(aliases=['fstop'])
    @commands.is_owner()
    async def fend(self, ctx):
        """
        Forcefully ends the game.
        """
        self.utilities.clean_game_state() # Return game_state to starting value
        await ctx.reply("Joc tancat a la força. Si era a mitja partida, no hi ha guanyadors.")

    @commands.command()
    @commands.is_owner()
    async def fjoin_ghost(self, ctx):
        """
        Adds a non-existing user to the game, for debugging purposes.
        """
        random_id = random.randint(0, 999999)
        state = self.utilities.read_config_file("config/game_state.json")
        state['players'][str(random_id)] = {}
        state['players'][str(random_id)]["username"] = "DEBUG"
        state['players'][str(random_id)]["nickname"] = "DEBUG"
        state['players'][str(random_id)]["display_name"] = "DEBUG"
        with open("config/game_state.json", 'w') as f:
            json.dump(state, f)

        await ctx.reply(f"Has afegit un jugador fantasma {random_id} al joc.")
        return

def setup(bot):
    bot.add_cog(AdminCog(bot))
import discord
from discord.ext import commands
import subprocess
import random
import json

class BotAdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # @commands.is_owner()
    # async def update(self, ctx):
    #     """
    #     Pulls the lastest version from GitHub.
    #     """
    #     output = subprocess.check_output("git pull", shell=True)
    #     await ctx.send("Pulling latest version from GitHub: ```" + str(output) + "``` Remember to use the reload command for the changes to take effect.")

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
    
def setup(bot):
    bot.add_cog(BotAdminCog(bot))
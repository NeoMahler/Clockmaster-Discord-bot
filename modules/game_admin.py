import discord
from discord.ext import commands
import subprocess
import random
import json

class GameAdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utilities = self.bot.get_cog("UtilitiesCog")

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
        random_id = random.randint(111111, 999999)
        state = self.utilities.read_config_file("config/game_state.json")
        state['players'][str(random_id)] = {}
        state['players'][str(random_id)]["username"] = f"DEBUG{random_id}"
        state['players'][str(random_id)]["nickname"] = f"DEBUG{random_id}"
        state['players'][str(random_id)]["display_name"] = f"DEBUG{random_id}"
        with open("config/game_state.json", 'w') as f:
            json.dump(state, f)

        await ctx.reply(f"Has afegit un jugador fantasma {random_id} al joc.")
        return

    @commands.command()
    @commands.is_owner()
    async def fstatus(self, ctx, arg = "0"):
        """
        Forcefully changes the status of the game. Accepted values: on, join, off.
        """
        valid_status = ['on', 'join', 'off']
        if arg not in valid_status:
            await ctx.reply("Status invàlid. Només pot ser `on`, `join` i `off`.")
            return
        self.utilities.modify_state_item('status', arg)
        await ctx.reply(f"Status del joc modificat a {arg}.")

    @commands.command()
    @commands.is_owner()
    async def fgetrole(self, ctx, *arg):
        """
        Returns the role of the given player
        """
        try:
            if isinstance(arg, tuple):
                player = " ".join(arg)
            else:
                player = arg
            role = self.utilities.get_player_role(player)
            await ctx.reply(f"{player} és {role}")
        except:
            await ctx.reply("Has d'especificar un jugador vàlid!")

    @commands.command()
    @commands.is_owner()
    async def fgetplayerbyrole(self, ctx, arg):
        """
        Returns the player ID of the given role
        """
        try:
            player = self.utilities.get_player_by_role(ctx, arg)
            await ctx.reply(f"{arg} és {player}")
        except:
            await ctx.reply("Has d'especificar un rol vàlid!")

    @commands.command()
    @commands.is_owner()
    async def fgetteam(self, ctx, *arg):
        """
        Returns the team of the given player
        """
        try:
            if isinstance(arg, tuple):
                player = " ".join(arg)
            else:
                player = arg
            team = self.utilities.get_player_team(player)
            await ctx.reply(f"{player} és {team}")
        except:
            await ctx.reply("Has d'especificar un jugador vàlid!")
    
    @commands.command()
    @commands.is_owner()
    async def fgetteam(self, ctx, arg):
        """
        Returns the members of the given team
        """
        try:
            players = self.utilities.get_players_in_team(ctx, arg)
            await ctx.reply(f"Els membres de l'equip {arg} són {', '.join(players)}")
        except:
            await ctx.reply("Has d'especificar un equip vàlid: `village`, `outsider`, `minion`, `demon`.")

def setup(bot):
    bot.add_cog(GameAdminCog(bot))
from discord.ext import commands
import random

class ControllerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utilities = self.bot.get_cog("UtilitiesCog")
    
    async def game_setup(self, ctx):
        """
        Sets up the game: gives out roles, demon bluffs, and goes to first night.
        """
        # Get player count
        players = self.utilities.get_player_data(ctx, "username")
        player_num = len(players)
        print(f"Hi ha {player_num} jugadors.")

        # Choose script based on player count
        good_scripts = []
        scripts = self.utilities.get_config_item("config/game_config.json", "scripts")
        for script in scripts:
            if scripts[script]["min_players"] <= player_num:
                good_scripts.append(script)
        chosen_script = random.choice(good_scripts)
        script_name = scripts[chosen_script]["name"][self.bot.lang]
        await ctx.send("Guió escollit: " + script_name)

        # Update game state
        if self.utilities.get_config_item("config/game_state.json", 'status') == 'on':
            channel = self.bot.get_channel(int(self.bot.config['game_channel']))
            all_pings = " ".join(self.utilities.get_player_data(ctx, "mention"))
            await channel.send(f"{all_pings} Comença el joc!")

        # Choose characters
        role_count = self.utilities.get_config_item("config/game_config.json", f"scripts/{chosen_script}/role_counts/{str(player_num)}")
        print(f"Role counts: {str(role_count)}")
        chosen_roles = []
        for team in role_count:
            all_team_roles = self.utilities.get_config_item("config/game_config.json", f"scripts/{chosen_script}/{team}")
            chosen_team_roles = random.sample(all_team_roles, k=role_count[team]) # random.sample makes sure there are no duplicates
            chosen_roles.extend(chosen_team_roles)
        print(f"Chosen roles: {', '.join(chosen_roles)}")

        # TODO:
        # - give out characters

def setup(bot):
    bot.add_cog(ControllerCog(bot))
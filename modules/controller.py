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

        # Assign roles to players
        for player in players: # We got players earlier in the function
            assigned_role = random.choice(chosen_roles)
            chosen_roles.remove(assigned_role) # Avoid duplicates
            player_id = self.utilities.get_id_from_data(player, "username")
            self.utilities.modify_state_item(f"players/{player_id}/game_info/role", assigned_role)

            if player == "DEBUG":
                await ctx.send(f"Rol assignat a jugador fantasma {player_id}: **{assigned_role}**")
            else:
                user = self.bot.get_user(int(player_id))
                await user.send(f"T'he assignat el rol **{assigned_role}**!")


def setup(bot):
    bot.add_cog(ControllerCog(bot))
from discord.ext import commands
import random

class ControllerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utilities = self.bot.get_cog("UtilitiesCog")
    
    def choose_script(self, player_num: int):
        """
        Returns a random script based on the player count.

        Parameters:
            player_num (int): The number of players
        
        Returns:
            chosen script (str) and localized script name (str)
        """
        good_scripts = []
        scripts = self.utilities.get_config_item("config/game_config.json", "scripts")
        for script in scripts:
            if scripts[script]["min_players"] <= player_num:
                good_scripts.append(script)
        chosen_script = random.choice(good_scripts)
        script_name = scripts[chosen_script]["name"][self.bot.lang]
        return chosen_script, script_name
    
    def choose_roles(self, chosen_script, player_num: int):
        """
        Choose roles that will be in play and returns them in a list.

        Parameters:
            chosen_script (str): The chosen script key
            player_num (int): The number of players
        """
        role_count = self.utilities.get_config_item("config/game_config.json", f"scripts/{chosen_script}/role_counts/{str(player_num)}")
        print(f"[DEBUG] Role counts: {str(role_count)}")
        chosen_roles = []
        for team in role_count:
            all_team_roles = self.utilities.get_config_item("config/game_config.json", f"scripts/{chosen_script}/{team}")
            chosen_team_roles = random.sample(all_team_roles, k=role_count[team]) # random.sample makes sure there are no duplicates
            chosen_roles.extend(chosen_team_roles)
        
        return chosen_roles

    async def assign_roles(self, ctx, players, chosen_roles):
        """
        Randomly assigns a role to all players.

        Parameters:
            ctx (discord.ext.commands.Context): The context of the command.
            players (list): A list of player usernanmes.
            chosen_roles (list): A list of chosen roles.
        """
        channel = self.bot.get_channel(int(self.bot.config['game_channel']))
        for player in players: # We got players earlier in the function
            assigned_role = random.choice(chosen_roles)
            chosen_roles.remove(assigned_role) # Avoid duplicates
            player_id = self.utilities.get_id_from_data(player)
            self.utilities.modify_state_item(f"players/{player_id}/game_info/role", assigned_role)

            if player.startswith("DEBUG"):
                print(f"Rol assignat a jugador fantasma: {assigned_role}")
            else:
                user = self.bot.get_user(int(player_id))
                try:
                    await user.send(f"T'he assignat el rol **{assigned_role}**!")
                except:
                    await channel.send(f"{user.mention}, no et puc enviar missatges privats. Revisa't la configuració!")


    async def game_setup(self, ctx):
        """
        Sets up the game: gives out roles, demon bluffs, and goes to first night.
        """
        # Get player count and choose script
        players = self.utilities.get_player_data(ctx, "username")
        player_num = len(players)
        print(f"[DEBUG] Hi ha {player_num} jugadors.")

        chosen_script, script_name = self.choose_script(player_num)

        # Announce game starts
        if self.utilities.get_config_item("config/game_state.json", 'status') == 'on':
            channel = self.bot.get_channel(int(self.bot.config['game_channel']))
            all_pings = " ".join(self.utilities.get_player_data(ctx, "mention"))
            await channel.send(f"{all_pings} Comença el joc amb el guió {script_name}!")

        # Choose roles and assign them
        chosen_roles = self.choose_roles(chosen_script, player_num)
        print(f"[DEBUG] Chosen roles: {', '.join(chosen_roles)}")
        await self.assign_roles(ctx, players, chosen_roles)

def setup(bot):
    bot.add_cog(ControllerCog(bot))
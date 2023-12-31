from discord.ext import commands
import json
import dpath

class UtilitiesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def clean_game_state(self):
        """
        Cleans the game_state.json file.
        """
        starting_dictionary = {"players": {}, "day": {"flags": []}, "night": {"flags": []}, "status": "off"}
        with open("config/game_state.json", 'w') as f:
            json.dump(starting_dictionary, f)

    def read_config_file(self, file):
        """
        Reads the provided JSON config file. Returns the entire dictionary.

        Parameters:
            file (str): The full path of the config file
        """
        with open(file, 'r') as f:
            state = json.load(f)
        return state

    def get_config_item(self, file, keys):
        """
        Returns the value of a config item in a dictionary that is multiple levels deep.
    
        Parameters:
            file (str): The full path to the config file.
            keys (string): A string of keys separated by /.
    
        Returns:
            The value of the config item if found, or None if not found.
        """
        dict = self.read_config_file(file)
        value = dpath.get(dict, keys)
        return value

    def modify_state_item(self, key, value):
        """
        Modifies a config item.
        
        Parameters:
            key (str): The name of the config item.
            value (str): The new value of the config item.
        """
        state = self.read_config_file("config/game_state.json")
        dpath.new(state, key, value)
        with open("config/game_state.json", 'w') as f:
            json.dump(state, f)
    
    def edit_flags(self, type, flags):
        """
        Edits flags from players, day or night. It can edit multiple flags at once.

        Parameters:
            type (str): can be the ID of a player, "day", or "night".
            flags (list): A list of flags to edit. Use + in front of the flag to add it, - to remove it.
        """
        current_flags = self.get_flags(type)

        if type in ["day", "night"]: # It's a player
            path = f"{type}/flags"
        else:
            path = f"players/{type}/game_info/flags"
        
        for flag in flags:
            if flag.startswith('-'):
                current_flags.remove(flag[1:])
            elif flag.startswith('+'):
                current_flags.append(flag[1:])
        
        self.modify_state_item(path, current_flags)

    def get_flags(self, type):
        """
        Returns a list of flags from players, day or night.

        Parameters:
            type (str): can be the ID of a player, "day", or "night".
        """
        if not type in ["day", "night"]: # It's a player
            all_players = self.get_config_item("config/game_state.json", "players")
            if not type in all_players:
                print(f"[ERROR] Couldn't get player {type} when attempting to view their flags. Use an ID instead")
                return
            current_flags = self.get_config_item("config/game_state.json", f"players/{type}/game_info/flags")
        else:
            current_flags = self.get_config_item("config/game_state.json", f"{type}/flags")

        return current_flags
    
    def add_player(self, player):
        """
        Adds a player to the game. It includes the user ID, username, and server-specific nickname.

        Parameters:
            player (discord.User): The user to add to the game.
        """
        state = self.read_config_file("config/game_state.json")
        state['players'][str(player.id)] = {}
        state['players'][str(player.id)]["username"] = player.name
        state['players'][str(player.id)]["display_name"] = player.display_name
        try:
            state['players'][str(player.id)]["nickname"] = player.nick
        except AttributeError:
            state['players'][str(player.id)]["nickname"] = player.display_name
        state['players'][str(player.id)]["game_info"] = {"role": "", "flags": []}
        with open("config/game_state.json", 'w') as f:
            json.dump(state, f)
        return
    
    def remove_player(self, player):
        """
        Removes a player from the game.

        Parameters:
            player (discord.User): The user to remove from the game.
        """
        state = self.read_config_file("config/game_state.json")
        del state['players'][str(player.id)]
        with open("config/game_state.json", 'w') as f:
            json.dump(state, f)
        return
    
    def get_player_data(self, ctx, type, players=[]):
        """
        Returns either the mention, username, display_name, or nickname of a player.

        Parameters:
            ctx (discord.ext.commands.Context): The context of the command.
            type (str): The type of data to return.
            players (list): A list of Discord user IDs.
        """
        data = []
        added_players = self.get_config_item("config/game_state.json", "players")

        if players != []: # Create a list of players only for the specified user
            for player in added_players:
                if player in players:
                    if len(player) == 6: # Ghost players have 6-digit IDs
                        data.append("DEBUG")
                    else:
                        user = ctx.guild.get_member(int(player))
                        data.append(self.sort_player_info(type, user))
        else: # Create list for all players added to the game
            for player in added_players:
                if len(player) == 6: # Ghost players have 6-digit IDs
                    data.append("DEBUG")
                else:
                    user = ctx.guild.get_member(int(player))
                    data.append(self.sort_player_info(type, user))
        return data
    
    def sort_player_info(self, type, user):
        """
        Sorts the player information based on the given type.

        Parameters:
            type (str): The type of information to sort. Valid values are "mention", "username", "display_name", and "nickname".
            user (User): The user object containing the player information.
        """
        if type == "mention":
            return user.mention
        elif type == "username":
            return user.name
        elif type == "display_name":
            return user.display_name
        elif type == "nickname":
            if user.nick == None:
                return user.display_name
            else:
                return user.nick
        elif type == "user":
            return user
        
    def get_id_from_data(self, data):
        """
        Returns the ID of a player based on the given data.

        Parameters:
            data (str): The data to match against the username, nickname, or display_name of a player.

        Returns:
            int: The ID of the player.
        """
        state = self.read_config_file("config/game_state.json")
        players = state["players"]
        for player_id, player_data in players.items():
            for key, value in player_data.items():
                if isinstance(value, str) and value.lower() == data.lower(): # .lower() is necessary because people type weird
                    return int(player_id)

        try: # Handle direct mentions
            player_id = data.replace("<@", "").replace(">", "")
            return int(player_id)
        except Exception as e:
            print(f"[ERROR] Exception occurred: {str(e)}")
            return None  # Return None if player is not found

    def get_player_role(self, player):
        """
        Returns the player's role (str) based on their Discord ID. Always returns the real role of the user.
        """
        state = self.read_config_file("config/game_state.json")
        player_id = self.get_id_from_data(player)
        role = state["players"][str(player_id)]["game_info"]["role"]
        return role
    
    def get_player_by_role(self, ctx, role):
        """
        Returns the player's Discord ID based on their role (str).
        """
        state = self.read_config_file("config/game_state.json")
        players = state["players"]
        for player_id, player_data in players.items():
            if player_data["game_info"]["role"] == role:
                player = self.get_player_data(ctx, "nickname", [str(player_id)])
                return player[0]

    def get_player_team(self, player):
        """
        Returns the player's team (str) based on their Discord ID. Always returns the real team of the user.
        """
        role = self.get_player_role(player)
        role_flags = self.get_config_item("config/game_config.json", f"roles/{role}/flags")
        if "is_village" in role_flags:
            return "village"
        elif "is_outsider" in role_flags:
            return "outsider"
        elif "is_minion" in role_flags:
            return "minion"
        elif "is_demon" in role_flags:
            return "demon"
        
    def get_players_in_team(self, ctx, team):
        """
        Returns a list of all players in the given team.
        """
        players_in_team = []
        for player in self.read_config_file("config/game_state.json")["players"]:
            if self.get_player_team(player) == team:
                user = self.get_player_data(ctx, "nickname", [str(player)])
                players_in_team.append(user[0])
        return players_in_team
    
    def roles_in_play(self):
        """
        Returns a list of all roles in play in the current game.
        """
        roles_in_play = []

        for player in self.read_config_file("config/game_state.json")["players"]:
            role = self.get_player_role(player)
            roles_in_play.append(role)
        
        return roles_in_play

    def order_roles(self, script, roles, first_night = True):
        """
        Returns the list provided as 'roles' ordered according to the script's night order.
        If first night, use first_night=True.
        """
        if first_night:
            role_order = self.get_config_item("config/game_config.json", f"scripts/{script}/first_night_order")
        else:
            role_order = self.get_config_item("config/game_config.json", f"scripts/{script}/general_night_order")
        
        ordered_list = [item for item in role_order if item in roles]
        return ordered_list

def setup(bot):
    bot.add_cog(UtilitiesCog(bot))
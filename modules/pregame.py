from discord.ext import commands

class PregameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utilities = self.bot.get_cog("UtilitiesCog")
        self.controller = self.bot.get_cog("ControllerCog")

    @commands.command(aliases=['new', 'noujoc', 'nou'])
    async def newgame(self, ctx):
        """
        Launches a new game.
        """
        if self.utilities.get_state_item('status') == 'on':
            return
        if self.utilities.get_state_item('status') != 'off':
            await ctx.reply("Ja hi ha un joc en curs. Utilitza !entrar per entrar al joc.")
            return
        
        self.utilities.modify_state_item('status', 'join')

        game_role = self.bot.config['game_role']
        user = ctx.author
        if str(ctx.channel.id) != self.bot.config['game_channel']: # Prevent games outside of the game channel
            await ctx.reply(f"Només pots iniciar un joc nou a <#{self.bot.config['game_channel']}>.")
            return

        self.utilities.add_player(user)
        await ctx.send(f"<@&{game_role}>, comença un nou joc! <@{user.id}>, t'he afegit automàticament a la llista de jugadors. La resta, feu !entrar per entrar al joc.")

    @commands.command(aliases=['entrar'])
    async def join(self, ctx):
        """
        Adds the user to the game.
        """
        if self.utilities.get_state_item('status') == 'on':
            return
        if self.utilities.get_state_item('status') != 'join':
            await ctx.reply("No hi ha cap joc en curs; utilitza !nou per iniciar un nou joc.")
            return
        
        if str(ctx.author.id) in self.utilities.get_state_item('players'):
            await ctx.reply("Ja estàs inscrit al joc. La paciència és la mare de la ciència.")
        else:
            self.utilities.add_player(ctx.author)
            await ctx.reply("Has entrat al joc.")
        return

    @commands.command(aliases=['sortir'])
    async def leave(self, ctx):
        """
        Removes the user from the game.
        """
        if self.utilities.get_state_item('status') == 'on':
            return
        if self.utilities.get_state_item('status') != 'join':
            await ctx.reply("No hi ha cap joc en curs; utilitza !nou per iniciar un nou joc.")
            return
        
        if str(ctx.author.id) in self.utilities.get_state_item('players'):
            self.utilities.remove_player(ctx.author)
            await ctx.reply("Has sortit del joc.")

    @commands.command(aliases=['iniciar'])
    async def start(self, ctx):
        """
        Starts the game by going to the setup phase.
        """
        self.utilities.modify_state_item('status', 'on')
        await self.controller.game_setup(ctx)

def setup(bot):
    bot.add_cog(PregameCog(bot))
from discord.ext import commands

class PregameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utilities = self.bot.get_cog("UtilitiesCog")
        self.controller = self.bot.get_cog("ControllerCog")

    @commands.command(aliases=['new', 'noujoc', 'nou'])
    async def newgame(self, ctx):
        if self.utilities.get_config_item('status') == 'on':
            return
        if self.utilities.get_config_item('status') != 'off':
            await ctx.reply("Ja hi ha un joc en curs. Utilitza !entrar per entrar al joc.")
            return
        
        self.utilities.modify_config_item('status', 'join')

        game_role = self.bot.config['game_role']
        user_id = ctx.author.id
        if str(ctx.channel.id) != self.bot.config['game_channel']: # Prevent games outside of the game channel
            await ctx.reply(f"Només pots iniciar un joc nou a <#{self.bot.config['game_channel']}>.")
            return

        self.utilities.add_player(user_id)
        await ctx.send(f"<@&{game_role}>, comença un nou joc! <@{user_id}>, t'he afegit automàticament a la llista de jugadors. La resta, feu !entrar per entrar al joc.")

    @commands.command(aliases=['entrar'])
    async def join(self, ctx):
        if self.utilities.get_config_item('status') == 'on':
            return
        if self.utilities.get_config_item('status') != 'join':
            await ctx.reply("No hi ha cap joc en curs; utilitza !nou per iniciar un nou joc.")
            return
        
        if str(ctx.author.id) in self.utilities.get_config_item('players'):
            await ctx.reply("Ja estàs inscrit al joc. La paciència és la mare de la ciència.")
        else:
            self.utilities.add_player(ctx.author.id)
            await ctx.reply("Has entrat al joc.")
        return

    @commands.command(aliases=['sortir'])
    async def leave(self, ctx):
        if self.utilities.get_config_item('status') == 'on':
            return
        if self.utilities.get_config_item('status') != 'join':
            await ctx.reply("No hi ha cap joc en curs; utilitza !nou per iniciar un nou joc.")
            return
        
        if str(ctx.author.id) in self.utilities.get_config_item('players'):
            self.utilities.remove_player(ctx.author.id)
            await ctx.reply("Has sortit del joc.")

    @commands.command(aliases=['iniciar'])
    async def start(self, ctx):
        self.utilities.modify_config_item('status', 'on')
        self.controller.game_setup()

def setup(bot):
    bot.add_cog(PregameCog(bot))
from discord.ext import commands

class PregameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utilities = self.bot.get_cog("UtilitiesCog")

    @commands.command(aliases=['new', 'noujoc', 'nou'])
    async def newgame(self, ctx):
        if self.utilities.get_config_item('status') != 'off':
            await ctx.send("Ja hi ha un joc en curs. Utilitza !entrar per entrar al joc.")
            return
        elif self.utilities.get_config_item('status') == 'on':
            return
        
        self.utilities.modify_config_item('status', 'join')

        game_role = self.bot.config['game_role']
        user_id = ctx.author.id
        if str(ctx.channel.id) != self.bot.config['game_channel']: # Prevent games outside of the game channel
            await ctx.send(f"<@{user_id}>, només pots iniciar un joc nou a <#{self.bot.config['game_channel']}>.")
            return

        self.utilities.add_player(user_id)
        await ctx.send(f"<@&{game_role}>, comença un nou joc! <@{user_id}>, t'he afegit automàticament a la llista de jugadors. La resta, feu !entrar per entrar al joc.")


#### TODO: when game starts, status switches to on

def setup(bot):
    bot.add_cog(PregameCog(bot))
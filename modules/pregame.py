from discord.ext import commands

class PregameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['new', 'noujoc', 'nou'])
    async def newgame(self, ctx):
        game_role = self.bot.config['game_role']
        user_id = ctx.author.id
    
        if ctx.channel.id != self.bot.config['game_channel']: # Prevent games outside of the game channel
            await ctx.send(f"<@{user_id}>, només pots iniciar un joc nou a <#{self.bot.config['game_channel']}>.")
            return

        await ctx.send(f"<@&{game_role}>, comença un nou joc! <@{user_id}>, t'he afegit automàticament a la llista de jugadors. La resta, feu !entrar per entrar al joc.")

def setup(bot):
    bot.add_cog(PregameCog(bot))
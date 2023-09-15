from discord.ext import commands

class NightCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utilities = self.bot.get_cog("UtilitiesCog")
    
    async def process_night(self, ctx, roles, script, first_night = False):
        if first_night:
            night_order = self.utilities.order_roles(script, roles, first_night=True)
            print("[DEBUG] Beginning first night")
        else:
            night_order = self.utilities.order_roles(script, roles, first_night=False)
            print("[DEBUG] Beginning night")
        
        print(f"[DEBUG] Night order: {', '.join(night_order)}")
        for role in night_order:
            print("[DEBUG] Night phase for " + role)
            # role_module = self.bot.get_cog(f"{role.upper()}Cog")
            role_module = self.bot.get_cog(f"ImpCog") # Force imp role for debugging purposes
            if first_night:
                await role_module.first_night(ctx)
            else:
                await role_module.night(ctx)
    

def setup(bot):
    bot.add_cog(NightCog(bot))
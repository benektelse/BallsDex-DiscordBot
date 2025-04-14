import logging
import time
from typing import TYPE_CHECKING

from discord.ext import commands
from tortoise import Tortoise

log = logging.getLogger("ballsdex.core.commands")

if TYPE_CHECKING:
    from .bot import BallsDexBot


class Core(commands.Cog):
    """
    Core commands of BallsDex bot
    """

    def __init__(self, bot: "BallsDexBot"):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """
        Ping!
        """
        await ctx.send("Pong")

    @commands.command()
    @commands.is_owner()
    async def reloadtree(self, ctx: commands.Context):
        """
        Sync the application commands with Discord
        """
        await self.bot.tree.sync()
        await ctx.send("Application commands tree reloaded.")

    async def reload_package(self, package: str, *, with_prefix=False):
        try:
            try:
                await self.bot.reload_extension(package)
            except commands.ExtensionNotLoaded:
                await self.bot.load_extension(package)
        except commands.ExtensionNotFound:
            if not with_prefix:
                return await self.reload_package("ballsdex.packages." + package, with_prefix=True)
            raise

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, package: str):
        """
        Reload an extension
        """
        try:
            await self.reload_package(package)
        except commands.ExtensionNotFound:
            await ctx.send("Extension not found.")
        except Exception:
            await ctx.send("Failed to reload extension.")
            log.error(f"Failed to reload extension {package}", exc_info=True)
        else:
            await ctx.send("Extension reloaded.")

    @commands.command()
    @commands.is_owner()
    async def reloadcache(self, ctx: commands.Context):
        """
        Reload the cache of database models.

        This is needed each time the database is updated, otherwise changes won't reflect until
        next start.
        """
        
        await self.bot.load_cache()
        from ballsdex.core.models import balls, specials
        from datetime import datetime
        from tortoise.timezone import now as datetime_now

        enabled_balls = {x: y for x, y in balls.items() if y.enabled}
    
        # Count spawnable specials (within their date range)
        spawnable_specials = {
            x: y for x, y in specials.items() 
            if (y.start_date is None or y.start_date <= datetime_now()) 
            and (y.end_date is None or y.end_date >= datetime_now())
        }
    
        total_specials = len(spawnable_specials)
        total_enabled_balls = len(enabled_balls)

        log.info(f"Reloaded cache. Total enabled balls: {total_enabled_balls}, Total spawnable specials: {total_specials}")
        await ctx.message.add_reaction("🔥")

    @commands.command()
    @commands.is_owner()
    async def analyzedb(self, ctx: commands.Context):
        """
        Analyze the database. This refreshes the counts displayed by the `/about` command.
        """
        connection = Tortoise.get_connection("default")
        t1 = time.time()
        await connection.execute_query("ANALYZE")
        t2 = time.time()
        await ctx.send(f"Analyzed database in {round((t2 - t1) * 1000)}ms.")

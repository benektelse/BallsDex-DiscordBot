import logging
import random
import string
from datetime import datetime

import discord

from ballsdex.core.models import Ball, balls
from ballsdex.packages.countryballs.components import CatchView
from ballsdex.settings import settings

log = logging.getLogger("ballsdex.packages.countryballs")

spwnmsglist = ["To spawn or not to spawn? An icon’s dilemma.", "I wonder what the lore is behind these icons.", "NiezzeQ got nothing on this icon.", "Please be Zoink, please be Zoink...", "How many of these are gonna spawn???", "There’s a 1 in 1 billion chance of this spawn message being a slur.", "A wild icon appeared!", "Is this even an icon? What constitutes as an icon anymore?", "Please be a shiny...", "Why are you grinding IconDex? Don’t you have other stuff to do?", "PieceOfTrash184 was here.", "Lambo was here.", "Athani was here.", "Tokyo was here.", "Exatl was here.", "Benektelse was here.", "What if the real icons were the friends we made along the way?", "I’m so tired of writing these.", "August 21st, 2023. Never forget what we suffered...", "June 28th is IconDex’s birthday!", "You should join the IconDex official server, unless you’re already there...", "I love icons.", "This is an icon.", "I bet you want a 100k special on this.", "PLEASE be a top 3 special...", "Rarity trials card pretty please?", "This is so draining.", "Robtop be like: Geometry Dash.", "This icon is referred to as Uncle Mitch.", "John Appleseed was here.", "This icon: My name is GEORGE!!!", "These were all written on May 29th of 2024.", "The biggest streak of luck ever seen in IconDex occurred on September 25th 2023.", "May 25th killed Galaxy KYWY and Gold Eandis.", "They ain’t believe in us... GOD DIDn’t.", "In life... you got Roblox.", "What am I doing with my time?", "Seventeenth month, waiting for the next addition wave to come out.", "🔥", "Love’s gonna get you killed, but Pride’s gonna be the death of you...", "Oh, Lamar! Hail Mary and marijuana, times is hard!", "Kendrick won the beef. Also, here’s an icon.", "R.I.P. to MyUsername. The OG IconDex Anarchist.", "They call me asparagus.", "TELL EM TO BRING THE YACHT OUT 🗣", "This icon is so silly."]

class CountryBall:
    def __init__(self, model: Ball):
        self.name = model.country
        self.model = model
        self.message: discord.Message = discord.utils.MISSING
        self.catched = False
        self.time = datetime.now()

    @classmethod
    async def get_random(cls):
        countryballs = list(filter(lambda m: m.enabled, balls.values()))
        if not countryballs:
            raise RuntimeError("No ball to spawn")
        rarities = [x.rarity for x in countryballs]
        cb = random.choices(population=countryballs, weights=rarities, k=1)[0]
        return cls(cb)

    async def spawn(self, channel: discord.TextChannel):
        def generate_random_name():
            source = string.ascii_uppercase + string.ascii_lowercase + string.ascii_letters
            return "".join(random.choices(source, k=15))

        extension = self.model.wild_card.split(".")[-1]
        file_location = "." + self.model.wild_card
        file_name = f"nt_{generate_random_name()}.{extension}"
        try:
            permissions = channel.permissions_for(channel.guild.me)
            if permissions.attach_files and permissions.send_messages:
                self.message = await channel.send((random.choice(spwnmsglist)),
                    view=CatchView(self),
                    file=discord.File(file_location, filename=file_name),
                )
            else:
                log.error("Missing permission to spawn ball in channel %s.", channel)
        except discord.Forbidden:
            log.error(f"Missing permission to spawn ball in channel {channel}.")
        except discord.HTTPException:
            log.error("Failed to spawn ball", exc_info=True)

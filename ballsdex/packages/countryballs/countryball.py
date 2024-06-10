import logging
import random
import string
from datetime import datetime

import discord

from ballsdex.core.models import Ball, balls
from ballsdex.packages.countryballs.components import CatchView
from ballsdex.settings import settings

log = logging.getLogger("ballsdex.packages.countryballs")

spwnmsglist = ["To spawn or not to spawn? An icon’s dilemma.", "I wonder what the lore is behind these icons.", "NiezzeQ got nothing on this icon.", "Please be a shiny, please be a shiny...", "How many of these are gonna spawn???", "There’s a 1 in 1 billion chance of this spawn message being a slur.", "A wild icon appeared!", "Is this even an icon? What constitutes as an icon anymore?", "Please be a shiny...", "Why are you grinding IconDex? Don’t you have other stuff to do?", "PieceOfTrash184 was here.", "Lambo was here.", "Athani was here.", "Tokyo was here.", "Exatl was here.", "Benektelse was here.", "What if the real icons were the friends we made along the way?", "I’m so tired of writing these.", "August 21st, 2023. Never forget what we suffered...", "June 28th is IconDex’s birthday!", "You should join the IconDex official server, unless you’re already there...", "I love icons.", "This is an icon.", "I bet you want a 100k special on this.", "PLEASE be a Top 5 special...", "Rarity trials card pretty please?", "This is so draining.", "Robtop be like: Geometry Dash.", "This icon is referred to as Uncle Mitch.", "John Appleseed was here.", "This icon: My name is GEORGE!!!", "How many rich people have gone unnoticed?", "The biggest streak of luck ever seen in IconDex occurred on September 25th 2023.", "May 25th killed Galaxy KYWY and Gold Eandis.", "They ain’t believe in us... GOD DIDn’t.", "In life... you got Roblox.", "What am I doing with my time?", "Seventeenth month, waiting for the next addition wave to come out.", "🔥", "Love’s gonna get you killed, but Pride’s gonna be the death of you...", "Oh, Lamar! Hail Mary and marijuana, times is hard!", "Kendrick won the beef. Also, here’s an icon.", "IconDex has a history of problematic members. They have all been banned. Icon time!", "They call me asparagus.", "TELL EM TO BRING THE YACHT OUT 🗣", "This icon is so silly.", "Be rare or be square.", "An icon spawned… what’s it gonna be?", "What you want, you an Orion? Lazerblitz? A Dorabae and a Bunch? OSIRIS? Cobrablitz?", "Every icon is a star, every icon is a star...", "Childish Lambino - Because the Icons.", "IconDex is the best dex, except maybe MCDex.", "With great icons, comes great memorization.", "Icons be like: bruh I'm square.", "Please catch me… I could be a 0.1…", "Imagine how rich you would be if you caught me!", "IconDex works its magic again.", "We love catching icons!", "me when I air the top 1", "IconDex.", "smokin on yo top 5 tonight", "Catch me, or else…", "A wise man once said: IconDex.", "If you like sparkling water, you don’t deserve an icon." "Playboi 'Thani - Whole Lotta Bias", "To Catch an Icon.", "Only 0.00001% can catch this icon.", "Remember the differences between Riot and ASBCHazel...", "Is this an icon?", "Are you sure this is an icon?", "How do icons even work?", "There will always be another icon...", "I wonder how many people have heard of IconDex.", "Tokyo's Revenge - Icon Lullaby", "If you're reading this, you should catch this icon.", "They not icons, they not icons, they not icons...", "Everybody wanna beat demons, 'til they get chipped by the easy game...", "5 percent will get in comp, but 95 is void...", "YouTube pranked Technical way too hard...", "More icons?", "It's insane how many icons can spawn.", "IconDex has been copied from multiple times.", "That's useless, I got icons to catch, but I can see you don't know 'nun 'bout that.", "Icons, icons, icons...", "This idea was taken from Pixeldex. Go play their dex!", "Benektelse's mashups go hard. This icon loves them!"]

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

    async def spawn(self, channel: discord.TextChannel) -> bool:
        """
        Spawn a countryball in a channel.
        Parameters
        ----------
        channel: discord.TextChannel
            The channel where to spawn the countryball. Must have permission to send messages
            and upload files as a bot (not through interactions).
        Returns
        -------
        bool
            `True` if the operation succeeded, otherwise `False`. An error will be displayed
            in the logs if that's the case.
        """

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
                return True
            else:
                log.error("Missing permission to spawn ball in channel %s.", channel)
        except discord.Forbidden:
            log.error(f"Missing permission to spawn ball in channel {channel}.")
        except discord.HTTPException:
            log.error("Failed to spawn ball", exc_info=True)
        return False
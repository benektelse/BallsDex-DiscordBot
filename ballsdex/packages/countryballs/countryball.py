import logging
import random
import string
from datetime import datetime

import discord

from ballsdex.core.models import Ball, balls
from ballsdex.packages.countryballs.components import CatchView
from ballsdex.settings import settings

log = logging.getLogger("ballsdex.packages.countryballs")

spwnmsglist = ["To spawn or not to spawn? An icon’s dilemma.", "I wonder what the lore is behind these icons.", "NiezziQ got nothing on this icon.", "Please be a shiny, please be a shiny...", "How many of these are gonna spawn???", "There’s a 1 in 1 billion chance of this spawn message being an insult.", "A wild icon appeared!", "Is this even an icon? What constitutes as an icon anymore?", "Please be a shiny...", "Why are you grinding IconDex? Don’t you have other stuff to do?", "PieceOfTrash184 was here.", "Lambo was here.", "Evelyn was here.", "Cellar was here.", "Exatl was here.", "Benektelse was here.", "What if the real icons were the friends we made along the way?", "I’m so tired of writing these.", "August 21st, 2023. Never forget what we suffered...", "June 28th is IconDex’s birthday!", "You should join the IconDex official server, unless you’re already there...", "I love icons.", "This is an icon.", "I bet you want a 100k special on this.", "PLEASE be a Top 5 special...", "Rarity trials card pretty please?", "This is so draining.", "Robtop be like: Geometry Dash.", "This icon is referred to as Uncle Mitch.", "John Appleseed was here.", "This icon: My name is GEORGE!!!", "How many rich people have gone unnoticed?", "The biggest streak of luck ever seen in IconDex occurred on September 25th 2023.", "May 25th killed Galaxy KYWY and Gold Eandis.", "They ain’t believe in us... GOD DIDn’t.", "In life... you got Roblox.", "What am I doing with my time?", "Seventeenth month, waiting for the next addition wave to come out.", "🔥", "Love’s gonna get you killed, but Pride’s gonna be the death of you...", "Oh, Lamar! Hail Mary and marijuana, times is hard!", "Kendrick won the beef. Also, here’s an icon.", "If you think IconDex is weird, you're weird.", "They call me asparagus.", "TELL EM TO BRING THE YACHT OUT 🗣", "This icon is so silly.", "Be rare or be square.", "An icon spawned… what’s it gonna be?", "What you want you, an Orion? Lazerblitz? A Dorabae and a Bunch? OSIRIS? Pasiblitz?", "Every icon is a star, every icon is a star...", "Childish Lambino - Because the Icons.", "IconDex is the best dex, except maybe MCDex.", "With great icons, comes great memorization.", "Icons be like: bruh I'm square.", "Please catch me… I could be a 0.1…", "Imagine how rich you would be if you caught me!", "IconDex works its magic again.", "We love catching icons!", "me when I air the top 1", "IconDex.", "smokin on yo top 5 tonight", "Catch me, or else…", "A wise man once said: IconDex.", "If you like sparkling water, you don’t deserve an icon.", "Playboi Larry - Whole Lotta Bias", "To Catch an Icon.", "Only 0.00001% can catch this icon.", "Remember the differences between Riot and ASBCHazel...", "Is this an icon?", "Are you sure this is an icon?", "How do icons even work?", "There will always be another icon...", "I wonder how many people have heard of IconDex.", "The Cellar Path by JamAttack.", "If you're reading this, you should catch this icon.", "They not icons, they not icons, they not icons...", "Everybody wanna beat demons, 'til they get chipped by the easy game...", "5 percent will get in comp, but 95 is void...", "YouTube pranked Technical way too hard...", "More icons?", "It's insane how many icons can spawn.", "IconDex has been copied from multiple times.", "That's useless, I got icons to catch, but I can see you don't know 'nun 'bout that.", "Icons, icons, icons...", "Benektelse's mashups go hard. This icon loves them!", "Can't let her grow up in that icon collection.", "I LOVE CATCHING ICONS!", "How many noobies in the house? How many noobies in the house without a Klaux?", "The bigger the collection, the better the specials.", "It's funny how PieceofTrash184 and Lambo might go to war, two elites that wanna build and destroy.", "When Spyro caught the #10000, was you still a fan?", "But while my loved ones was fighting the continuous war back in the city, I was entering a new one. A war that was based on copying and pasting.", "We want icons! Now if I give you icons, you gon' take em?", "Twenty-four seven, three sixty-five, IconDex stays on my mind.", "Have you seen the silly icon?", "If you don't join IconDex, you're a strange little fella","man idk what to put here just catch me","Lieutenant wrote this at 4:14am. CATCH ME!!!", "Everything was t1.5 in the beginning, why do you even care?", "He once told me he wasn't Teamhax, but only Teamhax uses that icon...", "He says he isn't Exen, but I didn't believe him!", "Where's Kvo82?", "It spawned...? Literally icon bias.", "Have you sent it to RobTop yet?", "I've heard that Amoeba had played a prank on 4y4 once.", "DAMBREARON MADE PROMETHEAN!!!", "I would rather win a good giveaway than continue to catch all of these WORTHLESS commons...", "No need to worry about the differences between Zylenox and Zeroxy.", "Did you know this icon has a 0% chance to strike gold?", "I bet this icon is so rare that it compares to NiezziQ.", "I love NiezziQ.", "Promise that you will catch this icon.", "I got- I got- I got- I got- Zylenox, TheRealDarnoc, inside of IconDex.", "Now if I catch this icon... and it just came out recently... and I get comp from that icon... I'm a public enemy.", "I never caught that many icons, never got rich outside of my servers. But I never could type on, it's a mess of buttons under cursors.", "Don't fumble the bag... Lieutenant will never live it down.", "The invite link in IconDex's about command works, after over a year!", "Evil benektelse be like: SpikeDex", "Too many IconDex players tease themselves with a Michigun.", "The Historydex-IconDex beef runs deep.", "Never trust someone with 3 hands!", "She don't believe in IconDex, but she believes in icons to flex.", "You are a very funny community of people.", "IconDex is so gay, and I couldn't be happier.", "I pray my comp get big as the Eiffel Tower, so I can flex on you for 72 hours.", "No one man should have all those icons. The clocks tickin, I just count the bygones.", "My mind is livin on Cloud 9...", "Only real ones know about the Rarity Trials Daniel Dumile.", "Newgen vs Oldgen: A Tale as Old as Time.", "Also try MCDex!", "Are you really silly?", "Go give Layla a Vatican.", "Lambo REALLY doesn't like when IconDex changes.", "bleep blorp icon time", "this is literally icondex if it was real", "i like the icon,,,", "This icon loves lasagna.", "People of IconDex, gather round... an icon has befallen us."]

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
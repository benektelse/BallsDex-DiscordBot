from __future__ import annotations

import logging
import math
import random
import string
from datetime import datetime
from typing import TYPE_CHECKING

import discord
from discord.ui import Button, Modal, TextInput, View, button
from tortoise.timezone import get_default_timezone
from tortoise.timezone import now as tortoise_now

from ballsdex.core.metrics import caught_balls
from ballsdex.core.models import (
    Ball,
    BallInstance,
    Player,
    Special,
    Trade,
    TradeObject,
    balls,
    specials,
)
from ballsdex.settings import settings

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot

log = logging.getLogger("ballsdex.packages.countryballs")

spwnmsglist = ["To spawn or not to spawn? An icon’s dilemma.", "I wonder what the lore is behind these icons.", "NiezziQ got nothing on this icon.", "Please be a shiny, please be a shiny...", "How many of these are gonna spawn???", "There’s a 1 in 1 billion chance of this spawn message being an insult.", "A wild icon appeared!", "Is this even an icon? What constitutes as an icon anymore?", "Please be a shiny...", "Why are you grinding IconDex? Don’t you have other stuff to do?", "PieceOfTrash184 was here.", "Lamia was here.", "Evelyn was here.", "Who is Orble?", "Exatl was here.", "Benektelse was here.", "What if the real icons were the friends we made along the way?", "I’m so tired of writing these.", "August 21st, 2023. Never forget what we suffered...", "June 28th is IconDex’s birthday!", "You should join the IconDex official server, unless you’re already there...", "I love icons.", "This is an icon.", "I bet you want a 100k special on this.", "PLEASE be a Top 5 special...", "Rarity trials card pretty please?", "This is so draining.", "Robtop be like: Geometry Dash.", "This icon is referred to as Uncle Mitch.", "John Appleseed was here.", "This icon: My name is GEORGE!!!", "How many rich people have gone unnoticed?", "The biggest streak of luck ever seen in IconDex occurred on September 25th 2023.", "May 25th killed Galaxy KYWY and Gold Eandis.", "They ain’t believe in us... GOD DIDn’t.", "In life... you got Roblox.", "What am I doing with my time?", "Seventeenth month, waiting for the next addition wave to come out.", "🔥", "Love’s gonna get you killed, but Pride’s gonna be the death of you...", "Oh, Lamar! Hail Mary and marijuana, times is hard!", "Kendrick won the beef. Also, here’s an icon.", "If you think IconDex is weird, you're weird.", "They call me asparagus.", "TELL EM TO BRING THE YACHT OUT 🗣", "This icon is so silly.", "Be rare or be square.", "An icon spawned… what’s it gonna be?", "What you want you, an Orion? Lazerblitz? A Dorabae and a Bunch? OSIRIS? Pasiblitz?", "Every icon is a star, every icon is a star...", "Childish Lambino - Because the Icons.", "IconDex is the best dex, except maybe MCDex.", "With great icons, comes great memorization.", "Icons be like: bruh I'm square.", "Please catch me… I could be a 0.1…", "Imagine how rich you would be if you caught me!", "IconDex works its magic again.", "We love catching icons!", "me when I air the top 1", "IconDex.", "smokin on yo top 5 tonight", "Catch me, or else…", "A wise man once said: IconDex.", "If you like sparkling water, you don’t deserve an icon.", "Playboi Larry - Whole Lotta Bias", "To Catch an Icon.", "Only 0.00001% can catch this icon.", "Remember the differences between Riot and ASBCHazel...", "Is this an icon?", "Are you sure this is an icon?", "How do icons even work?", "There will always be another icon...", "I wonder how many people have heard of IconDex.", "whizkid05 is cool i think", "If you're reading this, you should catch this icon.", "They not icons, they not icons, they not icons...", "Everybody wanna beat demons, 'til they get chipped by the easy game...", "5 percent will get in comp, but 95 is void...", "YouTube pranked Technical way too hard...", "More icons?", "It's insane how many icons can spawn.", "IconDex has been copied from multiple times.", "That's useless, I got icons to catch, but I can see you don't know 'nun 'bout that.", "Icons, icons, icons...", "Benektelse's mashups go hard. This icon loves them!", "Can't let her grow up in that icon collection.", "I LOVE CATCHING ICONS!", "How many noobies in the house? How many noobies in the house without a Klaux?", "The bigger the collection, the better the specials.", "It's funny how PieceofTrash184 and Lamia might go to war, two elites that wanna build and destroy.", "When Spyro caught the #10000, was you still a fan?", "But while my loved ones was fighting the continuous war back in the city, I was entering a new one. A war that was based on copying and pasting.", "We want icons! Now if I give you icons, you gon' take em?", "Twenty-four seven, three sixty-five, IconDex stays on my mind.", "Have you seen the silly icon?", "If you don't join IconDex, you're a strange little fella","man idk what to put here just catch me","Lieutenant wrote this at 4:14am. CATCH ME!!!", "Everything was t1.5 in the beginning, why do you even care?", "He once told me he wasn't Teamhax, but only Teamhax uses that icon...", "He says he isn't Exen, but I didn't believe him!", "Where's Kvo82?", "It spawned...? Literally icon bias.", "Have you sent it to RobTop yet?", "I've heard that Amoeba had played a prank on 4y4 once.", "DAMBREARON MADE PROMETHEAN!!!", "I would rather win a good giveaway than continue to catch all of these WORTHLESS commons...", "No need to worry about the differences between Zylenox and Zeroxy.", "Did you know this icon has a 0% chance to strike gold?", "I bet this icon is so rare that it compares to NiezziQ.", "I love NiezziQ.", "Promise that you will catch this icon.", "I got- I got- I got- I got- Zylenox, TheRealDarnoc, inside of IconDex.", "Now if I catch this icon... and it just came out recently... and I get comp from that icon... I'm a public enemy.", "I never caught that many icons, never got rich outside of my servers. But I never could type on, it's a mess of buttons under cursors.", "Don't fumble the bag... Lieutenant will never live it down.", "The invite link in IconDex's about command works, after over a year!", "Evil benektelse be like: SpikeDex", "Too many IconDex players tease themselves with a Michigun.", "The Historydex-IconDex beef runs deep.", "Never trust someone with 3 hands!", "She don't believe in IconDex, but she believes in icons to flex.", "You are a very funny community of people.", "IconDex is so gay, and I couldn't be happier.", "I pray my comp get big as the Eiffel Tower, so I can flex on you for 72 hours.", "No one man should have all those icons. The clocks tickin, I just count the bygones.", "My mind is livin on Cloud 9...", "Only real ones know about the Rarity Trials Daniel Dumile.", "Newgen vs Oldgen: A Tale as Old as Time.", "Also try MCDex!", "Are you really silly?", "Go give Layla a Vatican.", "Lamia REALLY doesn't like when IconDex changes.", "bleep blorp icon time", "this is literally icondex if it was real", "i like the icon,,,", "This icon loves lasagna.", "People of IconDex, gather round... an icon has befallen us.", "# join the IconDex server please", "I heard that if you get the name wrong enough times, it'll tell you the name of the icon! I will warn you, though... the wrong name messages are very mean.", "Who knew that the wrong name text could give you the right name?", "You're spamming wrong names, I'm going to assume.", "I feel like IconDex would be more playable if people didn't keep getting outed as pedophiles.", "On average, IconDex sweats are pretty tall. There's one player that lowers the average by multiple inches, though.", "That 16lord catch from Nosyerg was insanely influential... for a few hours.", "I think Deimos gets a kick out of putting Nosyerg down.", "Funnygame thinks this is a funny game.", "Quasar is in the official IconDex server. How the fuck.", "YouknowwhoGD is the goat in my opinion.", "Sorry for taking so long to actually work on IconDex.", "Before you catch this, check your calendar. If it's your mothers birthday today, DO NOT catch this.", "Nine tried to prank Benektelse, but IconDex decided to do the funniest thing of all time.", "Watch the [icondex slander](https://youtube.com/playlist?list=PL9pqWzW3dkruQaLryKeTJSieI_OLIaxc0) series. Also, join the [IconDex](https://discord.com/invite/raw9zRJY2F) discord server.", "If you're American... I feel bad.", "If you're European, you're a part of the majority that plays IconDex.", "https://discord.com/invite/raw9zRJY2F icondex,,.,.,,..,.,....."]

class CountryballNamePrompt(Modal, title=f"Catch this {settings.collectible_name}!"):
    name = TextInput(
        label=f"Name of this {settings.collectible_name}",
        style=discord.TextStyle.short,
        placeholder="Your guess",
    )

    def __init__(self, view: BallSpawnView):
        super().__init__()
        self.view = view

    async def on_error(
        self, interaction: discord.Interaction["BallsDexBot"], error: Exception, /  # noqa: W504
    ) -> None:
        log.exception("An error occured in countryball catching prompt", exc_info=error)
        if interaction.response.is_done():
            await interaction.followup.send(
                f"An error occured with this {settings.collectible_name}.",
            )
        else:
            await interaction.response.send_message(
                f"An error occured with this {settings.collectible_name}.",
            )

    async def on_submit(self, interaction: discord.Interaction["BallsDexBot"]):
        await interaction.response.defer(thinking=True)

        player, _ = await Player.get_or_create(discord_id=interaction.user.id)
        if self.view.caught:
            slowlist = [f"{interaction.user.mention}, you were too silly and slow!", f"{interaction.user.mention}, did you REALLY think you could catch that?", f"{interaction.user.mention}, I admire your confidence for trying.", f"Come on, {interaction.user.mention}! Keep trying! Maybe you'll outspeed Lamia one day.", f"{interaction.user.mention}, please try a little bit harder next time.", f"Hey {interaction.user.mention}, you gotta work on your typing speed.", f"{interaction.user.mention}, remember... THEORETICALLY, you could outspeed anyone... just not today.", f"{interaction.user.mention}, did you really try to get that one? It feels like you're antagonizing me.", f"{interaction.user.mention}, are you slow on purpose?", f"{interaction.user.mention}, I'm not meaning to put you in a bad mood. It's not my fault that you're a slow typer.", f"{interaction.user.mention}, you have no idea how much your slowness hurts me.", f"{interaction.user.mention}, your completion will be looking dry if you keep making attempts like that.", f"{interaction.user.mention} should stick to grinding completion instead of going for rares.", f"Sometimes I think you're not built for competitive play. Maybe you should stick to farming, {interaction.user.mention}."]
            await interaction.followup.send(random.choice(slowlist),
                ephemeral=True,
                allowed_mentions=discord.AllowedMentions(users=player.can_be_mentioned),
            )
            return

        if self.view.is_name_valid(self.name.value):
            ball, has_caught_before = await self.view.catch_ball(
                interaction.user, player=player, guild=interaction.guild
            )

            await interaction.followup.send(
                f"{interaction.user.mention} {self.view.get_message(ball, has_caught_before)}",
                allowed_mentions=discord.AllowedMentions(users=player.can_be_mentioned),
            )
            await interaction.followup.edit_message(self.view.message.id, view=self.view)
        else:
            wrongmsglist = [f"{interaction.user.mention} just said “{self.name}.” Point and laugh.", f"{interaction.user.mention}, that's not how you spell **{self.view.model.country}.**", f"I pray that {interaction.user.mention} doesn't have any hopes of becoming a stenographer...", f"{interaction.user.mention}, slamming your keyboard won't help.", f"What's wrong, {interaction.user.mention}? Don't know this one?", f"{interaction.user.mention}, I can't tell if you need to use comp or you're just REALLY bad at typing.", f"Was that a typo, {interaction.user.mention}?", f"{interaction.user.mention}, how do you NOT know what this icon's name is?", f"Fine, {interaction.user.mention}, it's **{self.view.model.country}.** Please stop wasting my time.", f"{interaction.user.mention}... how did you manage to type THAT poorly?", f"{interaction.user.mention}. Please. Type properly. For the love of god.", f"{interaction.user.mention}, I request of you to write this icon's name correctly next time. Don't disappoint me.", "I'm gonna save whoever just said that the embarrassment of being associated with that guess. You're welcome.", f"The genius known as {interaction.user.mention} thought it was someone DIFFERENT than **{self.view.model.country}.**", f"{interaction.user.mention} ligma ball"]
            # sorry bro
            sadnesslist = ["robtop", "anaban", "michigun", "riot", "pasiblitz", "sandstorm", "nswish", "lunarsimg", "brandonlarkin", "zobros", "krmal", "niezziq", "souls", "hiroquet", "hilo"]
            sadwrongmsglist = [f"{interaction.user.mention}, I wish it was them too, dude.", f"{interaction.user.mention}, sorry to break the news to you. You aren't getting that rich today."]
            # poop humor
            pooplist = ["poop", "shit", "fart", "scat", "feces", "fecal", "dung"]
            poopwrongmsglist = ["farty poop fart poopie farty", "HAHAHAHA POOP", "benektelse has irritable bowel syndrome", "POOPIGN!!!"]
            if f"{self.name}".lower() in sadnesslist:
                await interaction.followup.send(random.choice(sadwrongmsglist),
                    allowed_mentions=discord.AllowedMentions(users=player.can_be_mentioned),
                    ephemeral=False,
                )
            elif f"{self.name}".lower() in pooplist:
                await interaction.followup.send(random.choice(poopwrongmsglist),
                    allowed_mentions=discord.AllowedMentions(users=player.can_be_mentioned),
                    ephemeral=False,
                )
            else:
                await interaction.followup.send(random.choice(wrongmsglist),
                    allowed_mentions=discord.AllowedMentions(users=player.can_be_mentioned),
                    ephemeral=False,
                )


class BallSpawnView(View):
    """
    BallSpawnView is a Discord UI view that represents the spawning and interaction logic for a
    countryball in the BallsDex bot. It handles user interactions, spawning mechanics, and
    countryball catching logic.

    Attributes
    ----------
    bot: BallsDexBot
    model: Ball
        The ball being spawned.
    algo: str | None
        The algorithm used for spawning, used for metrics.
    message: discord.Message
        The Discord message associated with this view once created with `spawn`.
    caught: bool
        Whether the countryball has been caught yet.
    ballinstance: BallInstance | None
        If this is set, this ball instance will be spawned instead of creating a new ball instance.
        All properties are preserved, and if successfully caught, the owner is transferred (with
        a trade entry created). Use the `from_existing` constructor to use this.
    special: Special | None
        Force the spawned countryball to have a special event attached. If None, a random one will
        be picked.
    atk_bonus: int | None
        Force a specific attack bonus if set, otherwise random range defined in config.yml.
    hp_bonus: int | None
        Force a specific health bonus if set, otherwise random range defined in config.yml.
    """

    def __init__(self, bot: "BallsDexBot", model: Ball):
        super().__init__()
        self.bot = bot
        self.model = model
        self.algo: str | None = None
        self.message: discord.Message = discord.utils.MISSING
        self.caught = False
        self.ballinstance: BallInstance | None = None
        self.special: Special | None = None
        self.atk_bonus: int | None = None
        self.hp_bonus: int | None = None

    async def interaction_check(self, interaction: discord.Interaction["BallsDexBot"], /) -> bool:
        return await interaction.client.blacklist_check(interaction)

    async def on_timeout(self):
        self.catch_button.disabled = True
        if self.message:
            try:
                await self.message.edit(view=self)
            except discord.HTTPException:
                pass
        if self.ballinstance and not self.caught:
            await self.ballinstance.unlock()

    @button(style=discord.ButtonStyle.primary, label="Catch me!")
    async def catch_button(self, interaction: discord.Interaction["BallsDexBot"], button: Button):
        if self.caught:
            await interaction.response.send_message("I was caught already!", ephemeral=True)
        else:
            await interaction.response.send_modal(CountryballNamePrompt(self))

    @classmethod
    async def from_existing(cls, bot: "BallsDexBot", ball_instance: BallInstance):
        """
        Get an instance from an existing `BallInstance`. Instead of creating a new ball instance,
        this will transfer ownership of the existing instance when caught.

        The ball instance must be unlocked from trades, and will be locked until caught or timed
        out.
        """
        if await ball_instance.is_locked():
            raise RuntimeError("This countryball is locked for a trade")

        # prevent countryball from being traded while spawned
        await ball_instance.lock_for_trade()

        view = cls(bot, ball_instance.ball)
        view.ballinstance = ball_instance
        return view

    @classmethod
    async def get_random(cls, bot: "BallsDexBot"):
        """
        Get a new instance with a random countryball. Rarity values are taken into account.
        """
        countryballs = list(filter(lambda m: m.enabled, balls.values()))
        if not countryballs:
            raise RuntimeError("No ball to spawn!")
        rarities = [x.rarity for x in countryballs]
        cb = random.choices(population=countryballs, weights=rarities, k=1)[0]
        return cls(bot, cb)

    @property
    def name(self):
        return self.model.country

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
        file_location = "./admin_panel/media/" + self.model.wild_card
        file_name = f"nt_{generate_random_name()}.{extension}"
        try:
            permissions = channel.permissions_for(channel.guild.me)
            if permissions.attach_files and permissions.send_messages:
                self.message = await channel.send(random.choice(spwnmsglist),
                    view=self,
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

    def is_name_valid(self, text: str) -> bool:
        """
        Check if the prompted name is valid.

        Parameters
        ----------
        text: str
            The text entered by the user. It will be lowered and stripped of enclosing blank
            characters.

        Returns
        -------
        bool
            Whether the name matches or not.
        """
        if self.model.catch_names:
            possible_names = (self.name.lower(), *self.model.catch_names.split(";"))
        else:
            possible_names = (self.name.lower(),)
        if self.model.translations:
            possible_names += tuple(x.lower() for x in self.model.translations.split(";"))
        cname = text.lower().strip()
        # Remove fancy unicode characters like ’ to replace to '
        cname = cname.replace("\u2019", "'")
        cname = cname.replace("\u2018", "'")
        cname = cname.replace("\u201c", '"')
        cname = cname.replace("\u201d", '"')
        return cname in possible_names

    async def catch_ball(
        self,
        user: discord.User | discord.Member,
        *,
        player: Player | None,
        guild: discord.Guild | None,
    ) -> tuple[BallInstance, bool]:
        """
        Mark this countryball as caught and assign a new `BallInstance` (or transfer ownership if
        attribute `ballinstance` was set).

        Parameters
        ----------
        user: discord.User | discord.Member
            The user that will obtain the new countryball.
        player: Player
            If already fetched, add the player model here to avoid an additional query.
        guild: discord.Guild | None
            If caught in a guild, specify here for additional logs. Will be extracted from `user`
            if it's a member object.

        Returns
        -------
        tuple[bool, BallInstance]
            A tuple whose first value indicates if this is the first time this player catches this
            countryball. Second value is the newly created countryball.

            If `ballinstance` was set, this value is returned instead.

        Raises
        ------
        RuntimeError
            The `caught` attribute is already set to `True`. You should always check before calling
            this function that the ball was not caught.
        """
        if self.caught:
            raise RuntimeError("This ball was already caught!")
        self.caught = True
        self.catch_button.disabled = True
        player = player or (await Player.get_or_create(discord_id=user.id))[0]
        is_new = not await BallInstance.filter(player=player, ball=self.model).exists()

        if self.ballinstance:
            # if specified, do not create a countryball but switch owner
            # it's important to register this as a trade to avoid bypass
            trade = await Trade.create(player1=self.ballinstance.player, player2=player)
            await TradeObject.create(
                trade=trade, player=self.ballinstance.player, ballinstance=self.ballinstance
            )
            self.ballinstance.trade_player = self.ballinstance.player
            self.ballinstance.player = player
            self.ballinstance.locked = None  # type: ignore
            await self.ballinstance.save(update_fields=("player", "trade_player", "locked"))
            return self.ballinstance, is_new

        # stat may vary by +/- 20% of base stat
        bonus_attack = (
            self.atk_bonus
            if self.atk_bonus is not None
            else random.randint(-settings.max_attack_bonus, settings.max_attack_bonus)
        )
        bonus_health = (
            self.hp_bonus
            if self.hp_bonus is not None
            else random.randint(-settings.max_health_bonus, settings.max_health_bonus)
        )

        # check if we can spawn cards with a special background
        special = self.special
        population = [
            x
            for x in specials.values()
            # handle null start/end dates with infinity times
            if (x.start_date or datetime.min.replace(tzinfo=get_default_timezone()))
            <= tortoise_now()
            <= (x.end_date or datetime.max.replace(tzinfo=get_default_timezone()))
        ]
        if not special and population:
            # Here we try to determine what should be the chance of having a common card
            # since the rarity field is a value between 0 and 1, 1 being no common
            # and 0 only common, we get the remaining value by doing (1-rarity)
            # We then sum each value for each current event, and we should get an algorithm
            # that kinda makes sense.
            common_weight = sum(1 - x.rarity for x in population)

            weights = [x.rarity for x in population] + [common_weight]
            # None is added representing the common countryball
            special = random.choices(population=population + [None], weights=weights, k=1)[0]

        ball = await BallInstance.create(
            ball=self.model,
            player=player,
            special=special,
            attack_bonus=bonus_attack,
            health_bonus=bonus_health,
            server_id=guild.id if guild else None,
            spawned_time=self.message.created_at,
        )

        # logging and stats
        log.log(
            logging.INFO if user.id in self.bot.catch_log else logging.DEBUG,
            f"{user} caught {settings.collectible_name} {self.model}, {special=}",
        )
        if isinstance(user, discord.Member) and user.guild.member_count:
            caught_balls.labels(
                country=self.name,
                special=special,
                # observe the size of the server, rounded to the nearest power of 10
                guild_size=10 ** math.ceil(math.log(max(user.guild.member_count - 1, 1), 10)),
                spawn_algo=self.algo,
            ).inc()

        return ball, is_new

    def get_message(self, ball: BallInstance, new_ball: bool) -> str:
        """
        Generate a user-facing message after a ball has been caught.

        Parameters
        ----------
        ball: BallInstance
            The newly created ball instance
        new_ball: bool
            Boolean indicating if this is a new countryball in completion
            (as returned by `catch_ball`)
        """
        fakeoutlist = ["Henral", "Hotball1", "Trick", "Biprex", "KPGDylan", "Seels", "adafcaefc", "Zylenox", "Zoink", "Doggie", "heda", "Paqoe", "zNymo98", "SerVax", "Thycket", "Slithium", "Nocturina", "Wolvez", "Benektelse", "Zeroxy", "rWooshi", "StormBlazer", "nsla", "MrSpaghetti", "Thnnder", "Tigger4046", "BigMukMuk", "Swiborg", "SpaceUK", "saRy", "Hyperbola", "SpirteX", "WarGack", "sinc0s", "Phynn24", "mosk14142", "iIiViRuZiIi", "AleXPain24", "Qwer", "Absolute", "bop", "Vertic", "Quasar", "Cvolton", "3xotic", "Surv", "hmann", "DarkX", "KrmaL", "LunarSIMG", "BrandonLarkin", "Zobros", "nSwish", "Sandstorm", "Riot", "Pasiblitz", "Michigun", "Robtop", "Anaban",  "NiezziQ", "Hilo", "Souls", "DiscJoker", "Pacosky18", "llqne"]
        actionlist = ["spying on " f"**{random.choice(fakeoutlist)}**", "cooking dinner", "working out", "doing yoga", "working overtime", "playing IconDex", "sleeping", "in class", "making a video", "jumping over spikes", "playing a level", "arguing with " f"**{random.choice(fakeoutlist)}**", "having a pillow fight with " f"**{random.choice(fakeoutlist)}**", "running errands with " f"**{random.choice(fakeoutlist)}**", "hanging out with " f"**{random.choice(fakeoutlist)}**", "making a level", "grinding stars", "grinding moons", "grinding demons", "being tutored by " f"**{random.choice(fakeoutlist)}**", "partying with " f"**{random.choice(fakeoutlist)}**", "listening to music", "relaxing", "competing against " f"**{random.choice(fakeoutlist)}**", "on a picnic with " f"**{random.choice(fakeoutlist)}**", "on the beach with " f"**{random.choice(fakeoutlist)}**"]
        catchmsglist = ["just caught **{icon}** off guard while they were {iconaction}." f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "just caught **{icon}** off guard while they were {iconaction}." f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "just caught **{icon}** off guard while they were {iconaction}." f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "just caught **{icon}** off guard while they were {iconaction}." f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "just caught **{icon}** off guard while they were {iconaction}." f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "received **{icon}** " f"`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)` " "as a reward for winning a competition against " f"**{random.choice(fakeoutlist)}**!" "\n\n {icondexspecial}", "started a cult revolving around **{icon}...** " f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "Now in your posession... with an attack multiplier of " f"`{ball.attack_bonus:+}%` " "and a health multiplier of " f"`{ball.health_bonus:+}%`, " "everyone please welcome the great **{icon}** to their collection!!!" f"\n`(#{ball.pk:0X})`" "\n\n {icondexspecial}", "Have you considered that this **{icon}** you just caught might be silly? " f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "didn't ACTUALLY catch **{icon}.** I'm only sending this so that they don't feel bad. \n" f"`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "Nice work! You just caught **{icon}!** \n" f"`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "hey dude look you LITERALLY just got **{icon}!!!**" f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "Make sure to hide your **{icon}** before JuMa can steal it!" f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "Nice work! You just caught " f"**{random.choice(fakeoutlist)}!** " "\n ...just kidding, you actually caught **{icon}.**" f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", " has successfully caught **{icon}**!!" f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "This **{icon}** is pretty awesome. " f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "That **{icon}** looks really good in your collection! You should start collecting them!" f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "That **{icon}** doesn't have a permit to be silly, just so you know." f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "You should give me that **{icon}.** I need it more than you do." f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}"]
        text = ""
        if ball.specialcard and ball.specialcard.catch_phrase:
            text += f"*{ball.specialcard.catch_phrase}*\n"
        if new_ball:
            text += (
                f"Woah... is that a **new {settings.collectible_name}** "
                "you've just caught?!"
            )
        return (random.choice(catchmsglist).format(icon = self.name, icondexspecial = text, iconaction = random.choice(actionlist)))

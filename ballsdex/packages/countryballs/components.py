from __future__ import annotations

import logging
import math
import random
from datetime import datetime
from typing import TYPE_CHECKING, cast

import discord
from discord.ui import Button, Modal, TextInput, View, button
from tortoise.timezone import get_default_timezone
from tortoise.timezone import now as datetime_now

from ballsdex.core.metrics import caught_balls
from ballsdex.core.models import BallInstance, Player, specials
from ballsdex.settings import settings

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot
    from ballsdex.packages.countryballs.countryball import CountryBall

log = logging.getLogger("ballsdex.packages.countryballs.components")


class CountryballNamePrompt(Modal, title=f"Catch this {settings.collectible_name}!"):
    name = TextInput(
        label=f"Name of this {settings.collectible_name}",
        style=discord.TextStyle.short,
        placeholder="Your guess",
    )

    def __init__(self, ball: "CountryBall", button: Button):
        super().__init__()
        self.ball = ball
        self.button = button

    async def on_error(self, interaction: discord.Interaction, error: Exception, /) -> None:
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
        # TODO: use lock
        await interaction.response.defer(thinking=True)

        player, _ = await Player.get_or_create(discord_id=interaction.user.id)
        if self.ball.caught:
            slowlist = [f"{interaction.user.mention}, you were too silly and slow!", f"{interaction.user.mention}, did you REALLY think you could catch that?", f"{interaction.user.mention}, I admire your confidence for trying.", f"Come on, {interaction.user.mention}! Keep trying! Maybe you'll outspeed Lamia one day.", f"{interaction.user.mention}, please try a little bit harder next time.", f"Hey {interaction.user.mention}, you gotta work on your typing speed.", f"{interaction.user.mention}, remember... THEORETICALLY, you could outspeed anyone... just not today.", f"{interaction.user.mention}, did you really try to get that one? It feels like you're antagonizing me.", f"{interaction.user.mention}, are you slow on purpose?", f"{interaction.user.mention}, I'm not meaning to put you in a bad mood. It's not my fault that you're a slow typer.", f"{interaction.user.mention}, you have no idea how much your slowness hurts me.", f"{interaction.user.mention}, your completion will be looking dry if you keep making attempts like that.", f"{interaction.user.mention} should stick to grinding completion instead of going for rares.", f"Sometimes I think you're not built for competitive play. Maybe you should stick to farming, {interaction.user.mention}."]
            await interaction.followup.send((random.choice(slowlist)),
                ephemeral=True,
                allowed_mentions=discord.AllowedMentions(users=player.can_be_mentioned),
            )
            return

        if self.ball.model.catch_names:
            possible_names = (self.ball.name.lower(), *self.ball.model.catch_names.split(";"))
        else:
            possible_names = (self.ball.name.lower(),)
        if self.ball.model.translations:
            possible_names += tuple(x.lower() for x in self.ball.model.translations.split(";"))

        if self.name.value.lower().strip() in possible_names:
            self.ball.caught = True
            ball, has_caught_before = await self.catch_ball(
                interaction.client, cast(discord.Member, interaction.user)
            )

            special = ""
            if ball.specialcard and ball.specialcard.catch_phrase:
                special += f"*{ball.specialcard.catch_phrase}*\n"
            if has_caught_before:
                special += (
                    f"Woah... that's a **new {settings.collectible_name}** "
                    "added to your collection!"
                )
            fakeoutlist = ["Henral", "Hotball1", "Trick", "Biprex", "KPGDylan", "Seels", "adafcaefc", "Zylenox", "Zoink", "Doggie", "heda", "Paqoe", "zNymo98", "SerVax", "Thycket", "Slithium", "Nocturina", "Wolvez", "Benektelse", "Zeroxy", "rWooshi", "StormBlazer", "nsla", "MrSpaghetti", "Thnnder", "Tigger4046", "BigMukMuk", "Swiborg", "SpaceUK", "saRy", "Hyperbola", "SpirteX", "WarGack", "sinc0s", "Phynn24", "mosk14142", "iIiViRuZiIi", "AleXPain24", "Qwer", "Absolute", "bop", "Vertic", "Quasar", "Cvolton", "3xotic", "Surv", "hmann", "DarkX", "KrmaL", "LunarSIMG", "BrandonLarkin", "Zobros", "nSwish", "Sandstorm", "Riot", "Pasiblitz", "Michigun", "Robtop", "Anaban",  "NiezziQ", "Hilo", "Souls", "DiscJoker", "Pacosky18", "llqne"]
            actionlist = ["spying on " f"**{random.choice(fakeoutlist)}**", "cooking dinner", "working out", "doing yoga", "working overtime", "playing IconDex", "sleeping", "in class", "making a video", "jumping over spikes", "playing a level", "arguing with " f"**{random.choice(fakeoutlist)}**", "having a pillow fight with " f"**{random.choice(fakeoutlist)}**", "running errands with " f"**{random.choice(fakeoutlist)}**", "hanging out with " f"**{random.choice(fakeoutlist)}**", "making a level", "grinding stars", "grinding moons", "grinding demons", "being tutored by " f"**{random.choice(fakeoutlist)}**", "partying with " f"**{random.choice(fakeoutlist)}**", "listening to music", "relaxing", "competing against " f"**{random.choice(fakeoutlist)}**", "on a picnic with " f"**{random.choice(fakeoutlist)}**", "on the beach with " f"**{random.choice(fakeoutlist)}**"]
            catchmsglist = ["{ping} just caught **{icon}** off guard while they were {iconaction}." f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "{ping} just caught **{icon}** off guard while they were {iconaction}." f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "{ping} just caught **{icon}** off guard while they were {iconaction}." f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "{ping} just caught **{icon}** off guard while they were {iconaction}." f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "{ping} just caught **{icon}** off guard while they were {iconaction}." f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "{ping} received **{icon}** " f"`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)` " "as a reward for winning a competition against " f"**{random.choice(fakeoutlist)}**!" "\n\n {icondexspecial}", "{ping} started a cult revolving around **{icon}...** " f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "And now, in the possession of {ping}... with an attack multiplier of " f"`{ball.attack_bonus:+}%` " "and a health multiplier of " f"`{ball.health_bonus:+}%`, " "everyone please welcome **{icon}** to their collection!" f"\n`(#{ball.pk:0X})`" "\n\n {icondexspecial}", "{ping}, have you considered that this **{icon}** you just caught might be silly? " f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "{ping} didn't ACTUALLY catch **{icon}.** I'm only sending this so that they don't feel bad. \n" f"`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "Nice, {ping}! You just caught **{icon}!** \n" f"`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "{ping} {ping} {ping} hey {ping} dude look {ping} {ping} you got **{icon}!!!**" f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "Hey {ping}, make sure to hide your **{icon}** before Lamia can steal it!" f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "Nice, {ping}! You just caught " f"**{random.choice(fakeoutlist)}!** " "\n ...just kidding, you actually caught **{icon}.**" f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "**{icon}** has happily joined {ping}'s collection!" f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "Hey, {ping}! This **{icon}** is pretty awesome. " f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "Hey, {ping}! That **{icon}** looks really good in your collection! You should start collecting them!" f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "Hey, {ping}. That **{icon}** doesn't have a permit to be silly, just so you know." f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}", "{ping}, you should give me that **{icon}.** I need it more than you do." f"\n`(#{ball.pk:0X}, " f"{ball.attack_bonus:+}%/" f"{ball.health_bonus:+}%)`" "\n\n {icondexspecial}"]
            await interaction.followup.send(random.choice(catchmsglist).format(ping = interaction.user.mention, icon = self.ball.name, icondexspecial = special, iconaction = random.choice(actionlist)),
                allowed_mentions=discord.AllowedMentions(users=player.can_be_mentioned),
            )
            self.button.disabled = True
            await interaction.followup.edit_message(self.ball.message.id, view=self.button.view)
        else:
            wrongmsglist = [f"{interaction.user.mention} just said “{self.name}.” Point and laugh.", f"{interaction.user.mention}, that's not how you spell **{self.ball.name}.**", f"I pray that {interaction.user.mention} doesn't have any hopes of becoming a stenographer...", f"{interaction.user.mention}, slamming your keyboard won't help.", f"What's wrong, {interaction.user.mention}? Don't know this one?", f"{interaction.user.mention}, I can't tell if you need to use comp or you're just REALLY bad at typing.", f"Was that a typo, {interaction.user.mention}?", f"{interaction.user.mention}, how do you NOT know what this icon's name is?", f"Fine, {interaction.user.mention}, it's **{self.ball.name}.** Please stop wasting my time.", f"{interaction.user.mention}... how did you manage to type THAT poorly?", f"{interaction.user.mention}. Please. Type properly. For the love of god.", f"{interaction.user.mention}, I request of you to write this icon's name correctly next time. Don't dissapoint me.", "I'm gonna save whoever just said that the embarrassment of being associated with that guess. You're welcome.", f"The genius known as {interaction.user.mention} thought it was someone DIFFERENT than **{self.ball.name}.**", f"{interaction.user.mention} ligma ball"]
            # sorry bro
            sadnesslist = ["robtop", "anaban", "michigun", "riot", "pasiblitz", "sandstorm", "nswish", "lunarsimg", "brandonlarkin", "zobros", "krmal"]
            sadwrongmsglist = [f"{interaction.user.mention}, I wish it was them too, dude.", f"{interaction.user.mention}, sorry to break the news to you. You aren't getting that rich today."]
            # poop humor
            pooplist = ["poop", "shit", "fart", "scat", "feces", "fecal", "dung"]
            poopwrongmsglist = ["farty poop fart poopie farty", "HAHAHAHA POOP", "benektelse has irritable bowel syndrome", "POOPIGN!!!"]
            if f"{self.name}".lower() in sadnesslist:
                await interaction.followup.send(random.choice(sadwrongmsglist),
                    allowed_mentions=discord.AllowedMentions(users=player.can_be_mentioned),
                    ephemeral=config.silent,
                )
            elif f"{self.name}".lower() in pooplist:
                await interaction.followup.send(random.choice(poopwrongmsglist),
                    allowed_mentions=discord.AllowedMentions(users=player.can_be_mentioned),
                    ephemeral=config.silent,
                )
            else:
                await interaction.followup.send(random.choice(wrongmsglist),
                    allowed_mentions=discord.AllowedMentions(users=player.can_be_mentioned),
                    ephemeral=config.silent,
                )

    async def catch_ball(
        self, bot: "BallsDexBot", user: discord.Member
    ) -> tuple[BallInstance, bool]:
        player, created = await Player.get_or_create(discord_id=user.id)

        # stat may vary by +/- 20% of base stat
        bonus_attack = self.ball.atk_bonus or random.randint(
            -settings.max_attack_bonus, settings.max_attack_bonus
        )
        bonus_health = self.ball.hp_bonus or random.randint(
            -settings.max_health_bonus, settings.max_health_bonus
        )

        # check if we can spawn cards with a special background
        special = self.ball.special
        population = [
            x
            for x in specials.values()
            # handle null start/end dates with infinity times
            if (x.start_date or datetime.min.replace(tzinfo=get_default_timezone()))
            <= datetime_now()
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

        is_new = not await BallInstance.filter(player=player, ball=self.ball.model).exists()
        ball = await BallInstance.create(
            ball=self.ball.model,
            player=player,
            special=special,
            attack_bonus=bonus_attack,
            health_bonus=bonus_health,
            server_id=user.guild.id,
            spawned_time=self.ball.time,
        )
        if user.id in bot.catch_log:
            log.info(
                f"{user} caught {settings.collectible_name}" f" {self.ball.model}, {special=}",
            )
        else:
            log.debug(
                f"{user} caught {settings.collectible_name}" f" {self.ball.model}, {special=}",
            )
        if user.guild.member_count:
            caught_balls.labels(
                country=self.ball.model.country,
                special=special,
                # observe the size of the server, rounded to the nearest power of 10
                guild_size=10 ** math.ceil(math.log(max(user.guild.member_count - 1, 1), 10)),
                spawn_algo=self.ball.algo,
            ).inc()
        return ball, is_new


class CatchView(View):
    def __init__(self, ball: "CountryBall"):
        super().__init__()
        self.ball = ball

    async def interaction_check(self, interaction: discord.Interaction["BallsDexBot"], /) -> bool:
        return await interaction.client.blacklist_check(interaction)

    async def on_timeout(self):
        self.catch_button.disabled = True
        if self.ball.message:
            try:
                await self.ball.message.edit(view=self)
            except discord.HTTPException:
                pass
    
    btnlst = ["Catch?", "Catch!", "Catch...", "Catch, you silly!", "Catch this icon?", "Will you catch this?", "Catching this icon...", "Catch it before it despawns!!!", "Please catch this...", "What if... you caught this?", "Acquire... the icon.", "This is a button!", "This is an icon!", "Are you cool? Catch this!", "I wonder how many icons you've caught...", "The catcher.", "You're silly.", "✅", "🔥", "Seize the icon...", "You gon' take it?", "Hauling in this icon...", "Someone's gonna snipe this.", "Don't copy and paste on me!", "ARREST THIS ICON!", "CEASE THE SEIZE!", "Apprehend him!", "This icon deserves to be caught.", "This is my favorite icon.", "For real!", "Are you a cop?", "I accept all Terms & Conditions."]
    @button(style=discord.ButtonStyle.primary, label=(random.choice(btnlst)))
    async def catch_button(self, interaction: discord.Interaction["BallsDexBot"], button: Button):
        if self.ball.caught:
            await interaction.response.send_message("Too slow, silly!", ephemeral=True)
        else:
            await interaction.response.send_modal(CountryballNamePrompt(self.ball, button))

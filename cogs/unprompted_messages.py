from random import choice, randint
from re import sub

from discord.ext import commands

from other_utils import funcs

ALLOWED_BOTS = [
    479937255868465156,
    492970622587109380,
    597028739616079893,
    771696725173469204,
    771403225840222238
]


class UnpromptedMessages(commands.Cog, name="Unprompted Messages"):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild and message.guild.id in funcs.readJson("data/unprompted_messages.json")["servers"] \
                and funcs.userNotBlacklisted(self.client, message) \
                and (not message.author.bot or message.author.id in ALLOWED_BOTS):
            originalmsg = message.content
            lowercase = originalmsg.casefold()
            if self.client.user in message.mentions and not (await self.client.get_context(message)).valid:
                await message.channel.trigger_typing()
                msg = sub("<@!?" + str(self.client.user.id) + ">", "", message.content).strip()
                params = {
                    "botid": "b8d616e35e36e881",
                    "custid": message.author.id,
                    "input": msg or "Hi",
                    "format": "json"
                }
                res = await funcs.getRequest("https://www.pandorabots.com/pandora/talk-xml", params=params)
                data = res.json()
                text = choice(["I do not understand.", "Please say that again.", "What was that?", "Ok."]) \
                    if data["status"] == 4 else data["that"].replace("A.L.I.C.E", self.client.user.name).replace(
                    "ALICE", self.client.user.name).replace("<br>", "").replace("&quot;", '"').replace("&lt;",
                    "<").replace("&gt;", ">").replace("&amp;", "&")
                await message.channel.send(f"{message.author.mention} {text}")
            elif lowercase.startswith(("im ", "i'm ", "i‘m ", "i’m ", "i am ")):
                if lowercase.startswith("im "):
                    im = originalmsg[3:]
                elif lowercase.startswith(("i'm ", "i’m ", "i‘m ")):
                    im = originalmsg[4:]
                else:
                    im = originalmsg[5:]
                if im.casefold() == self.client.user.name:
                    await message.channel.send(f"No you're not, you're {message.author.name}.")
                else:
                    await message.channel.send(f"Hi {im}, I'm {self.client.user.name}!")
            elif "netvigator" in lowercase:
                await message.channel.send("notvogotor")
            elif lowercase == "h":
                if not randint(0, 9):
                    await funcs.sendImage(
                        message.channel, "https://cdn.discordapp.com/attachments/665656727332585482/667138135091838977/4a1862c.gif",
                        name="h.gif"
                    )
                else:
                    await message.channel.send("h")
            elif lowercase == "f":
                if not randint(0, 9):
                    await funcs.sendImage(
                        message.channel, "https://cdn.discordapp.com/attachments/663264341126152223/842785581602701312/assets_f.jpg"
                    )
                else:
                    await message.channel.send("f")
            elif "gordon ramsay" in lowercase:
                await message.channel.send("https://i.imgur.com/XezjUCZ.gifv")
            elif "hkeaa" in lowercase:
                await funcs.sendImage(
                    message.channel, "https://cdn.discordapp.com/attachments/659771291858894849/663420485438275594/HKEAA_DENIED.png"
                )
            elif lowercase.startswith("hmmm"):
                if all(m in "m" for m in lowercase.split("hmm", 1)[1].replace(" ", "")):
                    await funcs.sendImage(
                        message.channel, choice(
                            [
                                "https://media.giphy.com/media/8lQyyys3SGBoUUxrUp/giphy.gif",
                                "https://i.redd.it/qz6eknd73qvy.gif",
                                "https://i.imgur.com/zXAA3CV.gif",
                                "https://i.imgur.com/ZU014ft.gif",
                                "https://i.imgur.com/o7EsvoS.gif",
                                "https://i.imgur.com/8DxmZY6.gif"
                            ]
                        ), name="hmmm.gif"
                    )

    @commands.command(name="umenable", description="Enables unprompted messages for your server.",
                      aliases=["ume", "eum", "enableum"])
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def umenable(self, ctx):
        data = funcs.readJson("data/unprompted_messages.json")
        serverList = list(data["servers"])
        if ctx.guild.id not in serverList:
            serverList.append(ctx.guild.id)
            data["servers"] = serverList
            funcs.dumpJson("data/unprompted_messages.json", data)
            return await ctx.send("`Enabled unprompted messages for this server.`")
        await ctx.send(embed=funcs.errorEmbed(None, "Unprompted messages are already enabled."))

    @commands.command(name="umdisable", description="Disables unprompted messages for your server.",
                      aliases=["umd", "dum", "disableum"])
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def umdisable(self, ctx):
        data = funcs.readJson("data/unprompted_messages.json")
        serverList = list(data["servers"])
        if ctx.guild.id in serverList:
            serverList.remove(ctx.guild.id)
            data["servers"] = serverList
            funcs.dumpJson("data/unprompted_messages.json", data)
            return await ctx.send("`Disabled unprompted messages for this server.`")
        await ctx.send(embed=funcs.errorEmbed(None, "Unprompted messages are not enabled."))


def setup(client: commands.Bot):
    client.add_cog(UnpromptedMessages(client))

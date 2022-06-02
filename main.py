from discord.ext import commands
from discord.utils import get
import discord
import os
import imgonnafigureouttextblob

import imgonnafigureouttextblob
import kovifyKayar
import textManager as tm
import traceback
import letsUseClasses
flag = True



my_secret = os.environ['TOKEN']
bot = commands.Bot(os.environ['PREFIX'])
talkOrListen = {}
autogenInt = 1
autogenCounter = 1
big_bot = kovifyKayar.kovify_kr(4,"brain/")




@bot.command()
async def save(ctx):
    pass


@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot) + "\nPlease use $init with any applicable corpi separated with a space or leave blank for defaults\nRegardless, `init or I won't work")


@bot.command()
async def autogen(ctx, autogenAmount):
    print("autogen was used on {} {}".format(ctx.guild, ctx.channel))
    global autogen
    global autogenCounter
    global autogenInt
    autogenInt = autogenAmount
    autogenCounter = 1
    await ctx.channel.send("I will now message every {} messages. AutoGeneration Counter is {}".format(autogenAmount,autogenCounter))


@bot.command()
async def loadUsers(ctx):
    print("loadUsers was used on {} {}".format(ctx.guild, ctx.channel))
    newCorpusLoader = "activeUse/tempThinking"
    newFile = open(newCorpusLoader, "w", encoding="utf-8")
    for file in os.listdir("people/"):
        newFile.write("people/" + file + "\n")
    newFile.close()
    await init(ctx, newCorpusLoader)

@bot.command()
async def loadChannels(ctx):
    print("loadUsers was used on {} {}".format(ctx.guild, ctx.channel))
    newCorpusLoader = "activeUse/tempThinking"
    newFile = open(newCorpusLoader, "w", encoding="utf-8")
    for file in os.listdir("channels/"):
        newFile.write("channels/" + file + "\n")
    newFile.close()
    await init(ctx, newCorpusLoader)

@bot.command()
async def loadServers(ctx):
    print("loadUsers was used on {} {}".format(ctx.guild, ctx.channel))
    newCorpusLoader = "activeUse/tempThinking"
    newFile = open(newCorpusLoader, "w", encoding="utf-8")
    for file in os.listdir("server/"):
        newFile.write("server/" + file + "\n")
    newFile.close()
    await init(ctx, newCorpusLoader)

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.content.startswith("Created a channel named"):
        myName = reaction.message.content[24:reaction.message.content.find(".")]
        role = get(user.guild.roles, name=myName)
        await user.add_roles(role)



@bot.command()
async def newChann(ctx, *, name=None):
    print("NewChann was used on {} {}".format(ctx.guild, ctx.channel))
    guild = ctx.message.guild
    nameIsNoneFlag = True #changes to false if correct
    if name == None:
        await ctx.send('Sorry, but you have to insert a name. Try again, but do it like this: `create [channel name]')
        nameIsNoneFlag = False
    if nameIsNoneFlag:
        allChannels = {}
        for chann in guild.text_channels:
            allChannels[chann] = []
        if name in allChannels:
            await ctx.send('Sorry, but this channel already exists. Try again, but do it with a different name: `create [channel name]')
            return
        else:
            newName = ""
            for item in name.split(" "):
                if len(name.split(" ")) == name.split(" ").index(item) + 1:
                    newName += item
                else:
                    newName += item + "-"
            await guild.create_role(name=newName)
            member = ctx.message.author
            role = get(member.guild.roles, name=newName)
            await role.edit(position=1)
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True),
                role: discord.PermissionOverwrite(read_messages=True)
            }
            await member.add_roles(role)
            channel = await guild.create_text_channel(newName, overwrites=overwrites)
            await ctx.send(f"Created a channel named {channel.name}. Message 'talk to begin there!")
            return





@bot.command()
async def talkAll(ctx):
    print("TalkAll was used on {} {}".format(ctx.guild, ctx.channel))
    guild = ctx.channel.guild
    for chann in guild.text_channels:
        try:
            if chann not in talkOrListen:
                talkOrListen[chann] = True
                await chann.send("I am SUPER CHATTY BABY BOT GAULLE MWAHAHA (Active in all channels on this server)")
            else:
                talkOrListen[chann] = True
                await chann.send("Someone told me to talk.. idk I'm just following directions")
        except:
            pass


@bot.command()
async def talk(ctx, channelName=None):
    print("Talk was used on {} {}".format(ctx.guild, ctx.channel))
    if channelName is not None:
        guild = ctx.channel.guild
        channelIsSet = ctx.channel
        allChannels = {}
        for channel in guild.channels:
            if channel.name == channelName:
                channelIsSet = channel
        if channelName not in str(guild.channels):
            await ctx.channel.send("I can't send it there it doesn't exist")
        else:
            if talkOrListen.keys().__contains__(channelName):
                talkOrListen[channelName] = False
                await ctx.channel.send("Nah goodnight.")
            else:
                talkOrListen[channelName] = True
                await channelIsSet.send("I'm up I'm up")
                await ctx.channel.send("I'm up here too dw")
    else:
        if ctx.channel not in talkOrListen:
            talkOrListen[ctx.channel] = True
            await ctx.channel.send("I am feeling chatty")
        else:
            if talkOrListen[ctx.channel]:
                talkOrListen[ctx.channel] = False
                await ctx.channel.send("I am listening here")
            else:
                talkOrListen[ctx.channel] = True
                await ctx.channel.send("I'm gonna talk mmkay?")
        return



@bot.command()
async def init(ctx, *corpi):
    print("Init was used on {} {}".format(ctx.guild, ctx.channel))
    if len(corpi) == 0:
        big_bot.addToCorpus("corpusBodySource")
    else:
        big_bot.addToCorpus(corpi[0])
    await ctx.send("I have added those files to the corpus")


@bot.command()
async def sb(ctx):
    big_bot.save_whole_brain()

@bot.command()
async def lb(ctx):
    big_bot.load_entire_brain()


@bot.event
async def on_message(message):
    global autogenCounter
    global autogenInt
    if await bot.process_commands(message):
        pass
    else:
        try:
            if message.channel in talkOrListen:
                if talkOrListen[message.channel]:
                    if int(autogenCounter) % int(autogenInt) == 0:
                        if message.author == bot.user:
                            if message.channel.name == 'gaulle':
                                await message.reply(big_bot.get_response(message.content, ["discord convo", "self talk"]))
                                return
                            else:
                                return
                        await message.reply(big_bot.get_response(message.content, [str(message.author), str(message.channel)]))
                    autogenCounter += 1
        except Exception as e:
            print("I didn't hit the mark :( + {}".format(e))
        finally:
            pass


async def swimThroughMessages(messageTOTAL):
    string = ""
    if messageTOTAL.reference is not None:
        msg = await messageTOTAL.channel.fetch_message(messageTOTAL.reference.message_id)
        string += await swimThroughMessages(msg)
    string += messageTOTAL.content + " "
    return string



bot.run(my_secret)

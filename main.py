from discord.ext import commands
import os
import discord
import textManager as tm
import traceback
import letsUseClasses
flag = True



my_secret = os.environ['TOKEN']
bot = commands.Bot(command_prefix='`')
talkOrListen = {}
autogenInt = 1
autogenCounter = 1




@bot.command()
async def save(ctx):
    pass


@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot) + "\nPlease use $init with any applicable corpi separated with a space or leave blank for defaults\nRegardless, `init or I won't work")


@bot.command()
async def autogen(ctx, autogenAmount):
    global autogen
    global autogenCounter
    global autogenInt
    autogen = autogenAmount
    autogenCounter = 1
    await ctx.channel.send("I will now message every {} messages. AutoGeneration Counter is {}".format(autogenAmount,autogenCounter))


@bot.command()
async def loadUsers(ctx):
    newCorpusLoader = "activeUse/tempThinking"
    newFile = open(newCorpusLoader, "w", encoding="utf-8")
    for file in os.listdir("peopleiknow"):
        newFile.write("peopleiknow/" + file + "\n")
    newFile.close()
    await init(ctx, newCorpusLoader)





@bot.command()
async def newChann(ctx, *, name=None):
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
            await guild.create_text_channel(name)
            await ctx.send(f"Created a channel named {name}. Message 'talk to begin there!")
            return




@bot.command()
async def talkAll(ctx):
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
    if len(corpi) == 0:
        letsUseClasses.addToCorpus("corpusBodySource")
    else:
        tm.corpusInit(corpi, False)
    await ctx.send("I have added those files to the corpus")


@bot.event
async def on_message(message):
    global autogenCounter
    global autogenInt
    if await bot.process_commands(message):
        pass
    else:
        try:
            if message.channel in talkOrListen:
                if int(autogenCounter) % int(autogenInt) == 0:
                    if message.author == bot.user:
                        if message.channel.name == 'gaulle':
                            await message.reply(letsUseClasses.getResponse(message.content))
                            return
                        else:
                            return

                    await message.reply(letsUseClasses.getResponse(message.content))
                autogenCounter += 1
            raise KeyError
        except Exception as e:
            traceback.print_exc()
            print("I didn't hit the mark :(")
        finally:
            letsUseClasses.getResponse(message.content)





bot.run(my_secret)

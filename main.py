from discord.ext import commands
import os
import textManager as tm
flag = True


my_secret = os.environ['TOKEN']
bot = commands.Bot(command_prefix='`')
initFlag = False
talkOrListen = {}
autogenInt = 1
autogenCounter = 1




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
async def talk(ctx):
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



@bot.command()
async def init(ctx, *corpi):
    global initFlag
    if not initFlag:
        if len(corpi) == 0:
            tm.corpusInit()
        else:
            tm.corpusInit(corpi)
        await ctx.send("I have initialized the corpus with {} arguments".format(corpi))
        global flag
        flag = False
        initFlag = True


@bot.event
async def on_message(message):
    global autogenCounter
    global autogenInt
    if await bot.process_commands(message):
        pass
    else:
        try:
            if talkOrListen[message.channel]:
                if int(autogenCounter) % int(autogenInt) == 0:
                    if message.author == bot.user:
                        if message.channel.name == 'gaulle':
                            await message.reply(tm.getResponse(message.content))
                            return
                        else:
                            return
                    if not initFlag:
                        await message.reply("Please `init me to begin.")
                    else:
                        response = message.content
                        await message.reply(tm.getResponse(response))
                autogenCounter += 1
        except:
            tm.processMessage(message.content)
        finally:
            pass





bot.run(my_secret)

import discord
import asyncio
from discord.ext import commands
import subprocess
import ffmpeg

token = os.environ['DISCORD_BOT_TOKEN']
client = commands.Bot(command_prefix='.')
voice_client = None
@client.event
async def on_ready():
    print(client.user.name + ' 起動')

@client.command()
async def join(ctx):
    vc = ctx.author.voice.channel
    await vc.connect()
    mes = "ワイはアル太郎や読み上げたるでぇ"
    await ctx.send(mes)

@client.command()
async def bye(ctx):
    await ctx.voice_client.disconnect()
    await ctx.send("ほなさいなら")

@client.event
async def on_message(message):
    if message.content.startswith('.'):
        pass
    elif message.author.bot:
        pass
    else:
        mes = message.content
        create_wav(mes)
        ffmpeg_audio_source = discord.FFmpegPCMAudio("open_jtalk.wav")
        message.guild.voice_client.play(ffmpeg_audio_source)
    await client.process_commands(message)

def create_wav(txt):
    open_jtalk=['open_jtalk']
    mech=['-x','/usr/local/share/open_jtalk/open_jtalk_dic_utf_8-1.10']
    htsvoice=['-m','/usr/local/share/hts_voice/mei/mei_normal.htsvoice']
    speed=['-r','1.0']
    outwav=['-ow','open_jtalk.wav']
    cmd=open_jtalk+mech+htsvoice+speed+outwav
    c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
    c.stdin.write(txt.encode('utf-8'))
    c.stdin.close()
    c.wait()

client.run(token)

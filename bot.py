import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

# 創建機器人
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ 機器人已登錄：{bot.user}')
    print(f'延遲：{bot.latency * 1000:.0f}ms')
    
    # 自動加入語音頻道掛機
    await auto_join_voice()

@bot.event
async def on_voice_state_update(member, before, after):
    """當有人加入語音頻道時觸發"""
    if member == bot.user:
        return
    
    # 如果有人加入語音頻道，確保機器人在線
    if after.channel and not before.channel:
        print(f'{member.name} 加入了語音頻道 {after.channel.name}')

async def auto_join_voice():
    """自動加入第一個找到的語音頻道"""
    try:
        for guild in bot.guilds:
            # 查找有人的語音頻道
            for channel in guild.voice_channels:
                if len(channel.members) > 0:
                    # 檢查機器人是否已經在語音頻道中
                    if guild.voice_client is None:
                        print(f'🎙️ 正在加入語音頻道：{channel.name}')
                        await channel.connect()
                        return
    except Exception as e:
        print(f'❌ 自動加入語音頻道時出錯：{e}')

@bot.command(name='join')
async def join(ctx):
    """加入你所在的語音頻道"""
    if ctx.author.voice is None:
        await ctx.send('❌ 你需要先加入一個語音頻道')
        return
    
    channel = ctx.author.voice.channel
    try:
        await channel.connect()
        await ctx.send(f'✅ 已加入語音頻道：{channel.name}')
    except Exception as e:
        await ctx.send(f'❌ 無法加入語音頻道：{e}')

@bot.command(name='leave')
async def leave(ctx):
    """離開語音頻道"""
    if ctx.guild.voice_client is None:
        await ctx.send('❌ 機器人未在任何語音頻道中')
        return
    
    await ctx.guild.voice_client.disconnect()
    await ctx.send('✅ 已離開語音頻道')

@bot.command(name='ping')
async def ping(ctx):
    """檢查機器人延遲"""
    latency = bot.latency * 1000
    await ctx.send(f'🏓 Pong！延遲：{latency:.0f}ms')

@bot.command(name='status')
async def status(ctx):
    """檢查機器人狀態"""
    if ctx.guild.voice_client is None:
        voice_status = '❌ 未連接'
    else:
        voice_status = f'✅ 已連接至 {ctx.guild.voice_client.channel.name}'
    
    await ctx.send(f'```\n機器人狀態\n----------\n語音：{voice_status}\n延遲：{bot.latency * 1000:.0f}ms\n```')

@bot.command(name='help')
async def help(ctx):
    """顯示所有命令"""
    embed = discord.Embed(title='🤖 機器人命令列表', color=discord.Color.blue())
    embed.add_field(name='!join', value='加入你所在的語音頻道', inline=False)
    embed.add_field(name='!leave', value='離開語音頻道', inline=False)
    embed.add_field(name='!ping', value='檢查機器人延遲', inline=False)
    embed.add_field(name='!status', value='檢查機器人狀態', inline=False)
    embed.add_field(name='!help', value='顯示此幫助訊息', inline=False)
    
    await ctx.send(embed=embed)

# 啟動機器人
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN:
    bot.run(TOKEN)
else:
    print('❌ 錯誤：找不到 DISCORD_TOKEN 環境變數')

from typing import Literal
import discord
from discord.ext import commands
import secret, utils, defs, description

intents = discord.Intents.default()
intents.message_content = True

BOT = commands.Bot(command_prefix='$', intents = intents)
CONFIG = defs.bot_config('config.json')
MATCH: dict[int, utils.Match] = {}

@BOT.event
async def on_ready():
    await BOT.tree.sync()
    CONFIG.load_def(BOT.guilds[0])
    print(CONFIG.property['admin'].name)
    print(CONFIG.property['gamming'].name)

@BOT.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('此指令僅限管理員使用')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('參數輸入數量錯誤，指令無法執行')
    else:
        await ctx.send('未知錯誤，請洽詢程式設計師')

@BOT.event
async def on_message(message):
    if message.author == BOT.user:
        return
    if '寄' in message.content:
        await message.channel.send('寄什麼寄，恐懼源自於課金不足')

## command SELECT
@BOT.hybrid_command(name='select', description='[ 參賽者指令 ] 選擇己方所要Ban / Pick的幹員，當多於一個幹員時，使用空白分隔')
async def select(ctx: commands.Context, rolenames: str):
    if not utils.has_role(ctx.author, CONFIG.property.get('gamming')):
        await ctx.send('權限錯誤，指令無法執行')
        return
    await ctx.send(rolenames)
    print(rolenames.split())

## command MATCH
@BOT.hybrid_command(name='match', description='[ 主辦方指令 ] 設定比賽分組，並指定BP專用頻道')
async def match(ctx: commands.Context, channel: discord.TextChannel, role1: discord.Role, role2: discord.Role):
    if not utils.has_role(ctx.author, CONFIG.property.get('author')):
        await ctx.send('權限錯誤，指令無法執行')
        return
    if channel.id in MATCH:
        await ctx.send('已設定過該頻道，將直接覆蓋原設定')
    MATCH[channel.id] = utils.Match(channel, [role1, role2])
    await ctx.send(description.get_match(channel.mention, role1.mention, role2.mention))

## command CONFIRM
@BOT.hybrid_command(name='confirm', description='[ 主辦方指令 ] 確認該比賽分組的BP結果無誤')
async def confirm(ctx: commands.Context):
    if not utils.has_role(ctx.author, CONFIG.property.get('author')):
        await ctx.send('權限錯誤，指令無法執行')
        return
    await ctx.send('BP結果確認成功')

## command RESET
@BOT.hybrid_command(name='reset', description='[ 主辦方指令 ] 取消這次比賽分組的BP，將自動回到BP最初階段，並重新計時')
async def reset(ctx: commands.Context):
    if not utils.has_role(ctx.author, CONFIG.property.get('author')):
        await ctx.send('權限錯誤，指令無法執行')
        return
    await ctx.send('BP結果已被重置，自動回至BP最初階段')

## command CONFIG_ROLE
@BOT.hybrid_command(name='config_role', description='[ 管理者指令 ] 設置機器人相關身分組權限')
@commands.has_permissions(administrator=True)
async def config_role(ctx: commands.Context, option: Literal['admin', 'gamming'], role: discord.Role):
    if option == 'admin':
        await ctx.send(role.mention)
    elif option == 'gamming':
        await ctx.send(role.mention)
    else:
        await ctx.send('Usage: /config_role [\'admin\' | \'gamming\'] [@Role]')

## command CONFIG_CHANNEL
@BOT.hybrid_command(name='config_channel', description='[ 管理者指令 ] 設置機器人相關使用頻道')
@commands.has_permissions(administrator=True)
async def config_channel(ctx: commands.Context, option: Literal['log'], channel: discord.TextChannel):
    if option == 'log':
        await ctx.send(channel.mention)
    else:
        await ctx.send('Usage: /config_channel [\'log\'] [#Channel]')

BOT.run(secret.bot_token)

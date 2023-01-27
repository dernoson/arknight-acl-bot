import discord
from discord.ext import commands
import secret, utils, defs, description
from match import Match
from threading import Timer

BOT_INTENTS = discord.Intents.default()
BOT_INTENTS.message_content = True
BOT = commands.Bot(command_prefix='$', intents = BOT_INTENTS)
CONFIG = defs.bot_config('config.json')
MATCH: dict[int, Match] = {}
ALLOW_MENTION = discord.AllowedMentions(everyone=False, users=True, roles=True, replied_user=True)

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
async def on_message(message: discord.Message):
    if message.author == BOT.user:
        return
    if '寄' in message.content:
        await message.channel.send('寄什麼寄，恐懼源自於課金不足')
    # else:
    #     re = utils.get_rand_xddd()
    #     if re:
    #         await message.channel.send(re)

## command SELECT
@BOT.hybrid_command(name='select', description='[ 參賽者指令 ] 選擇己方所要Ban / Pick的幹員，當多於一個幹員時，使用空白分隔')
async def select(ctx: commands.Context, rolenames: str):
    if not ctx.channel.id in MATCH:
        await ctx.send('該頻道目前未指定為BP頻道')
        return

    channel_match = MATCH[ctx.channel.id]
    if channel_match.state != 'running':
        await ctx.send('當前頻道BP流程可能尚未開始，或是已經結束')
    elif not (utils.has_role(ctx.author, channel_match.get_now_team().team)):
        await ctx.send('當前頻道內你並無使用/select指令的權限')
    else:
        roles = list(set(rolenames.strip().split()))
        await ctx.send(channel_match.select_role(roles), allowed_mentions=ALLOW_MENTION)

## command MATCH
@BOT.hybrid_command(name='match', description='[ 主辦方指令 ] 設定比賽分組，並指定BP專用頻道')
async def match(ctx: commands.Context, channel: discord.TextChannel, role1: discord.Role, role2: discord.Role):
    if not utils.has_role(ctx.author, CONFIG.property.get('admin')):
        await ctx.send('權限錯誤，指令無法執行')
        return
    if channel.id in MATCH:
        await ctx.send('已設定過該頻道，將直接覆蓋原設定')

    new_match = Match(channel, (role1, role2))
    MATCH[channel.id] = new_match
    await ctx.send(description.get_match_description(channel.mention, role1.mention, role2.mention))
    await channel.send(f'=== {role1.mention} vs {role2.mention} ===\n**BP 流程開始**', allowed_mentions=ALLOW_MENTION)
    await channel.send(new_match.start(), allowed_mentions=ALLOW_MENTION)
    

## command CONFIRM
@BOT.hybrid_command(name='confirm', description='[ 主辦方指令 ] 確認該比賽分組的BP結果無誤')
async def confirm(ctx: commands.Context):
    if not utils.has_role(ctx.author, CONFIG.property.get('admin')):
        await ctx.send('權限錯誤，指令無法執行')
        return
    await ctx.send('BP結果確認成功')

## command RESET
@BOT.hybrid_command(name='reset', description='[ 主辦方指令 ] 取消這次比賽分組的BP，將自動回到BP最初階段，並重新計時')
async def reset(ctx: commands.Context):
    if not utils.has_role(ctx.author, CONFIG.property.get('admin')):
        await ctx.send('權限錯誤，指令無法執行')
        return
    await ctx.send('BP結果已被重置，自動回至BP最初階段')

## command CONFIG_ADMIN
@BOT.hybrid_command(name='config_admin', description='[ 管理者指令 ] 設置主辦方身分組與log使用頻道')
@commands.has_permissions(administrator=True)
async def config_admin(ctx: commands.Context, role: discord.Role, channel: discord.TextChannel):
    CONFIG.set_def('admin', role)
    CONFIG.set_def('log_channel', channel)
    await ctx.send(f'主辦方權限已設置給 {role.mention}\n機器人log頻道已設置於 {channel.mention}')

## command LOG_CONFIG
@BOT.hybrid_command(name='log_config', description='[ 管理者指令 ] 輸出所有機器人設定')
@commands.has_permissions(administrator=True)
async def log_config(ctx: commands.Context):
    pass

BOT.run(secret.bot_token)

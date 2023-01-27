from typing import Literal
from match import Match, BP
from utils import get_flow
from matchFlow import MATCH_FLOW

def get_match_description(channel: str, role1: str, role2: str):
    return f'\
對戰組合：{role1} vs {role2}\n\
指定BP頻道： {channel}\
'

def get_team_rolelist(team_bp: BP, option: Literal['ban', 'pick']):
    rolelist_str = " ".join(team_bp.rolelist[option])
    if rolelist_str:
        return f'{team_bp.team.name} {option}：\n```\n{rolelist_str}\n```\n'
    return ''

def get_selectRole_description(roles: list[str], match: Match):
    teamA = match.teams[0]
    teamB = match.teams[1]
    team_toselect_role = match.teams[match.turns].team
    team_lastselect_role = match.teams[match.switched_turn()].team

    description = ''
    if match.stage != 0:
        description += f'{team_lastselect_role.name} 選擇了 `{" ".join(roles)}`\n\n'

    description += get_team_rolelist(teamA, 'ban') + get_team_rolelist(teamB, 'ban') + get_team_rolelist(teamA, 'pick') + get_team_rolelist(teamB, 'pick')

    now_flow = get_flow(MATCH_FLOW, match.stage)
    if now_flow:
        description += f'請 {team_toselect_role.mention} 開始選擇要 {now_flow.option} 的 {now_flow.amount} 位幹員'
    else:
        description += f'BP流程已結束，請主辦方進行最後確認'

    return description

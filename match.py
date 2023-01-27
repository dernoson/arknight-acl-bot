from typing import Literal
from discord import Role, TextChannel
from matchFlow import MATCH_FLOW, BPType
from utils import get_flow

class Match():
    def __init__(self, channel: TextChannel, teams: tuple[Role, Role], banlimit = 5, picklimit = 12):
        self.channel = channel
        self.teams = (BP(teams[0]), BP(teams[1]))
        self.banlimit = banlimit
        self.picklimit = picklimit
        self.stage = 0
        self.turns: Literal[0, 1] = 0
        self.state: Literal['idle', 'running', 'pause', 'complete'] = 'idle'

    def get_now_team(self):
        return self.teams[self.turns]

    def switched_turn(self):
        if self.turns == 1:
            return 0
        else:
            return 1

    def next_stage(self):
        self.stage += 1
        self.turns = self.switched_turn()
        if not self.stage < len(MATCH_FLOW):
            self.state = 'pause'
        return self.get_stage_description()

    def last_stage(self):
        self.stage -= 1
        self.turns = self.switched_turn()
        last_stage = get_flow(MATCH_FLOW, self.stage)
        if not last_stage:
            return '已為最初狀態，無法再回到上一步'

        stage_bp = self.get_now_team()
        stage_rolelist = stage_bp.rolelist[last_stage.option]
        canceled_roles = stage_rolelist[-last_stage.amount:]
        new_rolelist = stage_rolelist[:-last_stage.amount]
        stage_bp.rolelist[last_stage.option] = new_rolelist

        return f'返回步驟：{stage_bp.team.name} {last_stage.option} ~~{", ".join(canceled_roles)}~~'

    def start(self):
        if self.stage < len(MATCH_FLOW):
            self.state = 'running'
        return self.get_stage_description()

    # def reset(self):
    #     for team in self.teams:
    #         team.rolelist = {'ban': [], 'pick': []}
    #     self.stage = 0
    #     self.turns = 0
    #     self.state = 'running'

    def select_role(self, roles: list[str]) -> str:
        duplicate = ", ".join(self.teams[0].get_duplicate(roles) + self.teams[1].get_duplicate(roles))
        if duplicate:
            return f'選擇的幹員已被選擇過({duplicate})'

        now_flow = get_flow(MATCH_FLOW, self.stage)
        if not now_flow:
            return 'BP流程已結束，無法選擇幹員'

        if self.state != 'running':
            return 'BP流程並非進行中，無法選擇幹員'

        stage_amount = now_flow.amount
        if len(roles) != stage_amount:
            return f'選擇幹員數量應為 {stage_amount} 位，你選擇了 {len(roles)} 位，請重新選擇'

        stage_bp = self.get_now_team()
        stage_bp.rolelist[now_flow.option].extend(roles)

        return f'\
{stage_bp.team.name} 選擇了 `{" ".join(roles)}`\n\
《當前Ban除幹員》\n\
{self.get_rolelist_description(0, "ban", self.banlimit)}\
{self.get_rolelist_description(1, "ban", self.banlimit)}\
《當前Pick幹員》\n\
{self.get_rolelist_description(0, "pick", self.picklimit)}\
{self.get_rolelist_description(1, "pick", self.picklimit)}\
\n\
{self.next_stage()}'

    def get_rolelist_description(self, teamIdx: Literal[0, 1], option: Literal['ban', 'pick'], limit: int) -> str:
        team_bp = self.teams[teamIdx]
        rolelist = team_bp.rolelist[option]
        if len(rolelist):
            return f'\
{team_bp.team.name} ({len(rolelist)}/{limit})：\n\
```\n\
{" ".join(rolelist)}\n\
```\n'
        return ''

    def get_stage_description(self) -> str:
        now_flow = get_flow(MATCH_FLOW, self.stage)
        if now_flow:
            return f'請 {self.get_now_team().team.mention} 開始選擇要 {now_flow.option} 的 {now_flow.amount} 位幹員'
        else:
            return f'BP流程已結束，請主辦方進行最後確認'

class BP():
    def __init__(self, teamrole: Role):
        self.team = teamrole
        self.rolelist: dict[BPType, list[str]] = {'ban': [], 'pick': []}

    def get_duplicate(self, roles: list[str]):
        duplicate: list[str] = []
        for r in roles:
            if r in self.rolelist['ban'] or r in self.rolelist['pick']:
               duplicate.append(r)
        return duplicate

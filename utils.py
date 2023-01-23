from typing import Callable
from discord import Role, TextChannel, User, Member
from discord.ext import commands

def has_role(author: User | Member, role: Role | None):
    if isinstance(author, User):
        return False
    if role and author.get_role(role.id):
        return True
    return False

class Match():
    def __init__(self, channel: TextChannel, teams: list[Role]):
        self.channel = channel
        self.teams = teams
        self.stage = 0
    

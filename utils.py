from discord import Role, User, Member
from matchFlow import matchStage
import random

def has_role(author: User | Member, role: Role | None):
    if not isinstance(author, Member):
        return False
    if role and author.get_role(role.id):
        return True
    return False

def get_flow(flowList: list[matchStage], index: int):
    try:
        return flowList[index]
    except:
        return None

def get_rand_xddd() -> str | None:
    value = random.randint(1, 25)
    if value == 1:
        return '形不成形，意不在意！'
    elif value == 2:
        return '千招百式在一息！'
    elif value == 3:
        return '你們解決問題！'
    elif value == 4:
        return '再回去練練吧！'
    elif value == 5:
        return '勁發江潮落！'
    elif value == 6:
        return '氣收秋毫平！'

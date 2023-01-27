from typing import Literal

BPType = Literal['ban', 'pick']

class matchStage():
    def __init__(self, option: BPType, amount: int):
        self.option: BPType = option
        self.amount = amount

MATCH_FLOW: list[matchStage] = [
    matchStage('ban', 1),
    matchStage('ban', 1),
    matchStage('ban', 1),
    matchStage('ban', 1),
    matchStage('ban', 1),
    matchStage('ban', 1),
    matchStage('pick', 1),
    matchStage('pick', 2),
    matchStage('pick', 2),
    matchStage('pick', 2),
    matchStage('pick', 2),
    matchStage('pick', 2),
    matchStage('pick', 1),
    matchStage('ban', 1),
    matchStage('ban', 1),
    matchStage('ban', 1),
    matchStage('ban', 1),
    matchStage('pick', 1),
    matchStage('pick', 2),
    matchStage('pick', 2),
    matchStage('pick', 2),
    matchStage('pick', 2),
    matchStage('pick', 2),
    matchStage('pick', 1)
]

import copy
from tetromino import *
from direction import *
from rotation import *

class GreedyPlayer:

    def __init__(self, board, gapPenaltyFactor = -1.0, stackHeightFactor = -0.5, surfaceRoughnessFactor = -0.3, clearBonusFactor = -1.0):
        self.board = board
        self.gapPenaltyFactor = gapPenaltyFactor
        self.stackHeightFactor = stackHeightFactor
        self.surfaceRoughnessFactor = surfaceRoughnessFactor
        self.clearBonusFator = clearBonusFactor

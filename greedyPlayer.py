from tetromino import *
from direction import *
from rotation import *
from gridUtils import gridUtils

class GreedyPlayer:

    def __init__(self, 
                 board, 
                 gapPenaltyFactor = -10,
                 stackHeightFactor = -0.5, 
                 surfaceRoughnessFactor = -0.2, 
                 clearBonusFactor = 4
                 ):
        
        self.board = board
        self.gapPenaltyFactor = gapPenaltyFactor
        self.stackHeightFactor = stackHeightFactor
        self.surfaceRoughnessFactor = surfaceRoughnessFactor
        self.clearBonusFactor = clearBonusFactor
    
    def scorePlacement(self, placement):
        heights = gridUtils.getColumnHeight(placement["grid"], self.board.width, self.board.height)
        holes = gridUtils.countHoles(placement["grid"], self.board.width, self.board.height)
        roughness = gridUtils.getBumpiness(heights)

        score = (self.gapPenaltyFactor * holes 
                 + self.stackHeightFactor * sum(heights)
                 + self.surfaceRoughnessFactor * roughness
                 + self.clearBonusFactor * placement["linesCleared"])
        return score

    def chooseMove(self, tetromino): 
        placements = self.board.getLegalPlacements(tetromino)
        bestPlacement = max(placements, key = self.scorePlacement)
        return {"rotation": bestPlacement["rotation"], "xPos": bestPlacement["xPos"]}

    def makeMove(self, tetromino):
        move = self.chooseMove(tetromino)
        return self.board.applyPlacement(tetromino, move["xPos"], move["rotation"])
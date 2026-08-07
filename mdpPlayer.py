import copy, random
from tetromino import *
import numpy as np
from direction import *
from rotation import *
from board import Board
from gridUtils import gridUtils

class MdpPlayer:

    featureNames = ["holes", "aggHeight", "bumpiness", "bias"]
    allShapes = list(Tetromino._allShapes.keys())
    lineScores = (0, 1, 3, 5, 8)
 
    def __init__(self, weights=None, gamma=0.95):
        self.gamma = gamma
        self.weights = np.array(weights, dtype=float) if weights is not None \
            else np.zeros(len(self.featureNames))
 
    def getFeatures(self, grid, width, height):
        heights = gridUtils.getColumnHeight(grid, width, height)
        holes = gridUtils.countHoles(grid, width, height)
        bumpiness = gridUtils.getBumpiness(heights)
        return np.array([holes, sum(heights), bumpiness, 1.0])
 
    def value(self, features):
        return float(self.weights @ features)
 
    def _placementReward(self, board, placement):
        return self.lineScores[placement["linesCleared"]] 
 
    def _bestPlacement(self, board, tetromino):
        placements = board.getLegalPlacements(tetromino)
        best, bestVal = None, -float("inf")
        for p in placements:
            reward = self._placementReward(board, p)
            features = self.getFeatures(p["grid"], board.width, board.height)
            v = reward + self.gamma * self.value(features)
            if v > bestVal:
                bestVal, best = v, p
        if best is None:
            raise ValueError("No legal placements available")
        return best
 
    def sampleStates(self, numStates, maxStepsPerEpisode=200, explorationRate=0.15):
        states = []
        board = Board()
        tetromino = board.generatePiece()
        steps = 0
 
        while len(states) < numStates:
            if board.isGridBlocked(tetromino) or steps >= maxStepsPerEpisode:
                board = Board()
                tetromino = board.generatePiece()
                steps = 0
                continue
 
            states.append(copy.deepcopy(board.grid))
 
            if random.random() < explorationRate:
                move = random.choice(board.getLegalPlacements(tetromino))
            else:
                move = self._bestPlacement(board, tetromino)
 
            board.applyPlacement(tetromino, move["xPos"], move["rotation"])
            tetromino = board.generatePiece()
            steps += 1
 
        return states
 
    def bellmanTarget(self, grid, boardTemplate):
        pieceValues = []
        for shape in self.allShapes:
            scratchBoard = copy.deepcopy(boardTemplate)
            scratchBoard.grid = copy.deepcopy(grid)
            tetromino = Tetromino(shape)
            scratchBoard.centrePiece(tetromino)
 
            if scratchBoard.isGridBlocked(tetromino):
                pieceValues.append(0.0)  # can't place at all -> terminal, value 0
                continue
 
            best = -float("inf")
            for p in scratchBoard.getLegalPlacements(tetromino):
                reward = self._placementReward(scratchBoard, p)
                features = self.getFeatures(p["grid"], scratchBoard.width, scratchBoard.height)
                best = max(best, reward + self.gamma * self.value(features))
            pieceValues.append(best)
        return sum(pieceValues) / len(pieceValues)
 
    def fitWeights(self, states, targets, boardTemplate):
        X = np.array([self.getFeatures(s, boardTemplate.width, boardTemplate.height) for s in states])
        y = np.array(targets)
        newWeights, *_ = np.linalg.lstsq(X, y, rcond=None)
        return newWeights
 
    def runValueIteration(self, numIterations=20, numStates=300, verbose=True):
        boardTemplate = Board()
        for iteration in range(numIterations):
            states = self.sampleStates(numStates)
            targets = [self.bellmanTarget(s, boardTemplate) for s in states]
            newWeights = self.fitWeights(states, targets, boardTemplate)
 
            delta = float(np.linalg.norm(newWeights - self.weights))
            self.weights = newWeights
 
            if verbose:
                print(f"iteration {iteration}: weights={self.weights}, weight_delta={delta:.4f}")
 
        return self.weights
 
    def chooseMove(self, board, tetromino):
        best = self._bestPlacement(board, tetromino)
        return {"rotation": best["rotation"], "xPos": best["xPos"]}
 
    def makeMove(self, board, tetromino):
        move = self.chooseMove(board, tetromino)
        return board.applyPlacement(tetromino, move["xPos"], move["rotation"])


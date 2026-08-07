

class gridUtils:

    @staticmethod
    def getColumnHeight(grid, width, height):
        heights = []
        for x in range(width):
            colHeight = 0
            for y in range(height):
                if grid[y][x] != 0:
                    colHeight = height - y
                    break
            heights.append(colHeight)
        return heights

    @staticmethod
    def countHoles(grid, width, height):
        # A Hole -> An empty cell with at least one filled cell above it in the same column
        holes = 0
        for x in range(width):
            blockFound = False
            for y in range(height):
                if grid[y][x] != 0:
                    blockFound = True
                elif blockFound:
                    holes += 1
        return holes

    @staticmethod
    def getBumpiness(heights): 
        bumpiness = 0
        for i in range(len(heights) - 1):
            bumpiness += abs(heights[i] - heights[i + 1])
        return bumpiness
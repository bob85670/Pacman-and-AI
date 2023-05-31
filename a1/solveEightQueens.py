import random
import copy
from optparse import OptionParser
import util

class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        """
        Value 1 indicates the position of queen
        """
        self.numberOfRuns = numberOfRuns
        self.verbose = verbose
        self.lectureCase = [[]]
        if lectureExample:
            self.lectureCase = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    def solve(self):
        solutionCounter = 0
        for i in range(self.numberOfRuns):
            if self.search(Board(self.lectureCase), self.verbose).getNumberOfAttacks() == 0:
                solutionCounter += 1
        print("Solved: %d/%d" % (solutionCounter, self.numberOfRuns))

    def search(self, board, verbose):
        """
        Hint: Modify the stop criterion in this function
        """
        newBoard = board
        i = 0 
        while i < 100:
            if verbose:
                print("iteration %d" % i)
                print(newBoard.toString())
                print("# attacks: %s" % str(newBoard.getNumberOfAttacks()))
                print(newBoard.getCostBoard().toString(True))
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            (newBoard, newNumberOfAttacks, newRow, newCol) = newBoard.getBetterBoard()
            i += 1
            #if currentNumberOfAttacks <= newNumberOfAttacks:
            #    break
        return newBoard

class Board:
    def __init__(self, squareArray = [[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray

    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [[ 0 for i in range(8)] for j in range(8)]
        for i in range(8):
            tmpSquareArray[random.randint(0,7)][i] = 1
        return tmpSquareArray
          
    def toString(self, isCostBoard=False):
        """
        Transform the Array in Board or cost Board to printable string
        """
        s = ""
        for i in range(8):
            for j in range(8):
                if isCostBoard: # Cost board
                    cost = self.squareArray[i][j]
                    s = (s + "%3d" % cost) if cost < 9999 else (s + "  q")
                else: # Board
                    s = (s + ". ") if self.squareArray[i][j] == 0 else (s + "q ")
            s += "\n"
        return s 

    def getCostBoard(self):
        """
        First Initalize all the cost as 9999. 
        After filling, the position with 9999 cost indicating the position of queen.
        """
        costBoard = Board([[ 9999 for i in range(8)] for j in range(8)])
        for r in range(8):
            for c in range(8):
                if self.squareArray[r][c] == 1:
                    for rr in range(8):
                        if rr != r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = 0
                            testboard.squareArray[rr][c] = 1
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        """
        
        This function should return a tuple containing containing four values
        the new Board object, the new number of attacks, 
        the Column and Row of the new queen  
        For exmaple: 
            return (betterBoard, minNumOfAttack, newRow, newCol)
        The datatype of minNumOfAttack, newRow and newCol should be int
        """
        "*** YOUR CODE HERE ***"

        
        tempBoard = copy.deepcopy(self)
        tempCostBoard = tempBoard.getCostBoard()

        #print(tempCostBoard.toString(True))

        """
        for i in range(8):
            for j in range(8):
                print(tempCostBoard.squareArray[j][i])

        """
        #print(tempBoard.toString(True))

        """
        for i in range(8):
            for j in range(8):
                print(tempBoard.squareArray[j][i])

        """  

        smallest_int = 999

        for i in range(8):
            for j in range(8):
                if tempCostBoard.squareArray[j][i] < smallest_int:
                    smallest_int = tempCostBoard.squareArray[j][i]
        

        #print("Smallest: ", smallest_int)


        a = 0
        b = 0
        for i in range(8):
            for j in range(8):

                #print("temp pos: ", j,i, tempCostBoard.squareArray[j][i])

                if tempCostBoard.squareArray[j][i] == smallest_int:
                    a, b = j, i
                    
                    break

            else:
                continue

            break
                    
        #print("a, b:", a, b)


        for k in range(8):
            if tempBoard.squareArray[k][b] == 1:
                #print("Original q:", k, b)
                tempBoard.squareArray[a][b] = 1
                tempBoard.squareArray[k][b] = 0
                break

        #print(tempBoard.toString(True))

        return (tempBoard, smallest_int, a, b)
        


        util.raiseNotDefined()




    def getNumberOfAttacks(self):
        """
        This function should return the number of attacks of the current board
        The datatype of the return value should be int
        """
        "*** YOUR CODE HERE ***"
        count = 0

        #i: column, j: row
        for i in range(8):
            for j in range(8):
                if self.squareArray[j][i] == 1:

                    #print("Visiting: " ,j,i)

                    #checking attacks
                    for k in range(7-i):        #right
                        if self.squareArray[j][k+i+1] == 1:
                            count += 1

                            #print(j, k+i+1)

                    a, b = j-1, i+1             #up (right) diagonal
                    while a >= 0 and b < 8:

                        #print("Up Diagonal: ", a, b)

                        if self.squareArray[a][b] == 1:
                            count += 1
                        a, b = a-1, b+1

                    c, d = j+1, i+1             #down (right) diagonal
                    while c < 8 and d < 8:

                        #print("Down diagonal: ", c, d)

                        if self.squareArray[c][d] == 1:
                            count += 1
                        c, d = c+1, d+1


        return count

        

        util.raiseNotDefined()



if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    random.seed(1)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    EightQueensAgent = SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)
    EightQueensAgent.solve()

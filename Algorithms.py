from Board import *

class Algorithms:

    def __init__(self):
        self.started = False
        self.finished = False
        self.complete = False

    #performs one iteration of algorithm
    def BFS(self, board):
        if board.running and board.live:
            if not self.complete:
                if not self.finished or board.started:

                    #first iteration
                    if not self.started or board.started:
                        board.currentCell = board.start
                        board.celllist.append(board.currentCell)
                        board.visitedCells.append(board.currentCell)
                        board.parentCells[board.currentCell] = None
                        self.started = True
                        board.started = False


                    # generic iteration
                    if(len(board.celllist)>0):
                    
                        #pop off of queue
                        board.currentCell = board.celllist.pop(0)

                        #check if goal node
                        if(board.currentCell == board.goal):
                            self.finished = True
                            board.path.append(board.goal)
                            board.backtrack = board.goal

                        #get neighbors
                        board.neighbors = board.getNeighbors(board.currentCell)
                        print(len(board.neighbors))
                        for n in board.neighbors:
                            if n not in board.visitedCells:
                                board.celllist.append(n)
                                board.parentCells[n] = board.currentCell
                                board.visitedCells.append(n)

                    else:
                        print("no possible path")

                

                else:
                    #clear neighbors
                    board.neighbors = []
                    if(board.parentCells[board.backtrack] != None):
                        board.backtrack = board.parentCells[board.backtrack]
                        board.path.append(board.backtrack)
                    else:
                        self.complete = True

        return board
                    
    
    def DFS(self, board):
        if board.running and board.live:
            if not self.complete:
                if not self.finished or board.started:

                    #first iteration
                    if not self.started or board.started:
                        board.currentCell = board.start
                        board.celllist.append(board.currentCell)
                        board.visitedCells.append(board.currentCell)
                        board.parentCells[board.currentCell] = None
                        self.started = True
                        board.started = False


                    # generic iteration
                    if(len(board.celllist)>0):
                    
                        #pop off of queue
                        board.currentCell = board.celllist.pop(len(board.celllist)-1)

                        #check if goal node
                        if(board.currentCell == board.goal):
                            self.finished = True
                            board.path.append(board.goal)
                            board.backtrack = board.goal

                        #get neighbors
                        board.neighbors = board.getNeighbors(board.currentCell)
                        print(len(board.neighbors))
                        for n in board.neighbors:
                            if n not in board.visitedCells:
                                board.celllist.append(n)
                                board.parentCells[n] = board.currentCell
                                board.visitedCells.append(n)

                    else:
                        print("no possible path")

                

                else:
                    #clear neighbors
                    board.neighbors = []
                    if(board.parentCells[board.backtrack] != None):
                        board.backtrack = board.parentCells[board.backtrack]
                        board.path.append(board.backtrack)
                    else:
                        self.complete = True

        return board
                        

    def ASTAR(self, board):
        if board.running and board.live:
            if not self.complete:
                if not self.finished or board.started:

                    #first iteration
                    if not self.started or board.started:
                        board.currentCell = board.start
                        board.celllist.append(board.currentCell)
                        board.visitedCells.append(board.currentCell)
                        board.parentCells[board.currentCell] = None
                        self.started = True
                        board.started = False


                    # generic iteration
                    if(len(board.celllist)>0):
                    
                        #pop off of queue
                        board.currentCell = board.celllist.pop(0)

                        #check if goal node
                        if(board.currentCell == board.goal):
                            self.finished = True
                            board.path.append(board.goal)
                            board.backtrack = board.goal

                        #get neighbors
                        board.neighbors = board.getNeighbors(board.currentCell)

                        #calculate scores
                        for n in board.neighbors:
                            n.calculateGCost(board.currentCell)
                            n.calculateHCost(board.goal)
                            n.calculateFCost()

                        #sort neighbors considering heuristic
                        board.neighbors.sort(key=lambda x: x.fcost, reverse=False)

                        print(len(board.neighbors))
                        for n in board.neighbors:
                            if n not in board.visitedCells:
                                board.celllist.append(n)
                                board.parentCells[n] = board.currentCell
                                board.visitedCells.append(n)

                    else:
                        print("no possible path")

                

                else:
                    #clear neighbors
                    board.neighbors = []
                    if(board.parentCells[board.backtrack] != None):
                        board.backtrack = board.parentCells[board.backtrack]
                        board.path.append(board.backtrack)
                    else:
                        self.complete = True

        return board
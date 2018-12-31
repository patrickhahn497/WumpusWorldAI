# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent


class Square:
    safe = False
    stench = False
    breeze = False
    glitter = False
    bump = False
    scream = False
    visited = False
    prev = 'N'
    safesplit = set()
    gold = False
    wumpus = False
    pit = False


class MyAI(Agent):
    maxn = 7
    maxm = 7
    map = [[Square()] * 7] * 7

    directions = ['R', 'D', 'L', 'U']
    dindex = 0
    direction = 'R'
    n = 0
    m = 0
    ammo = True
    goldfound = False
    wumpusfound = False
    wumpusalive = True
    lastaction = ""
    actions = []
    leftcount = 0
    movecounter = 0

    getout = False
    # this flag is raised whenever there's no more safe spaces to go to
    # or when the gold is found

    vcount = 0

    # we use the number of pits already discovered to find out the probability another square is a pit
    # pitprob starts at .2 and decreases as we discover more and more pits
    # pitprob also changes based on
    # we can only be completely sure for the denominator for
    pitnumber = 0
    pitprob = .2

    # contains a list of the spaces where it's safe to go into
    safespaces = set()
    safecounter = 0
    # contains a list of spaces where we're not too sure about
    unsure = set()

    def __init__(self):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        pass
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def inBounds(self, chosenN, chosenM):
        if chosenN <= self.maxn and chosenN >= 0 and chosenM <= self.maxm and chosenM >= 0:
            return True
        return False

    def rotate(self, direction):
        if direction == 'L':
            newdindex = (self.dindex - 1) % 4
            self.direction = self.directions[newdindex]
            self.dindex = newdindex
        elif direction == 'R':
            newdindex = (self.dindex + 1) % 4
            self.direction = self.directions[newdindex]
            self.dindex = newdindex

    def GoForward(self):
        n = self.n
        m = self.m
        if self.direction == 'U':
            if self.inBounds(n, m + 1):
                self.m += 1
        elif self.direction == 'R':
            if self.inBounds(n + 1, m):
                self.n += 1
        elif self.direction == 'L':
            if self.inBounds(n - 1, m):
                self.n -= 1
        elif self.direction == 'D':
            if self.inBounds(n, m - 1):
                self.m -= 1

    def PerformAction(self, dir):
        if dir == 'U':
            self.UpActions()
        if dir == 'D':
            self.DownActions()
        elif dir == 'L':
            self.LeftActions()
        elif dir == 'R':
            self.RightActions()
        # elif dir=='F':
        #     self.GoForward()
        # self.actions.append(Agent.Action.FORWARD)

    def UpActions(self):
        if self.direction == 'D':
            self.actions += ['R', 'R', 'F']
        elif self.direction == 'L':
            self.actions += ['R', 'F']
        elif self.direction == 'R':
            self.actions += ['L', 'F']
        if self.direction == 'U':
            self.actions.append('F')

    def DownActions(self):
        if self.direction == 'U':
            self.actions += ['R', 'R', 'F']
        elif self.direction == 'R':
            self.actions += ['R', 'F']
        elif self.direction == 'L':
            self.actions += ['L', 'F']
        else:
            self.actions.append('F')

    def RightActions(self):
        """Adds the actions necessary to go to the right square"""
        if self.direction == 'U':
            self.actions += ['R', 'F']
        elif self.direction == 'L':
            self.actions += ['R', 'R', 'F']
        elif self.direction == 'D':
            self.actions += ['L', 'F']
        else:
            self.actions.append('F')

    def LeftActions(self):
        """Adds the actions necessary to go to the left square"""
        if self.direction == 'D':
            self.actions += ['R', 'F']
        elif self.direction == 'R':
            self.actions += ['R', 'R', 'F']
        elif self.direction == 'U':
            self.actions += ['L', 'F']
        elif self.direction == 'L':
            self.actions.append('F')

    def TurnLeftSimple(self):
        self.actions.append('R')
        self.actions.append('R')

    def getOpposite(self):
        return self.directions[self.dindex + 2 % 4]

    def makemove(self):
        """this is only called when there are actions in the action list
        it takes the first item out of the list, makes the appropriate alterations, then changes it"""
        # print("RAGGGGGGGG")
        next = self.actions.pop(0)
        # print("GRAHHHHH")
        if next == 'R':
            # print("the move is 'RIGHT")
            self.rotate('R')
            return Agent.Action.TURN_RIGHT
        elif next == 'F':
            # print("WE GO FORWARD")
            self.GoForward()
            return Agent.Action.FORWARD
        elif next == 'L':
            # print("GOing left")
            self.rotate('L')
            return Agent.Action.TURN_LEFT
        elif next == 'S':
            return Agent.Action.SHOOT

    def addSafeSpaces(self):
        """if you are on a provably safe square, then all valid adjacent tiles will be added
        maybe add variation where this is only for when the square is completely empty
        because this only works when the square is completely empty
        this will basically only be used in the beginning then"""

        if self.inBounds(self.n, self.m + 1):
            # self.safespaces.add((self.n, self.m + 1))
            self.safecounter += 1
            self.map[self.n][self.m].safesplit.add('U')
        if self.inBounds(self.n, self.m - 1):
            # self.safespaces.add((self.n, self.m - 1))
            self.safecounter += 1
            self.map[self.n][self.m].safesplit.add('D')
        if self.inBounds(self.n + 1, self.m):
            # self.safespaces.add((self.n + 1, self.m))
            self.safecounter += 1
            self.map[self.n][self.m].safesplit.add('R')

        if self.inBounds(self.n - 1, self.m):
            # self.safespaces.add((self.n - 1, self.m))
            self.safecounter += 1
            self.map[self.n][self.m].safesplit.add('L')

    def makeSafe(self, chosenN, chosenM):
        """marks a square as safe
        this is only used for unvisited squares because if you tried to mark a visited square and it turned out to be dangerous,
        you would already be dead"""
        if not self.visited(chosenN, chosenM):
            self.map[chosenN][chosenM].safe = True
            self.safecounter += 1

    def reverseVar(self):
        """called when bump is detected
        places the state marker back to the previous tile"""
        if self.direction == 'D':
            self.m += 1
            self.maxm = self.m
        elif self.direction == 'L':
            self.n += 1
            self.maxn = self.n
        elif self.direction == 'R':
            self.n -= 1
        elif self.direction == 'U':
            self.m -= 1

    def makeWumpus(self, n, m):
        self.map[n][m] = True





    def visited(self, chosenN, chosenM):
        return self.map[chosenN][chosenM].visited

    def visit(self, chosenN, chosenM):
        self.map[chosenN][chosenM].visited = True
        # print("visit1")
        self.map[chosenN][chosenM].prev = self.getOpposite()
        # print("visit2")
        self.CornerCheck2(chosenN, chosenM)
        # print("visit3")

    def getOpposite(self):

        return self.directions[(self.dindex + 2) % 4]

    def diagCheck(self, chosenN, chosenM, nmod, mmod, nadj, madj):
        """this compares a single tile with a single diagonal then amkes the appropriate adjustments"""
        # print("diag1")
        validdiag = self.inBounds(chosenN + nmod, chosenM + mmod)
        tempspace = self.map[chosenN][chosenM]
        newn = chosenN + nmod
        newm = chosenM + mmod
        # print("diag2")
        if validdiag and self.visited(newn, newm):
            diagspace = self.map[newn][newm]
            # the stench marks a square if the wumpus is still alive
            if not ((diagspace.breeze and tempspace.breeze) or (
                    diagspace.stench and tempspace.stench and self.wumpusalive)):
                if not self.visited(chosenN, newm):
                    self.makeSafe(chosenN, newm)
                    self.map[chosenN][chosenM].safesplit.add(nadj)
                if not self.visited(newn, chosenM):
                    self.makeSafe(newn, chosenM)
                    self.map[chosenN][chosenM].safesplit.add(madj)
            else:
                if (diagspace.breeze and tempspace.breeze):
                    if not self.visited(chosenN, newm):
                        self.makePit(chosenN, newm)
                    if not self.visited(newn, chosenM):
                        self.makePit(newn, chosenM)
                elif (diagspace.stench and tempspace.stench and self.wumpusalive == True):
                    # it only goes in here if the wumpus is still alive
                    if not self.visited(chosenN, newm):
                        self.makeWumpus(chosenN, newm)
                        # make an action to turn towards wumpus and kill it
                    if not self.visited(newn, chosenM):
                        self.makeWumpus(newn, chosenM)

    def CornerCheck2(self, chosenN, chosenM):
        """checks which diagonal squares are inbound and visited
        it then compares valid diagonals to itself in order to
        the weakness of corner check is that there are cases when just because the corners are breezes, doesn't mean
        that the square you marked is a pit. it can be a breeze because of another square
        we can ignore this for now but address it by the smart ai

        """
        # print("corner1")
        rightup = self.inBounds(chosenN + 1, chosenM + 1)
        rightdown = self.inBounds(chosenN + 1, chosenM - 1)
        leftup = self.inBounds(chosenN - 1, chosenM + 1)
        leftdown = self.inBounds(chosenN - 1, chosenM - 1)
        # print("corner2")
        if rightup:
            #  print("corner3")
            if self.visited(chosenN + 1, chosenM + 1):
                #  print("corner3.5")
                self.diagCheck(chosenN, chosenM, 1, 1, 'R', 'U')
            # print("corner3.6")
        if rightdown:
            # print("corner4")
            if self.visited(chosenN + 1, chosenM - 1):
                self.diagCheck(chosenN, chosenM, 1, -1, 'R', 'D')
        if leftup:
            # print("corner5")
            if self.visited(chosenN - 1, chosenM + 1):
                self.diagCheck(chosenN, chosenM, -1, 1, 'L', 'U')
        if leftdown:
            # print("corner6")
            if self.visited(chosenN - 1, chosenM - 1):
                self.diagCheck(chosenN, chosenM, -1, -1, 'L', 'D')

    # testindex = 0
    # testactions = [Agent.Action.TURN_RIGHT, Agent.TURN_RIGHT, Agent.TURN_RIGHT, Agent.TURN_RIGHT, Agent.TURN_LEFT]
    #

    def addSafeSpaces(self):
        """if you are on a provably safe square, then all valid adjacent tiles will be added
        maybe add variation where this is only for when the square is completely empty
        because this only works when the square is completely empty
        this will basically only be used in the beginning then"""
        if self.inBounds(self.n + 1, self.m) and not self.visited(self.n + 1, self.m):
            # self.safespaces.add((self.n + 1, self.m))
            self.safecounter += 1
            self.map[self.n][self.m].safesplit.add('R')
        if self.inBounds(self.n - 1, self.m) and not self.visited(self.n - 1, self.m):
            # self.safespaces.add((self.n - 1, self.m))
            self.safecounter += 1
            self.map[self.n][self.m].safesplit.add('L')
        if self.inBounds(self.n, self.m + 1) and not self.visited(self.n, self.m + 1):
            # self.safespaces.add((self.n, self.m + 1))
            self.safecounter += 1
            self.map[self.n][self.m].safesplit.add('U')
        if self.inBounds(self.n, self.m - 1) and not self.visited(self.n, self.m - 1):
            # self.safespaces.add((self.n, self.m - 1))
            self.safecounter += 1
            self.map[self.n][self.m].safesplit.add('D')

    # each action is a boolean
    def getAction(self, stench, breeze, glitter, bump, scream):

        print("NO MATTER WHAT")
        print(" CURRENT N is" + str(self.n))
        print(" CURRENT M is" + str(self.m))
        if bump:
            # we implement the -=1 because we previously went one square too far whenever we bumped
            print("ideally get inside here")
            if self.direction == 'R':
                self.n -= 1
                self.maxn = self.n
            elif self.direction == 'U':
                self.m -= 1
                self.maxm = self.m
            if self.map[self.n][self.m].safesplit:
                tempsafe = self.map[self.n][self.m].safesplit.pop()
            else:
                tempsafe = self.map[self.n][self.m].prev
                print("the previous item is " + tempsafe)
            self.PerformAction(tempsafe)
            return self.makemove()

        if not bump:
            tempsquare = self.map[self.n][self.m]
            visited = self.visited(self.n, self.m)
            print(self.map[self.n][self.m].safesplit)

        if self.getout and self.n == 0 and self.m == 0:
            return Agent.Action.CLIMB
        print("marker1")
        if self.actions:
            return self.makemove()
        print("marker2")
        if self.getout:
            print("needs to get out")
            self.PerformAction(tempsquare.prev)
            print("that is triggered")
        print("marker3")
        # print("wow2")

        # print("wow3")
        if not (stench or breeze or glitter or bump or scream):
            print("gone in here")
            if not visited:
                print("visited here")
                self.addSafeSpaces()
                self.visit(self.n, self.m)
            if self.map[self.n][self.m].safesplit:
                print("mapper")
                tempsafe = self.map[self.n][self.m].safesplit.pop()
                print("mapper2")
                print(tempsafe)
                self.PerformAction(tempsafe)
                return self.makemove()
            else:
                if self.n == 0 and self.m == 0:
                    return Agent.Action.CLIMB
                print("leftover")
                self.PerformAction(self.map[self.n][self.m].prev)
                return self.makemove()
        # for the next step, replace goforward with safesplit.pop
        # if self.map[self.n][self.m].safesplit:
        #     self.PerformAction(self.map[self.n][self.m].safesplit.pop(0))
        #     return self.makemove()

        # print("wow4")
        if glitter and not self.goldfound:
            self.getout = True
            self.PerformAction(tempsquare.prev)
            self.goldfound = True
            return Agent.Action.GRAB
        # print("wow5")
        elif (stench or breeze or bump or scream):
            print("your danger sense is tingling")
            if self.n == 0 and self.m == 0:
                return Agent.Action.CLIMB
            else:
                self.getout = True
            print("bmuparoo gets triggered here")
            self.PerformAction(self.map[self.n][self.m].prev)
            print("all is done")
        if self.actions:
            return self.makemove()

        # if not (stench or breeze) and self.movecounter==0:
        #     self.movecounter+=1
        #     self.GoForward()
        #     return Agent.Action.FORWARD
        # if (self.movecounter>=1 or breeze or stench):
        #     self.getout = True
        #     if self.m == 0 and self.n == 0:
        #         # print("we are already at the origin so we just climb")
        #         return Agent.Action.CLIMB
        #     else:
        #         if self.leftcount<2:
        #             self.leftcount+=1
        #             self.rotate('R')
        #             return Agent.Action.TURN_RIGHT
        #         else:
        #             self.GoForward()
        #             return Agent.Action.FORWARD
        # if self.getout and self.m == 0 and self.n == 0:
        #     return Agent.Action.CLIMB

        # if (stench or breeze):
        #    # print("BADNESS DETECTED")
        #     if not self.getout:
        #        # print("Time to head back")
        #         self.getout=True
        #         if self.m==0 and self.n==0:
        #             #print("we are already at the origin so we just climb")
        #             return Agent.Action.CLIMB
        #         else:
        #             #print("otherwise we turn left then keep making moves")
        #             self.leftcount+=1
        #             self.rotate('R')
        #             return Agent.Action.TURN_RIGHT
        #     else:
        #
        #         #print("we arleady know to get out")
        #         if self.leftcount<2:
        #             self.rotate('R')
        #             self.leftcount+=1
        #             return Agent.Action.TURN_RIGHT
        #         else:
        #             self.GoForward()
        #             return Agent.Action.FORWARD
        # else:
        #     #this should only activate on rotates
        #     print("we arleady know to get out")
        #     if self.m==0 and self.n==0:
        #         print("we have arrived at origin xo we climb out")
        #         return Agent.Action.CLIMB
        #     else:
        #         print("we simply move forward then but add it to the queue of course")
        #         self.actions.append(Agent.Action.FORWARD)
        #         return self.makemove()
        # else:
        #
        # if self.getout:
        #     if self.m == 0 and self.n == 0:
        #         return Agent.Action.CLIMB
        #     else:
        #         self.GoForward()
        #         return Agent.Action.FORWARD
        #         # self.actions.append(Agent.Action.FORWARD)
        #         # return self.makemove()
        # else:
        #     self.GoForward()
        #     return Agent.Action.FORWARD

        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================

        # return Agent.Action.CLIMB
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================

    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
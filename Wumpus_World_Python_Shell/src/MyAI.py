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
    n = -1
    m = -1
    safe = False
    stench = False
    breeze = False
    glitter = False
    bump = False
    scream = False
    visited = False
    visit2 = False
    prev = 'N'
    safesplit = set()
    allsafespaces = set()
    gold = False
    wumpus = False
    pit = False
    message = "wassup"
    movecounter=0

    def __init__(self, n=-1, m=-1):
        self.n = n
        self.m = m

    def set(self, n, m):
        self.n = n
        self.m = m

    def diagnostic(self):
        print(" ")
        print("COORDINATES are : " + str(self.n) + ", " + str(self.m))
        print("VISITED STATUS is " + str(self.visited))
        print("SAFE STATUS is " + str(self.safe))
        print("PREVIOUS TILE is " + self.prev)
        print("REMAINING SAFE SPACES: " + str(self.safesplit))
        print("ALL REGISTERED SAFE SPACES: " + str(self.allsafespaces))
        print("breeze status is : " + str(self.breeze))
        print(self.message)
        print(" ")


class MyAI(Agent):
    maxn = 6
    maxm = 6
    # map = [[Square()] * 7] * 7
    map = [[Square() for i in range(7)] for i in range(7)]

    directions = ['R', 'D', 'L', 'U']
    dindex = 0
    direction = 'R'
    n = 0
    m = 0
    ammo = True
    goldfound = False
    wumpusfound = False
    wumpusalive = True
    facingwumpus = False
    wumpusadj = False
    wumpusdirection = 'N'





    wn= -1
    wm = -1
    lastaction = ""
    actions = []
    leftcount = 0
    movecounter = 0
    vlist = []
    pathback = []
    treadpath = []
    bestpath = 9999

    getout = False
    pathestablished = False
    goback = False
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
    safespaces =  [] # set()
    safecounter = 0
    # contains a list of spaces where we're not too sure about
    unsure = set()

    def __init__(self):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        for n in range(7):
            for m in range(7):
                # tempo = Square()
                #self.map[n][m] = Square(n, m)
                self.map[n][m].set(n, m)
                self.unvisitUnsafe(n, m)
        self.vlist = []
        self.safespaces = []
        self.dindex = 0
        direction = 'R'
        self.n = 0
        self.m = 0
        self.ammo = True
        self.goldfound = False
        self.wumpusfound = False
        self.wumpusalive = True
        self.facingwumpus = False
        self.wumpusadj = False
        self.wumpusdirection = 'N'
        self.pathestablished = False
        self.wn = -1
        self.wm = -1
        self.lastaction = ""
        self.actions = []
        self.leftcount = 0
        self.movecounter = 0
        self.vlist = []
        self.pathback = []
        self.treadpath = [(99, 99)]

        self.getout = False
        self.goback = False

        pass
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def diagnostics(self):
        print(" ")
        for n in range(7):
            for m in range(7):
                if self.map[n][m].visited:
                    self.map[n][m].diagnostic()
        print(" ")

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


    def minTuple(self, path):
        '''returns a tuple of the (best direction to go, index of shortest path) '''
        mintup = (-1,-1)
        minval = 9999
        for num, val in enumerate(path):
            if val[0] < minval:
                minval = val[0]
                mintup = val[1]
        return (minval, mintup)
   # return (minval, [mintup] + path)

    def heureval(self, valids):
        ''' valids is a list of coordinates'''
        minval = 9999
        minN = 99
        minM = 99
        listo = []
        for n, m in valids:
            if n+m <minval:
                minval = n+m
                minN = n
                minM = m
                listo.append((n,m))
            elif n+m ==minval:
                listo.append((n,m))
        # return (minval, (minN, minM))
        return (minval, listo)

    def shortestHelper(self, n, m, depth, path):
       # print("i am inside of the shortest helper now")
        if not self.visited(n, m):
            #print(" ONE ")
            if (n, m) not in self.safespaces: #this means that the space either hasnt been explored or has been deemed unsafe
                #print(" TWO")
                return (9999, path)
        if n ==0  and m==0:
            return (depth, path)
        valids = self.backtrackValids(n, m, path)
        if valids:
            if (0,0) in valids:
                return (0, (0,0))
            return self.minTuple([self.shortestHelper(x[0], x[1], depth+1, path+[x]) for x in valids])
        else:
            return (9999, path)

    def heurHelper(self, n, m, depth, path):
        if not self.visited(n, m):
            #print(" ONE ")
            if (n, m) not in self.safespaces: #this means that the space either hasnt been explored or has been deemed unsafe
                return (9999, path)
        if n == 0 and m == 0:
            return (depth, path)
        valids = self.backtrackValids(n, m, path)
        if valids:
            heurvalids =  self.heureval(valids)[1] #you want to make sure that the path goes into the chosen heuristic function
            return self.minTuple([self.heurHelper(x[0], x[1], depth+1, path+[x]) for x in heurvalids])
        else:
            return (9999, path)




    def backtrackValids(self, n, m, path):
        '''make sure to store the current path'''
        valids = []
       # print("attempting to find valids")
        if self.inBounds(n + 1, m):
            if (self.visited(n + 1, m) or (n+1, m) in self.safespaces) and (n+1, m) not in path:
                valids.append((n+1,m))
        if self.inBounds(n - 1, m):
            if (self.visited(n - 1, m) or (n-1, m) in self.safespaces) and (n-1, m) not in path:
                valids.append((n - 1, m))
        if self.inBounds(n, m+1):
            if (self.visited(n, m+1) or (n, m+1) in self.safespaces) and (n, m+1) not in path:
                valids.append((n, m+1))
        if self.inBounds(n, m-1):
            if (self.visited(n, m-1) or (n, m-1) in self.safespaces) and (n, m-1) not in path:
                valids.append((n, m-1))
       # print("found the valids")
        return valids


    def shortestPath(self, n, m):
        '''this is only called once the getout functionality has been triggered'''
        #print("now attempting to find the shortest path")
        valids = self.backtrackValids(n, m, [])
        if valids:
            return self.minTuple([self.shortestHelper(x[0], x[1], 1, [x]) for x in valids])
        else:
            return (0, [])



    def heuristicSearch(self, n, m):
        '''searches for which valid square will give you the best value
        utilizes pruning so that if a certain move will take you further away, it does not do it'''
        #print("im going in")
        valids = self.backtrackValids(n, m, [])
        if valids:
            return self.minTuple([self.heurHelper(x[0], x[1], 1, [x]) for x in valids])
        return (0, [])

    def GoForward(self):
        # so for when im accounting for the bump, I'll have it so that the maxn and maxm is 6
        n = self.n
        m = self.m
        visited = False
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
        elif dir=='S':
            self.actions.append('S')

    def UpActions(self):
        if self.direction == 'D':
            self.actions.append('R')
        elif self.direction == 'L':
            self.actions.append('R')
        elif self.direction == 'R':
            self.actions.append('L')
        if self.direction == 'U':
            self.actions.append('F')

    def DownActions(self):
        if self.direction == 'U':
            self.actions.append('R')
        elif self.direction == 'R':
            self.actions.append('R')
        elif self.direction == 'L':
            self.actions.append('L')
        else:
            self.actions.append('F')

    def RightActions(self):
        """Adds the actions necessary to go to the right square"""
        if self.direction == 'U':
            self.actions.append('R')
        elif self.direction == 'L':
            self.actions.append('R')
        elif self.direction == 'D':
            self.actions.append('L')
        else:
            self.actions.append('F')

    def LeftActions(self):
        """Adds the actions necessary to go to the left square"""
        if self.direction == 'D':
            self.actions.append('R')
        elif self.direction == 'R':
            self.actions.append('R')
        elif self.direction == 'U':
            self.actions.append('L')
        elif self.direction == 'L':
            self.actions.append('F')

    def TurnLeftSimple(self):
        self.actions.append('R')
        self.actions.append('R')

    def coordToDir(self, n, m, newn, newm):
        if newn!=n:
            if newn>n:
                return 'R'
            else:
                return 'L'
        if newm!=m:
            if newm>m:
                return 'U'
            else:
                return 'D'

    def getOpposite(self):
        return self.directions[(self.dindex + 2) % 4]

    def makemove(self):
        """this is only called when there are actions in the action list
        it takes the first item out of the list, makes the appropriate alterations, then changes it"""
        next = self.actions.pop(0)
        if next == 'R':
            self.rotate('R')
            return Agent.Action.TURN_RIGHT
        elif next == 'F':
            self.GoForward()
            return Agent.Action.FORWARD
        elif next == 'L':
            self.rotate('L')
            return Agent.Action.TURN_LEFT
        elif next == 'S':
            return Agent.Action.SHOOT


    def makeSafe(self, chosenN, chosenM):
        """marks a square as safe
        this is only used for unvisited squares because if you tried to mark a visited square and it turned out to be dangerous,
        you would already be dead"""
        if not self.visited(chosenN, chosenM):
            self.map[chosenN][chosenM].safe = True
            self.safecounter += 1
            self.safespaces.add((chosenN, chosenM))

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
        if not self.wumpusfound:
            self.map[n][m].wumpus = True
            self.wumpusfound = True
            self.wn = n
            self.wm = m
            # print("THERE IS A WUMPUS AT " + str(n) + ", " + str(m))

    def wumpusAdj(self):
        """this checks if the wumpus is adjacent"""
        if self.wumpusfound and self.wumpusalive:
            if (abs(self.n-self.wn) ==1 and abs(self.m-self.wm) ==0) or (abs(self.n-self.wn) ==0 and abs(self.m-self.wm) ==1):
                if self.m==self.wm:
                    if self.n==self.wn+1:
                        self.wumpusdirection="L"
                    if self.n== self.wn-1:
                        self.wumpusdirection='R'
                elif self.n==self.wn:
                    if self.m==self.wm+1:
                        self.wumpusdirection="D"
                    if self.m== self.wm-1:
                        self.wumpusdirection='U'


    def turnWumpus(self):
        """ turns in the wumpus's direction. This is only called when wumpusAdj yields true"""
        if not self.direction == self.wumpusdirection:
            # print("TURNING IN DIRECTION OF WUMPUS")
            self.PerformAction(self.wumpusdirection)
        else:
            # print("WE ARE NOW FACING THE WUMPUS! FIRE AT WILL!")
            self.facingwumpus = True
            self.PerformAction('S')
            self.ammo = False

    def postWumpus(self):
        """turns the wumpus square and all adjacent stench and non-pit squares into no safe squares
        this is only activated after the wumpus is dead"""
        wn = self.wn
        wm = self.wm
        if self.map[self.wn][self.wm].pit == False:
            self.makeSafe(self.wn, self.wm)



    def visited(self, chosenN, chosenM):
        try:
            # return self.map[chosenN][chosenM].visited
            return (chosenN, chosenM) in self.vlist
        except:
            return True

    def makePit(self, n, m):
        if not self.map[n][m].pit:
            self.map[n][m].pit = True
            self.pitnumber += 1

    def getOpposite(self):
        return self.directions[(self.dindex + 2) % 4]

    def diagCheck(self, chosenN, chosenM, nmod, mmod, nadj, madj):
        """this compares a single tile with a single diagonal then amkes the appropriate adjustments"""
        # print("diag1")
        validdiag = self.inBounds(chosenN + nmod, chosenM + mmod)
        tempspace = self.map[chosenN][chosenM]
        newn = chosenN + nmod
        newm = chosenM + mmod
        flag = 0
        if validdiag and self.visited(newn, newm):
            diagspace = self.map[newn][newm]
            # the stench marks a square if the wumpus is still alive
            if (diagspace.breeze and tempspace.breeze):
                flag+=1
                if not self.visited(chosenN, newm):
                    self.makePit(chosenN, newm)
                if not self.visited(newn, chosenM):
                    self.makePit(newn, chosenM)
            if (diagspace.stench and tempspace.stench and self.wumpusalive == True):
                flag+=1
                # it only goes in here if the wumpus is still alive
                if not self.visited(chosenN, newm):
                    self.makeWumpus(chosenN, newm)
                    # make an action to turn towards wumpus and kill it
                if not self.visited(newn, chosenM) and not self.wumpusfound:
                    self.makeWumpus(newn, chosenM)
            if flag < 1:
                if not self.visited(chosenN, newm):
                    self.makeSafe(chosenN, newm)
                if not self.visited(newn, chosenM):
                    self.makeSafe(newn, chosenM)

    def CornerCheck2(self, chosenN, chosenM):
        """checks which diagonal squares are inbound and visited
        it then compares valid diagonals to itself in order to
        the weakness of corner check is that there are cases when just because the corners are breezes, doesn't mean
        that the square you marked is a pit. it can be a breeze because of another square
        we can ignore this for now but address it by the smart ai

        """
        rightup = self.inBounds(chosenN + 1, chosenM + 1)
        rightdown = self.inBounds(chosenN + 1, chosenM - 1)
        leftup = self.inBounds(chosenN - 1, chosenM + 1)
        leftdown = self.inBounds(chosenN - 1, chosenM - 1)
        if rightup:
            if self.visited(chosenN + 1, chosenM + 1):
                self.diagCheck(chosenN, chosenM, 1, 1, 'R', 'U')
        if rightdown:
            if self.visited(chosenN + 1, chosenM - 1):
                self.diagCheck(chosenN, chosenM, 1, -1, 'R', 'D')
        if leftup:
            if self.visited(chosenN - 1, chosenM + 1):
                self.diagCheck(chosenN, chosenM, -1, 1, 'L', 'U')
        if leftdown:
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
        # print("ADDING them safespaces")
        if self.inBounds(self.n + 1, self.m)and not self.visited(self.n + 1, self.m):
            self.makeSafe(self.n + 1, self.m)
            #self.safespaces.add((self.n + 1, self.m))
        if self.inBounds(self.n - 1, self.m):
            self.makeSafe(self.n-1, self.m)
            #self.safespaces.add((self.n - 1, self.m))
        if self.inBounds(self.n, self.m + 1) and not self.visited(self.n, self.m + 1):
            self.makeSafe(self.n, self.m+1)
           # self.safespaces.add((self.n, self.m + 1))
        if self.inBounds(self.n, self.m - 1) and not self.visited(self.n, self.m - 1):
            self.makeSafe(self.n, self.m-1)
        # print("EVERYTHING DONE")
           # self.safespaces.add((self.n, self.m - 1))

    def addSafeSpacesCustom(self, chosenN, chosenM):
        """if you are on a provably safe square, then all valid adjacent tiles will be added
        maybe add variation where this is only for when the square is completely empty
        because this only works when the square is completely empty
        this will basically only be used in the beginning then"""
        # print("ADDING them safespaces")
        if self.inBounds(chosenN + 1, chosenM)and not self.visited(chosenN + 1, chosenM):
            self.makeSafe(chosenN + 1, chosenM)
            #self.safespaces.add((self.n + 1, self.m))
        if self.inBounds(chosenN - 1, chosenM):
            self.makeSafe(chosenN-1, chosenM)
            #self.safespaces.add((self.n - 1, self.m))
        if self.inBounds(chosenN, chosenM + 1) and not self.visited(chosenN, chosenM + 1):
            self.makeSafe(chosenN, chosenM+1)
           # self.safespaces.add((self.n, self.m + 1))
        if self.inBounds(chosenN, chosenM- 1) and not self.visited(chosenN, chosenM - 1):
            self.makeSafe(chosenN, chosenM-1)


    def purgeInvalids(self):
        """retroactively removes all invalid squares from safespace. Usually triggered on a bump"""
        if self.safespaces:
            self.safespaces = [x for x in self.safespaces if self.inBounds(x[0], x[1])]


    def ValidSafeSpaces2(self):
        tempsafe = []
        if not self.safespaces:
            return tempsafe
        if (self.n + 1, self.m) in self.safespaces:
            tempsafe.append('R')
        if (self.n - 1, self.m) in self.safespaces:
            tempsafe.append('L')
        if (self.n, self.m+1) in self.safespaces:
            tempsafe.append('U')
        if (self.n, self.m-1) in self.safespaces:
            tempsafe.append('D')
        return tempsafe

    def makeSafe(self, chosenN, chosenM):
        # print("making the neighborhood safe")
        self.map[chosenN][chosenM].safe = True
        if (chosenN, chosenM) not in self.vlist and (chosenN, chosenM) not in self.safespaces:
            self.safespaces.append((chosenN, chosenM))

    def unvisitUnsafe(self, n, m):
        self.map[n][m].safe = False
        self.map[n][m].visited = False

    def visit(self, chosenN, chosenM, empty):
        self.map[chosenN][chosenM].visited = True
        if empty:
            self.addSafeSpaces()
        if (chosenN, chosenM) in self.safespaces:
            self.safespaces.remove((chosenN, chosenM))
        self.vlist.append((chosenN, chosenM))
        self.map[chosenN][chosenM].prev = self.getOpposite()
        self.CornerCheck2(chosenN, chosenM)

    def setSquarePrecepts(self, stench, breeze, n, m):
        self.map[n][m].stench=stench
        self.map[n][m].breeze = breeze



    # each action is a boolean
    def getAction(self, stench, breeze, glitter, bump, scream):

        self.movecounter+=1
        tempsquare = self.map[self.n][self.m]
        if scream:
            self.wumpusalive = False
            self.postWumpus()
        if self.getout:
            if self.n == 0 and self.m == 0:
                self.getout = False
                self.goback = False
                return Agent.Action.CLIMB

            if not self.pathestablished:
                tester = self.heuristicSearch(self.n, self.m)
                self.pathback = tester[1]
                self.bestpath = tester[0]
                if self.pathback:
                    if self.pathback[0]:
                        self.pathestablished = True
            if self.pathestablished:
                if (self.n==1 and self.m==0) or (self.n==0 and self.m==1):
                    epath=(0,0)
                elif (self.n, self.m) == self.treadpath[-1] or self.treadpath[-1]==(99,99): #once you have reached tyour goal, add a new goal to treadpath
                    epath = self.pathback.pop(0)
                    self.treadpath.append(epath)
                else:
                    epath = self.treadpath[-1]
                self.PerformAction(self.coordToDir(self.n, self.m, epath[0], epath[1]))
                return self.makemove()
            self.PerformAction(self.map[self.n][self.m].prev)
            return self.makemove()
        if self.goback:
            tempspace = self.ValidSafeSpaces2()
            if tempspace and not self.getout: #if there's valid adjacent safe spaces and getout is not triggered
                self.goback = False
                self.PerformAction(tempspace.pop(0))
            elif not tempspace and self.n == 0 and self.m == 0:
                return Agent.Action.CLIMB
            else: #otherwise it backtracks
                self.PerformAction(self.map[self.n][self.m].prev)
            return self.makemove()
        elif (bump or (stench and self.wumpusalive) or breeze or glitter):
            empty = True
            if ((stench and self.wumpusalive) or breeze or bump):
                empty = False
            if bump:
                if self.direction == 'R':
                    self.n -= 1
                    self.maxn = self.n
                    self.purgeInvalids()
                elif self.direction == 'U':
                    self.m -= 1
                    self.maxm = self.m
                    self.purgeInvalids()
            if not self.visited(self.n, self.m):
                self.setSquarePrecepts(stench, breeze, self.n, self.m)
                self.visit(self.n, self.m, empty)
            if glitter and not self.goldfound:
                self.getout = True
                self.goback = True
                self.goldfound = True
                return Agent.Action.GRAB
            if ((stench and self.wumpusalive) or breeze):
                if self.n == 0 and self.m == 0:
                    return Agent.Action.CLIMB
                elif stench and self.wumpusalive and self.wumpusfound and self.ammo:
                    if self.wumpusdirection == 'N':
                        self.wumpusAdj()
                    self.turnWumpus()
                else:
                    tempspace = self.ValidSafeSpaces2()
                    if tempspace:  # adds a random
                        self.PerformAction(tempspace.pop(0))
                    else:  # if there's no valid adjacent spaces, it backtracks
                        self.goback = True
                        self.PerformAction(self.map[self.n][self.m].prev)
                    return self.makemove()
        else: #this is what happens if you're not going back or there's no precept
            if not self.visited(self.n, self.m):
                self.setSquarePrecepts(stench, breeze, self.n, self.m)
                self.visit(self.n, self.m, True)
            tempspace = self.ValidSafeSpaces2()
            if tempspace:
                self.PerformAction(tempspace.pop(0))
            else:
                if self.n == 0 and self.m == 0: #this should trigger when there's nothing to go to
                    return Agent.Action.CLIMB
                self.goback = True     #otherwise it just backtracks
                self.PerformAction(self.map[self.n][self.m].prev)
            return self.makemove()
        if self.actions:
            return self.makemove()


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
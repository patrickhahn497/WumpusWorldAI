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

    getout = False
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
        # self.map[6][0].message = "WRONG"

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
        # if not self.visited(self.n, self.m):
        #     self.visit(self.n, self.m)

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
        # elif dir=='F':
        #     self.GoForward()
        # self.actions.append(Agent.Action.FORWARD)

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
    #
    # def addSafeSpaces(self):
    #     """if you are on a provably safe square, then all valid adjacent tiles will be added
    #     maybe add variation where this is only for when the square is completely empty
    #     because this only works when the square is completely empty
    #     this will basically only be used in the beginning then"""
    #
    #     if self.inBounds(self.n, self.m + 1):
    #         # self.safespaces.add((self.n, self.m + 1))
    #         self.safecounter += 1
    #         self.map[self.n][self.m].safesplit.add('U')
    #         self.map[self.n][self.m].allsafespaces.add('U')
    #     if self.inBounds(self.n, self.m - 1):
    #         # self.safespaces.add((self.n, self.m - 1))
    #         self.safecounter += 1
    #         self.map[self.n][self.m].safesplit.add('D')
    #         self.map[self.n][self.m].allsafespaces.add('D')
    #     if self.inBounds(self.n + 1, self.m):
    #         # self.safespaces.add((self.n + 1, self.m))
    #         self.safecounter += 1
    #         self.map[self.n][self.m].safesplit.add('R')
    #         self.map[self.n][self.m].allsafespaces.add('R')
    #
    #     if self.inBounds(self.n - 1, self.m):
    #         # self.safespaces.add((self.n - 1, self.m))
    #         self.safecounter += 1
    #         self.map[self.n][self.m].safesplit.add('L')
    #         self.map[self.n][self.m].allsafespaces.add('L')

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
            #     return True
            # else:
            #     return False

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
        # rightup = self.inBounds(chosenN + 1, chosenM + 1)
        # rightdown = self.inBounds(chosenN + 1, chosenM - 1)
        # leftup = self.inBounds(chosenN - 1, chosenM + 1)
        # leftdown = self.inBounds(chosenN - 1, chosenM - 1)





    def visited(self, chosenN, chosenM):
        try:
            return self.map[chosenN][chosenM].visited
        except:
            return True

    def makePit(self, n, m):
        if not self.map[n][m].pit:
            self.map[n][m].pit = True
            self.pitnumber += 1
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
        flag = 0
        # print("diag2")
        if validdiag and self.visited(newn, newm):
           # print("     BEFORE teh change are " + str(self.safespaces))
            diagspace = self.map[newn][newm]
            # the stench marks a square if the wumpus is still alive
            #print("tempspace breeze is " + str(tempspace.breeze))
            #print("diagspace breeze is " + str(diagspace.breeze))
            if (diagspace.breeze and tempspace.breeze):
               # print("found the breezarino")
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
               # print("             i fucking found you")
                if not self.visited(chosenN, newm):
                   # print("went inside here")
                    self.makeSafe(chosenN, newm)
                    # self.map[chosenN][chosenM].safesplit.add(nadj)
                    # self.map[chosenN][chosenM].allsafespaces.add(nadj)
                if not self.visited(newn, chosenM):
                   # print("went inside here 2")
                    self.makeSafe(newn, chosenM)
                    # self.map[chosenN][chosenM].safesplit.add(madj)
                    # self.map[chosenN][chosenM].allsafespaces.add(madj)

           # print("     AFTER teh change are " + str(self.safespaces))

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


    def purgeInvalids(self):
        """retroactively removes all invalid squares from safespace. Usually triggered on a bump"""
        if self.safespaces:
            self.safespaces = [x for x in self.safespaces if self.inBounds(x[0], x[1])]



    # def ValidSafeSpaces(self):
    #     tempsafe = []
    #     if (self.n + 1, self.m) in self.safespaces:
    #         tempsafe.append((self.n + 1, self.m))
    #     if (self.n - 1, self.m) in self.safespaces:
    #         tempsafe.append((self.n - 1, self.m))
    #     if (self.n, self.m+1) in self.safespaces:
    #         tempsafe.append((self.n, self.m+1))
    #     if (self.n, self.m-1) in self.safespaces:
    #         tempsafe.append((self.n, self.m-1))
    #     return tempsafe
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
            # print("adding savior " + str((chosenN, chosenM)))
            self.safespaces.append((chosenN, chosenM))
            # if chosenM==1 and chosenN==3:
            #     print("what the fuck are you doing")
            #     self.map[3][1].diagnostic()
            #     self.safespaces.append((3, 1))
            # try:
            #     self.safespaces.add((chosenN, chosenM))
            # except ValueError:
            #     print("value error")
            # except:
            #     print("elser")
        #
        #     print("savior added")
        # print("this the updated safe spaces: "+str(self.safespaces))

    def visit(self, chosenN, chosenM, empty):
        #print(" start of visit")
        self.map[chosenN][chosenM].visited = True
        # print("checking for safespaces")
        #not every visited square should have safespaces added
        if empty:
            self.addSafeSpaces()
        if (chosenN, chosenM) in self.safespaces:
           # print("removing prompt from safespace")
            self.safespaces.remove((chosenN, chosenM))
        #print("about to add to visit list")
        self.vlist.append((chosenN, chosenM))
       # print("finish2")
        self.map[chosenN][chosenM].prev = self.getOpposite()
        self.CornerCheck2(chosenN, chosenM)

    def setSquarePrecepts(self, stench, breeze, n, m):
        self.map[n][m].stench=stench
        self.map[n][m].breeze = breeze



    # each action is a boolean
    def getAction(self, stench, breeze, glitter, bump, scream):

        # print(" CURRENT N is" + str(self.n))
        # print(" CURRENT M is" + str(self.m))
        # print("CURRENT DIRECTION IS " + self.direction)
        tempsquare = self.map[self.n][self.m]
        empty = True
        # self.diagnostics()
        # print("safe spaces are " + str(self.safespaces))
        # print("visited spaces are " + str(self.vlist))


        # print("yessir")
        #this snippet should ideally handle backtracking
        if scream:
            self.wumpusalive=False
            # print("THE WUMPUS IS SLAIN")
            """turn all wumpus related squares to safe as long as there's breeze or pit in them"""
        if ((stench and self.wumpusalive) or breeze or bump):
            empty = False
        if bump:
            # print("BUMPED HERE")
            if self.direction == 'R':
                self.n -= 1
                self.maxn = self.n
                self.purgeInvalids()
            elif self.direction == 'U':
                self.m -= 1
                self.maxm = self.m
                self.purgeInvalids()
        # print("WHY")

        if not self.visited(self.n, self.m):
            # print("attempt to visit")
            self.setSquarePrecepts(stench, breeze, self.n, self.m)
            # print("precepts set")
            self.visit(self.n, self.m, empty)

        # if (self.n == 3 and self.m == 2):
        #     self.setSquarePrecepts(stench, breeze, self.n, self.m)
        #     self.map[3][2].diagnostic()

        #     print("visit finished")
        # print("wassuh")
        # print("previous square is " + tempsquare.prev)
        # print("diagnostic complete")
        if self.goback:
            # print("BECAUSE OF BACKTRACK")
            #this just goes back
            if self.getout:
                if self.n == 0 and self.m == 0:
                    self.getout = False
                    self.goback=False
                    return Agent.Action.CLIMB
            tempspace = self.ValidSafeSpaces2()
            if tempspace and not self.getout: #if there's valid adjacent safe spaces and getout is not triggered
                self.goback = False
                self.PerformAction(tempspace.pop(0))
            elif not tempspace and self.n == 0 and self.m == 0:
                return Agent.Action.CLIMB
            else:
                self.PerformAction(self.map[self.n][self.m].prev)
            return self.makemove()
        if glitter and not self.goldfound:
            self.getout = True
            self.goback = True
            #self.PerformAction(tempsquare.prev)
            self.goldfound = True
            return Agent.Action.GRAB
        elif ((stench and self.wumpusalive) or breeze or scream):
            # print("HAZARD")
            if self.n == 0 and self.m == 0:
                return Agent.Action.CLIMB
            elif stench and self.wumpusalive and self.wumpusfound and self.ammo:
                # print("THE WUMPUS IS NEXT TO US")
                if self.wumpusdirection=='N':
                    self.wumpusAdj()
                    # print("THE WUMPUS IS TO THE DIRECTION: "+self.wumpusdirection )
                self.turnWumpus()
            else:
                #account for bumps in here
                # if stench and self.wumpusfound:



                #checks how many valid adjacent spaces there are
                #self.diagnostics()
                tempspace = self.ValidSafeSpaces2()
                if len(tempspace) > 0: #adds a random
                    #the problem with this is that since a random action is popped, it might not always give you the one you want
                        #but according to the function, the same item should be on the first of the queue each time
                   # print("but there's a temporary solution which is "+ str(tempspace))

                    self.PerformAction(tempspace.pop(0))
                else:#if there's no valid adjacent spaces, it backtracks
                    # print("it's gonna go back home")
                    self.goback = True
                    self.PerformAction(self.map[self.n][self.m].prev)
           # print("all is done")
        else:
         #   print("elser")
            tempspace = self.ValidSafeSpaces2()
            if tempspace:
                self.PerformAction(tempspace.pop(0))
            else:
                if self.n == 0 and self.m == 0:
                    return Agent.Action.CLIMB
                self.goback = True
                self.PerformAction(self.map[self.n][self.m].prev)
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
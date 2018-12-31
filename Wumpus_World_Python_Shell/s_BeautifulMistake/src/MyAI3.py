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

#we can also
class Square:
    safe = False
    stench = False
    breeze = False
    glitter = False
    bump = False
    scream = False
    visited = False
    #0 is for when we don't know if the item is in
    #1 is for when we know the item is in there
    #2 is for when we suspect an item might be in there but we don't know
    prev = 'N'
    #prev allows us to see where the previous tile was. this goes all the way to the origin
    safesplit = set()
    #if a space has more than one safe neighbor, it will add in here
    #if a safe neighbor is chosen, that item will be removed form safesplit

    #we can also keep a variable of how far the path is so once a better path is found, we can replace it

    #or alternate system, we can add 1 each time we suspect something to be something
    #that way, we can simply do gold >=2 if we want to confirm the presence of something
    gold = False
    wumpus = False
    pit = False

class MyAI ( Agent ):
    # map =  [[[]]*7]*4
    map = [[Square()]*7]*7
    # n = column number. we are trying to plot out the bounds
    maxn = 7
    #m = row number
    maxm = 7

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

    getout = False
    #this flag is raised whenever there's no more safe spaces to go to
    #or when the gold is found

    vcount = 0

    #we use the number of pits already discovered to find out the probability another square is a pit
    #pitprob starts at .2 and decreases as we discover more and more pits
    #pitprob also changes based on
    #we can only be completely sure for the denominator for
    pitnumber = 0
    pitprob = .2


    #contains a list of the spaces where it's safe to go into
    safespaces = set()
    safecounter = 0
    #contains a list of spaces where we're not too sure about
    unsure = set()

    actions = []



    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        self.map[0][0].prev="out"
        pass
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================


    def inBounds(self, chosenN, chosenM):
        if chosenN <= self.maxn and chosenN >=0 and chosenM <=self.maxm and chosenM >= 0:
            return True
        return False

    def visited(self, chosenN, chosenM):
        return self.map[chosenN][chosenM].visited

    def visit(self, chosenN, chosenM):
        self.map[chosenN][chosenM].visited = True
        self.vcount+=1
        self.map[chosenN][chosenM].prev = self.getOpposite()
        self.CornerCheck2(chosenN, chosenM)
        #include a line where you perform crosscheck

    def makeSafe(self, chosenN, chosenM):
        """marks a square as safe
        this is only used for unvisited squares because if you tried to mark a visited square and it turned out to be dangerous,
        you would already be dead"""
        if not self.visited(chosenN, chosenM):
            self.map[chosenN][chosenM].safe = True
            self.safecounter += 1


    def diagCheck(self, chosenN, chosenM, nmod, mmod, nadj, madj):
        """this compares a single tile with a single diagonal then amkes the appropriate adjustments"""
        validdiag = self.inBounds(chosenN+nmod, chosenM+mmod)
        tempspace = self.ChosenSquare(chosenN, chosenM)
        newn=chosenN+nmod
        newm = chosenM+mmod
        if validdiag and self.visited(newn, newm):
            diagspace = self.map[newn][newm]
            #the stench marks a square if the wumpus is still alive
            if not ((diagspace.breeze and tempspace.breeze) or (diagspace.stench and tempspace.stench and self.wumpusalive)):
                if not self.visited(chosenN, newm):
                    #see reasoning in makeSafe function
                    self.makeSafe(chosenN, newm)
                    self.map[chosenN][chosenM].safesplit.add(nadj)
                    # self.map[chosenN][chosenM].safesplit.append(adj1)
                if not self.visited(newn, chosenM):
                    self.makeSafe(newn, chosenM)
                    self.map[chosenN][chosenM].safesplit.add(madj)
                    # self.map[chosenN][chosenM].safesplit.append(adj2)
            else:
                if (diagspace.breeze and tempspace.breeze):
                    """this is because if the tile was already visited, then we know for sure it is not a pit
                    it is not possible for there have to been a pit and have it be visited
                    because if it had, then agent would already have died"""
                    if not self.visited(chosenN, newm):
                        self.makePit(chosenN, newm)
                    if not self.visited(newn, chosenM):
                        self.makePit(newn, chosenM)
                elif (diagspace.stench and tempspace.stench and self.wumpusalive==True):
                    #it only goes in here if the wumpus is still alive
                    if not self.visited(chosenN, newm):
                        self.makeWumpus(chosenN, newm)

                        #make an action to turn towards wumpus and kill it
                    if not self.visited(newn, chosenM):
                        self.makeWumpus(newn, chosenM)


    def CornerCheck2(self, chosenN, chosenM):
        """checks which diagonal squares are inbound and visited
        it then compares valid diagonals to itself in order to
        the weakness of corner check is that there are cases when just because the corners are breezes, doesn't mean
        that the square you marked is a pit. it can be a breeze because of another square
        we can ignore this for now but address it by the smart ai

        what we can do to make this program more efficient is to use modifiers for the function

        so do parameters: modifier, and the direction of the two adjacent tiles

        rightup: modifier = (+1, +1)
            so do n modifier and m modifier
        adjacent: 'U', 'R'

        makesafe(currentn, currentm+ m modifier)
        makesafe(currentn + n modifier, m modifier)

        """
        rightup = self.inBounds(chosenN + 1, chosenM+1)
        rightdown = self.inBounds(chosenN + 1, chosenM-1)
        leftup = self.inBounds(chosenN - 1, chosenM+1)
        leftdown = self.inBounds(chosenN - 1, chosenM-1)
        #tempspace = self.ChosenSquare(chosenN, chosenM)

        if rightup:
            if self.visited(chosenN + 1, chosenM+1):
                self.diagCheck(chosenN, chosenM, 1, 1, 'R', 'U')
        if rightdown:
            if self.visited(chosenN+1, chosenM-1):
                self.diagCheck(chosenN, chosenM, 1, -1, 'R', 'D')
                """ so now im thinking about making the safespace for each square a set
                that way, we can more easily handle repetitive elements"""
        if leftup:
            if self.visited(chosenN-1, chosenM+1):
                self.diagCheck(chosenN, chosenM, -1, 1, 'L', 'U')
        if leftdown:
            if self.visited(chosenN-1, chosenM-1):
                self.diagCheck(chosenN, chosenM, -1, -1, 'L', 'D')


        """
        if wumpus is found, turn towards it and kill it
        then if scream is found, wumpus square will be marked safe
        after that, stench will be treated as a nonfactor"""


    def crossCheck(self):
        """checks adjacent tiles to see if they are marked as safe
        adds them if safety is guaranteed"""
        pass





    def ChosenSquare(self, chosenN, chosenM):
        return self.map[chosenN][chosenM]

    def CurrentSquare(self):
        return self.map[self.n][self.m]

    def rotate(self, direction):
        if direction=='L':
            newdindex = (self.dindex-1)%4
            self.direction=self.directions[newdindex]
            self.dindex = newdindex
        elif direction=='R':
            newdindex = (self.dindex+1)%4
            self.direction = self.directions[newdindex]
            self.dindex = newdindex


    def GoForward(self):
        if self.direction=='U':
            self.m +=1
        elif self.direction=='R':
            self.n+=1
        elif self.direction=='L':
            self.n-=1
        else:
            self.m-=1
        n = self.n
        m = self.m
        if self.inBounds(n, m):
            if not self.visited(n, m):
                 self.visit(n, m)
                # self.map[self.n][self.m].prev = self.getOpposite()

    def PerformAction(self, dir):
        if dir=='U':
            self.UpActions()
        if dir=='D':
            self.DownActions()
        elif dir=='L':
            self.LeftActions()
        elif dir=='R':
            self.RightActions()


    def UpActions(self):
        if self.direction=='D':
            self.actions += [Agent.Action.TURN_RIGHT, Agent.Action.TURN_RIGHT, Agent.Action.FORWARD]
        elif self.direction=='L':
            self.actions += [Agent.Action.TURN_RIGHT, Agent.Action.FORWARD]
        elif self.direction=='R':
            self.actions += [Agent.Action.TURN_LEFT, Agent.Action.FORWARD]
        if self.direction =='U':
            self.actions.append(Agent.Action.FORWARD)

    def DownActions(self):
        if self.direction=='U':
            self.actions += [Agent.Action.TURN_RIGHT, Agent.Action.TURN_RIGHT, Agent.Action.FORWARD]
        elif self.direction=='R':
            self.actions += [Agent.Action.TURN_RIGHT, Agent.Action.FORWARD]
        elif self.direction=='L':
            self.actions += [Agent.Action.TURN_LEFT, Agent.Action.FORWARD]
        else:
            self.actions.append(Agent.Action.FORWARD)

    def RightActions(self):
        """Adds the actions necessary to go to the right square"""
        if self.direction=='U':
            self.actions += [Agent.Action.TURN_RIGHT, Agent.Action.FORWARD]
        elif self.direction=='L':
            self.actions += [Agent.Action.TURN_RIGHT,Agent.Action.TURN_RIGHT, Agent.Action.FORWARD]
        elif self.direction=='D':
            self.actions += [Agent.Action.TURN_LEFT, Agent.Action.FORWARD]
        else:
            self.actions.append(Agent.Action.FORWARD)

    def LeftActions(self):
        """Adds the actions necessary to go to the left square"""
        if self.direction=='D':
            self.actions += [Agent.Action.TURN_RIGHT, Agent.Action.FORWARD]
        elif self.direction=='R':
            self.actions += [Agent.Action.TURN_RIGHT,Agent.Action.TURN_RIGHT, Agent.Action.FORWARD]
        elif self.direction=='U':
            self.actions += [Agent.Action.TURN_LEFT, Agent.Action.FORWARD]
        else:
            self.actions.append(Agent.Action.FORWARD)

    def getOpposite(self):
        return self.directions[self.dindex+2%4]

    def makePit(self, n, m):
        if not self.map[n][m].pit:
            self.map[n][m].pit = True
            self.pitnumber+=1

    def makeWumpus(self, n, m):
        self.map[n][m] = True


    def addSafeSpaces(self):
        """if you are on a provably safe square, then all valid adjacent tiles will be added
        maybe add variation where this is only for when the square is completely empty
        because this only works when the square is completely empty
        this will basically only be used in the beginning then"""
        if self.inBounds(self.n + 1, self.m):
            # self.safespaces.add((self.n + 1, self.m))
            self.safecounter += 1
            self.map[self.n][self.m].safesplit.add('R')
        if self.inBounds(self.n - 1, self.m):
            #self.safespaces.add((self.n - 1, self.m))
            self.safecounter+=1
            self.map[self.n][self.m].safesplit.add('L')
        if self.inBounds(self.n, self.m + 1):
            #self.safespaces.add((self.n, self.m + 1))
            self.safecounter += 1
            self.map[self.n][self.m].safesplit.add('U')
        if self.inBounds(self.n, self.m - 1):
           # self.safespaces.add((self.n, self.m - 1))
            self.safecounter += 1
            self.map[self.n][self.m].safesplit.add('D')

    def tellNeighbors(self):
        """ basically tells the neighbor squares that this is a safe space"""
        pass

    def makemove(self):
        """this is only called when there are actions in the action list
        it takes the first item out of the list, makes the appropriate alterations, then changes it"""
        next = self.actions.pop(0)
        if next == Agent.Action.TURN_RIGHT:
            self.rotate('R')
        elif next == Agent.Action.TURN_LEFT:
            self.rotate('L')
        elif next == Agent.Action.FORWARD:
            self.GoForward()
        return next

    def reverseVar(self):
        """called when bump is detected
        places the state marker back to the previous tile"""
        if self.direction=='D':
            self.m+=1
            self.maxm = self.m
        elif self.direction=='L':
            self.n +=1
            self.maxn = self.n
        elif self.direction=='R':
            self.n -=1
        if self.direction =='U':
            self.m-=1


    # testindex = 0
    # testactions = [Agent.Action.TURN_RIGHT, Agent.TURN_RIGHT, Agent.TURN_RIGHT, Agent.TURN_RIGHT, Agent.TURN_LEFT]
    #




#each action is a boolean
    def getAction( self, stench, breeze, glitter, bump, scream ):
        # print(" CURRENT M is" + str(self.m))
        # print(" CURRENT N is" + str(self.n))
        # print("CURRENT DIRECTION IS: " + self.direction)
        if self.actions:
            #when you perform an action, you should change the state depending on what you have
            # next = self.actions.pop(0)
            return self.makemove()
        tempsquare = self.map[self.n][self.m]
        visited = self.visited(self.n, self.m)


        #this one is undeniably safe
        if bump:
            if self.direction is 'R':
                maxn = self.n-1
            elif self.direction is 'U':
                maxm = self.m-1
            self.reverseVar()
            if not self.map[self.n][self.m].safesplit:
                self.LeftActions()
                return self.makemove()
        if not (stench or breeze or glitter or bump or scream):
            # print("This square is safe")
            # if not visited:
            #     self.visit(self.n, self.m)
            #     self.map[self.n][self.m].safe = True
            #     self.addSafeSpaces()
            self.GoForward()
            return Agent.Action.FORWARD
        if glitter and not self.goldfound:
            self.goldfound= True
            return Agent.Action.GRAB
        else:
            if self.n==0 and self.m==0:
                # print("HALLOWEEEEEN")
                return Agent.Action.CLIMB
            self.LeftActions()
            return self.makemove()



        """
        if tempsquare.safesplit:
            pop out a safe action
            then add it to action queue
            reduce safe counter
        else:
            go to previous square
            
        """


        #this one is undeniably safe
        # if not (stench or breeze or glitter or bump or scream):
        #     print("This square is safe")
        #     if not visited:
        #         self.visit(self.n, self.m)
        #         self.map[self.n][self.m].safe = True
        #         self.addSafeSpaces()
        #     self.GoForward()
        #     return Agent.Action.FORWARD
        # else:
        #     return Agent.Action.FORWARD

            # if self.n==0 and self.m==0:
            #     return Agent.Action.CLIMB
            # self.LeftActions()

        """
        #this is would be a very minimal AI because it exits at the slightest sign of danger
        if self.vcount == 0 and (stench or breeze):
            print("first square is not safe, leaving now")
            self.getout=True
            return Agent.Action.CLIMB
        if scream:
            self.wumpusalive=False
        if self.getout:
            if self.m == 0 and self.n == 0:
                print("got out")
                return Agent.Action.CLIMB
            self.PerformAction(tempsquare.prev)
            #go towards the last known path towards the entrance

        if glitter:
            self.goldfound = True
            self.getout = True
            return Agent.Action.GRAB
        if bump:
            self.reverseVar()

            #choose the next safest option
        if tempsquare.safesplit:
            self.safecounter-=1
            self.PerformAction(self.map[self.n][self.m].safesplit.pop())
        else:
            self.PerformAction(tempsquare.prev)
            
            """

        """
        if bump:
            go back to the previous square
            return one of the m or n values to the value that it was before
                //you don't need to do any actual actions
                //just change the class variable of n or m  
                
        if there's no safe spaces where the agent can go from a certain square
            go to previous space until it finds the a square with a safe space
            
        
        if wumpus is killed, turn that square to safe
        """







        # if tempsquare.safe and not visited:
        #     self.map[self.n][self.m].safe = True
        #     #add adjacent in bound spaces to safe spaces
        #     #remember to remove those items after you have visited
        #     #look at the other options available
        # if breeze:
        #     #if "safe" not in square
        #         #basically, if the square has not already been provably safe
        #     # map[n+1][m].append("P?")
        #     # map[n][m+1].append("P?")
        #     self.map[self.n + 1][self.m].pit = 2
        #     self.map[self.n][self.m].pit=2
        #     #
        # if stench:
        #     self.map[self.n + 1][self.m].wumpus = 2
        #     self.map[self.n][self.m].wumpus = 2
        # if glitter:
        #     self.map[self.n + 1][self.m].gold = 2
        #     self.map[self.n][self.m].gold = 2




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






    # def CornerCheck(self, chosenN, chosenM):
    #     """Corner check is used when you don't know what's in a square but you know what's directly
    #     above, below, left, or right
    #     so in that case, i should add a clause for visited
    #     """
    #     #if the tile above the square is in bounds
    #     right = self.inBounds(chosenN + 1, chosenM)
    #     left = self.inBounds(chosenN-1, chosenM)
    #     if self.inBounds(chosenN, chosenM+1):
    #         uspace = self.map[chosenN][chosenM+1]
    #         if right:
    #             rspace = self.map[chosenN+1][chosenM]
    #             if not ((rspace.breeze and uspace.breeze) or (rspace.stench and uspace.stench)) and rspace.visited and uspace.visited:
    #                 self.map[chosenN][chosenM].safe = True
    #                 self.safespaces.add(chosenN, chosenM)
    #             else:
    #                 if rspace.breeze and uspace.breeze:
    #                     self.map[chosenN][chosenM].pit+=2
    #                 if rspace.stench and uspace.stench:
    #                     self.map[chosenN][chosenM].wumpus+=2
    #             # if rspace.glitter and uspace.glitter:
    #             #     self.map[chosenN][chosenM].gold+=2
    #             #     self.goldfound = True
    #         if left:
    #             lspace = self.map[chosenN - 1][chosenM]
    #             if not ((lspace.breeze and uspace.breeze) or (lspace.stench and uspace.stench)) and lspace.visited and uspace.visited:
    #                 self.map[chosenN][chosenM].safe = True
    #                 self.safespaces.add(chosenN, chosenM)
    #             else:
    #                 if lspace.breeze and uspace.breeze:
    #                     self.map[chosenN][chosenM].pit += 2
    #                 if lspace.stench and uspace.stench:
    #                     self.map[chosenN][chosenM].wumpus += 2
    #             # if lspace.glitter and uspace.glitter:
    #             #     self.map[chosenN][chosenM].gold += 2
    #             #     self.goldfound = True
    #     if self.inBounds(chosenN, chosenM-1):
    #         dspace = self.map[chosenN][chosenM - 1]
    #         if right:
    #             rspace = self.map[chosenN + 1][chosenM]
    #             if not ((rspace.breeze and dspace.breeze) or (rspace.stench and dspace.stench)) and rspace.visited and dspace.visited:
    #                 self.map[chosenN][chosenM].safe = True
    #                 self.safespaces.add(chosenN, chosenM)
    #             else:
    #                 if rspace.breeze and dspace.breeze:
    #                     self.map[chosenN][chosenM].pit += 2
    #                 if rspace.stench and dspace.stench:
    #                     self.map[chosenN][chosenM].wumpus += 2
    #             # if rspace.glitter and dspace.glitter:
    #             #     self.map[chosenN][chosenM].gold += 2
    #             #     self.goldfound = True
    #         if left:
    #             lspace = self.map[chosenN - 1][chosenM]
    #             if not ((lspace.breeze and dspace.breeze) or (lspace.stench and dspace.stench)) and lspace.visited and dspace.visited:
    #                 self.map[chosenN][chosenM].safe = True
    #                 self.safespaces.add(chosenN, chosenM)
    #             else:
    #                 if lspace.breeze and dspace.breeze:
    #                     self.map[chosenN][chosenM].pit += 2
    #                 if lspace.stench and dspace.stench:
    #                     self.map[chosenN][chosenM].wumpus += 2
    #             #so take out all the glitters. noa djacent space will have glitter
    #             # if lspace.glitter and dspace.glitter:
    #             #     self.map[chosenN][chosenM].gold += 2
    #             #     self.goldfound = True
    #     return
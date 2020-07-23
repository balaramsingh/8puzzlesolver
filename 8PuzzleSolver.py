from queue import PriorityQueue
from copy import copy, deepcopy

# the function required to print the state of puzzle in an understandable way
# input parameters
# var : inlist ->  the state required to print
# no output parameters
def good_print(inlist):
    for i in range(3):
        for j in range(3):
            print(inlist[i][j],end =' ')
        print()

# The function returns the index of a specific tile from the given current state
# input parameters
# var : inlist -> the current state
# var : num -> the number whose index we need
# output parameters
# var : a -> a 2 element list which has the required co-ordinates  
def giveindex(inlist,num):
    a = []
    for i in range(3):
        for j in range(3):
            if inlist[i][j] == num :
                a.append(i)
                a.append(j)
                return a
    return a

# function gives the heuristic value of current state . Here the heuristic is Manhattan distance
# input parameters
# var : inlist -> the current state
# var : goallist -> the final state
# output parameters
# var : h -> the calculated heuristic value
def giveheuristic(inlist,goalstate):
    h= 0
    for i in range(9):
        a = giveindex(inlist,i)
        b = giveindex(goallist,i)
        h = h + abs(a[0] - b[0]) + abs(a[1] - b[1])
    return h

# function creates a new node 
# each node means the current state and new state visited
def createnode(parent,inlist,goallist):
    # print("Called createnode")
    li = []
    li.append(parent)
    li.append(inlist)
    return li

# The function takes the runtime input, arranges the variables and returns as a game state
# no input parameters
# output parameters
# var : a -> ( 2D array of dimensions 3x3 )
def takeinput():
    a = []
    for i in range(3):
        l = list(map(int,input().split(' ')))
        a.append(l)
    return a

# The function which takes the current state and gives us the possible moves 
# input parameters 
# var : inlist -> the current state ( it is a 2-D array 3x3 array )
# output parameters
# var : ans -> has the list of actions applicable from the present state
def possible_actions(inlist):
    ans = []
    zer = giveindex(inlist,0)
    if zer[0] <= 1 :
        ans.append('down')
    if zer[0] >= 1 :
        ans.append('up')
    if zer[1] <= 1 :
        ans.append('right')
    if zer[1] >= 1 :
        ans.append('left')
    return ans

# The function takes the current state and a given action and gives out the new state
# input parameters
# var : inlist -> the current state
# var : action -> the given action
# output parametres
# var : temp -> the new state 

def do_action(inlist,action):
    temp = deepcopy(inlist)
    zer = giveindex(inlist,0) # gets the co-ordinates of zero ( empty tile )
    x = zer[0]
    y = zer[1]
    if action == 'left' :
        temp[x][y-1] , temp[x][y] = temp[x][y] , temp[x][y-1]
    elif action == 'right' :
        temp[x][y+1] , temp[x][y] = temp[x][y] , temp[x][y+1]
    elif action == 'up' :
        temp[x-1][y] , temp[x][y] = temp[x][y] , temp[x-1][y]
    elif action == 'down' :
        temp[x+1][y] , temp[x][y] = temp[x][y] , temp[x+1][y]
    return temp # returns the state after doing an action

# The function which takes the initial state and goal state and prints the path , if a path exists
# input parameters 
# var : inlist -> the initial state ( it is a 2-D array 3x3 array )
# var : goallist -> the final state ( it is a 2-D array 3x3 array )
# var : nodelist -> the list which contains all the nodes created
def find_path(inlist,goallist,nodelist):
    start = [[ 0, 0, 0], [ 0, 0, 0],[ 0, 0, 0]]
    visited = []   # initializing a list : to avoid repetitive visits to an intermediate node
    visited.append(inlist)
    q = PriorityQueue() # initializing an empty Priority Queue ( for A-star Algorithm ) 
    q.put((giveheuristic(inlist,goallist) + 0,inlist,0))
    while not q.empty(): # loop runs until the Queue is empty
        a = q.get()   # pop's the top element of Priority Queue
        path_cost = a[2]
        a = deepcopy(a[1])
        if a == goallist :   # checks for goal state , if it matches , loop breaks
            print("Success")
            break
        actions = possible_actions(a)  # the possible actions from each state are stored in actions variable
        b = deepcopy(a)
        for action in actions:   # iterates through the possible actions
            temp = do_action(b,action)
            if temp not in visited :  # if the next step is not visited , a new node is created and it is also added to priority Queue
                tempnode = createnode(a,temp,goallist)
                nodelist.append(tempnode)
                visited.append(temp)
                q.put((giveheuristic(temp,goallist)+path_cost+1,deepcopy(temp),path_cost+1))
    # Path Back Tracker
    tempz = deepcopy(nodelist[0])
    tempz = deepcopy(tempz[0])
    temp = deepcopy(goallist)
    answer = []
    answer.append(temp)
    flag = 0 # flag variable to continue loop until we find the path
    while flag == 0:
        for nodes in nodelist :
            btemp = deepcopy(nodes[1])
            if btemp == temp :
                if btemp == inlist :
                    print("YESSS")
                    flag = 1 
                temp = deepcopy(nodes[0])
                
                answer.append(temp)
    # reversing the list to print the path in chronological order
    answer.reverse()
    for nodes in answer :
        good_print(nodes)
        print("")
    return nodelist

# main
start = [[ 0, 0, 0], [ 0, 0, 0],[ 0, 0, 0]]   # Null State
print("Print initial state :   ")
inlist = takeinput()     # taking the initial state
print("Print goal state  :  ")
goallist = takeinput()   # taking the required final state
print("-------------------")
nodelist = []
nodelist.append(createnode(start,inlist,goallist)) # initializing the start node
l = find_path(inlist,goallist,nodelist)   # calling the function



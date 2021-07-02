# Derive an optimization formulation for this problem.  [10pts]
# Let's denote map = [4][5]     ---> (4 rows 5 columns) where each memory space contains the integer of the department number
# [ i ] [ j ]
# department position number  = i * 5 + j
# distance = [20][20] which takes this information from the csv file.  [ i ][ j ]. where i denotes the start position and j denotes the destination position. It is a 20 by 20 matrix that maps the distance costs from spot 1 on the table in the question provided, to the spot 2 on the table that is provided in the question. 
# flow = [20][20] which takes this information from the csv file.  [ i ][ j ]. where i defines the starting department number, and j defines the destination department number.
# We must optimize min(c) = (product of sums of all costs and distances from one department to all other departments, repeated for each department)
import random
import csv
import copy

from numpy.lib.nanfunctions import _divide_by_count

file = open('Distance.csv')
distance =  list(csv.reader(file))
file = open('Flow.csv')
flow =  list(csv.reader(file))
file = open('Map.csv')
map =  list(csv.reader(file))


def cost(path,flow,distance):
    cost = 0
    for i in range(len(path)):
        current = int(path[i])-1
        for j in range(len(path)):
            compare = int(path[j])-1
            cost += int(distance[i][j])*int(flow[current][compare])
    return cost

def findNeighbors(current, tabu,threshold = None):
    # neighbors [array of neighbor]
    # neighbor 
    neighbors = []
    k = 0
    for i in range(len(tabu)):
        for j in range(len(tabu[i])):
            if tabu[i][j] == 0:
                neighbor = copy.deepcopy(current)
                neighbor[i] = current[j+i+1]
                neighbor[j+i+1] = current[i]
                neighbor = [neighbor,(i,j)] # the second value tells us which indexes were swapped
                neighbors.append(neighbor)
                k += 1
            if threshold and k == threshold: 
                return neighbors 
    return neighbors

def decreaseTabu(tabu):
    for i in range(len(tabu)):
        for j in range(len(tabu[i])):
            tabu[i][j] = max(tabu[i][j]-1, 0)
    return

def printNe(neigh):
    for row in neigh:
        print(row, " /n")

def solve( map, flow, distance, allowedIterations, threshold = None, tenure = 3): 
    # map is the current solution
    # threshold decides how many neighbors we check
    # allowedIterations is used for termination
    # this def takes the map, 
    # finds 190 neighbors, checking the tabu list to ensure we do not repeat previous sol
    frequency = 5 # lets update the dynamic tenure every 5 iterations
    f = 0
    tabu_dynamic = random.randint(1, 100)
    tabu_start = tenure
    current = map
    lowestCost = cost(current,flow,distance)
    # print("Initial Solution : ", current, "\n", "Cost: ",lowestCost)
    tabu = []
    for i in range(len(map)-1):
        row = []
        for j in range(i+1,len(map)):
            row.append(0)
        tabu.append(row)
    for i in range(allowedIterations):
        decendent = None
        # decrement the tableau
        decreaseTabu(tabu)
        # find neighbors
        neighbors = findNeighbors(current,tabu,threshold)
  
        # for each neighbor calculate the cost
        for neighbor in neighbors:
            cur_cost = cost(neighbor[0],flow,distance)
            if cur_cost == 2570: 
                print("Iterations: ", i)
                return neighbor[0], cur_cost # if the cost is less than or equal too 2570  (the specified goal) return this solution
            if cur_cost <= lowestCost :   # save least neighbor as the current solution
                current = neighbor[0]
                lowestCost = cur_cost
                decendent = neighbor[1] # coordinates
        # if no neighbor improves the solution, than return last solution
        if decendent == None:
            print("Iterations: ", i)
            return current, lowestCost
        # update the swap in the tableu
        if tabu_start == "Dynamic":
            if f == frequency:
                tabu_dynamic = random.randint(1, 20)
                f = 0
            tabu[decendent[0]][decendent[1]] = tabu_dynamic
            f += 1
        else: 
            tabu[decendent[0]][decendent[1]] = tabu_start 
    
    # after all of the interations we still have not found the most optimal solution. 
    # Lets just return the solution that we found anyways
    print("Iterations: ", allowedIterations )
    return current,lowestCost

def solveFrequency( map, flow, distance, allowedIterations, threshold = None, tenure = 3): 
    # map is the current solution
    # threshold decides how many neighbors we check
    # allowedIterations is used for termination
    # this def takes the map, 
    # finds 190 neighbors, checking the tabu list to ensure we do not repeat previous sol
    frequency = 5 # lets update the dynamic tenure every 5 iterations
    f = 0
    tabu_dynamic = random.randint(1, 100)
    tabu_start = tenure
    current = map
    lowestCost = cost(current,flow,distance)
    # print("Initial Solution : ", current, "\n", "Cost: ",lowestCost)
    tabu = []
    for i in range(len(map)):
        row = []
        for j in range(i+1,len(map)):
            row.append(0)
        tabu.append(row)

    for i in range(allowedIterations):
        decendent = None
        # decrement the tableau
        decreaseTabu(tabu)
        # find neighbors
        neighbors = findNeighbors(current,tabu,threshold)
  
        # for each neighbor calculate the cost
        for neighbor in neighbors:
            cur_cost = cost(neighbor[0],flow,distance)
            if cur_cost == 2570: 
                print("Iterations: ", i)
                return neighbor[0], cur_cost # if the cost is less than or equal too 2570  (the specified goal) return this solution
            if cur_cost <= lowestCost :   # save least neighbor as the current solution
                current = neighbor[0]
                lowestCost = cur_cost
                decendent = neighbor[1] # coordinates
        # if no neighbor improves the solution, than return last solution
        if decendent == None:
            print("Iterations: ", i)
            return current, lowestCost
        # update the swap in the tableu
        if tabu_start == "Dynamic":
            if f == frequency:
                tabu_dynamic = random.randint(1, 20)
                f = 0
            tabu[decendent[0]][decendent[1]] = tabu_dynamic
            tabu[decendent[1]][decendent[0]] = tabu_dynamic
            f += 1
        else: 
            tabu[decendent[0]][decendent[1]] = tabu_start 
            tabu[decendent[1]][decendent[0]] = tabu_start 
    
    # after all of the interations we still have not found the most optimal solution. 
    # Lets just return the solution that we found anyways
    print("Iterations: ", allowedIterations )
    return current,lowestCost

def Experiment1():
    print("Test #1: Basic configuration provided by the question \n")
    current,lowestCost = solve(map[0],flow,distance=distance,allowedIterations=100)
    print("Solution : ", current, "\n", "Cost: ", lowestCost)

    print("Experiment #1: 20 random initial configurations \n")

    for i in range(20):
        random.shuffle(map[0])
        print("Test ",i, " : \n")
        current,lowestCost = solve(map[0],flow,distance=distance,allowedIterations=100)
        print("Solution : ", current, "\n", "Cost: ", lowestCost, "\n")

def Experiment2():
    print("Experiment #2: tabu size adjustment \n")
    print("Tenure 1 "," :")
    current,lowestCost = solve(map[0],flow,distance=distance,allowedIterations=100,tenure=1)
    print("Solution : ", current, "\n", "Cost: ", lowestCost)
    print("\n")

    print("Tenure 3 "," :")
    current,lowestCost = solve(map[0],flow,distance=distance,allowedIterations=100,tenure=3)
    print("Solution : ", current, "\n", "Cost: ", lowestCost)
    print("\n")

    print("Tenure 5 "," :")
    current,lowestCost = solve(map[0],flow,distance=distance,allowedIterations=100,tenure=5)
    print("Solution : ", current, "\n", "Cost: ", lowestCost)
    print("\n")
    
    print("Tenure 20 "," :")
    current,lowestCost = solve(map[0],flow,distance=distance,allowedIterations=100,tenure=20)
    print("Solution : ", current, "\n", "Cost: ", lowestCost)
    print("\n")

    #test with the optimal initial input

    sol = ['12', '4', '10', '5', '11', '20', '9', '6', '15', '19', '3', '16', '17', '2', '18', '7', '8', '14', '13', '1'] 
    print("Tenure 1 "," :")
    current,lowestCost = solve(sol,flow,distance=distance,allowedIterations=100,tenure=1)
    print("Solution : ", current, "\n", "Cost: ", lowestCost)
    print("\n")

    print("Tenure 3 "," :")
    current,lowestCost = solve(sol,flow,distance=distance,allowedIterations=100,tenure=3)
    print("Solution : ", current, "\n", "Cost: ", lowestCost)
    print("\n")
    
    print("Tenure 20 "," :")
    current,lowestCost = solve(sol,flow,distance=distance,allowedIterations=100,tenure=20)
    print("Solution : ", current, "\n", "Cost: ", lowestCost)
    print("\n")

def Experiment3():
    print("Experiment #3: tabu dynamic size \n")

    print("Tenure 1 "," :")
    current,lowestCost = solve(map[0],flow,distance=distance,allowedIterations=100,threshold=190/2,tenure=1)
    print("Solution : ", current, "\n", "Cost: ", lowestCost)
    print("\n")

    print("Tenure 3 "," :")
    current,lowestCost = solve(map[0],flow,distance=distance,allowedIterations=100,threshold=190/2,tenure=3)
    print("Solution : ", current, "\n", "Cost: ", lowestCost)
    print("\n")

    print("Tenure 5 "," :")
    current,lowestCost = solve(map[0],flow,distance=distance,allowedIterations=100,threshold=190/2,tenure=5)
    print("Solution : ", current, "\n", "Cost: ", lowestCost)
    print("\n")
    
    print("Tenure 20 "," :")
    current,lowestCost = solve(map[0],flow,distance=distance,allowedIterations=100,threshold=190/2,tenure=20)
    print("Solution : ", current, "\n", "Cost: ", lowestCost)
    print("\n")

    print("Tenure Dynamic  "," :")
    current,lowestCost = solve(map[0],flow,distance=distance,allowedIterations=100,threshold=190/2,tenure="Dynamic")
    print("Solution : ", current, "\n", "Cost: ", lowestCost)
    print("\n")

def Experiment4():
    print("Experiment #4: Aspiration Critera \n")
    # we will run a loop of 20 random starting sol, and select the solution with the least cost found
    # this critera may not be complete and we may not find the optimal solution
    print("Run Loop with 20 random solutions:\n")
    min = 4000 
    best = None
    for i in range(20):
        random.shuffle(map[0])
        #consider all neighbors, allow only 25 iterations, and 3 tenure
        current,lowestCost = solve(map[0],flow,distance=distance,allowedIterations=25)
        if(lowestCost < min):
            min = lowestCost
            best = current
        if lowestCost == 2570:
            break
    print("Solution : ", best, "\n", "Cost: ", min, "\n")

    # we will run a loop solving for a random initial solution until we find the optimal path. We know before hand that 2570 is the optimal cost
    # this critera will be complete since we already know that in the past we have found the optimal solution.

    print("Run Loop until optimal :\n")
    min = 4000 
    best = None
    maps = set()
    while(min != 2570):
        random.shuffle(map[0])
        #consider all neighbors, allow only 25 iterations, and 3 tenure
        current,lowestCost = solve(map[0],flow,distance=distance,allowedIterations=25)
        if(lowestCost < min):
            min = lowestCost
            best = current
        if lowestCost == 2570:
            break
    print("Solution : ", best, "\n", "Cost: ", min, "\n")

def Experiment5():
    print("Test #5: Frequency Tabu\n")

# Experiment1()
# Experiment2()
# Experiment3()
Experiment2()
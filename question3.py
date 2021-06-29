# Derive an optimization formulation for this problem.  [10pts]
# Let's denote map = [4][5]     ---> (4 rows 5 columns) where each memory space contains the integer of the department number
# [ i ] [ j ]
# department position number  = i * 5 + j
# distance = [20][20] which takes this information from the csv file.  [ i ][ j ]. where i denotes the start position and j denotes the destination position. It is a 20 by 20 matrix that maps the distance costs from spot 1 on the table in the question provided, to the spot 2 on the table that is provided in the question. 
# flow = [20][20] which takes this information from the csv file.  [ i ][ j ]. where i defines the starting department number, and j defines the destination department number.
# We must optimize min(c) = (product of sums of all costs and distances from one department to all other departments, repeated for each department)

import csv
file = open('Distance.csv')
distance =  list(csv.reader(file))

file = open('Flow.csv')
flow =  list(csv.reader(file))

file = open('Map.csv')
map =  list(csv.reader(file))
cost = 0
for i in len(map):
    for j in len(map[i]):
        current_pos = map[i][j]
        current_spot = i * len(map[i]) + j
        # current_pos = (i,j)
        if(j < len(map[i]) - 1 ):
            for k in range(i,len(map)):
                for l in range(j+1,len(map[i])):
                    compare_pos = map[k][l]
                    compare_spot = k * len(map[i]) + l
                    c_flow = flow[current_pos-1][compare_pos-1]
                    c_dist = distance[current_spot][current_pos]
                    cost += c_flow * c_dist


        #distance 





# provided a solution of all departments and there locations in a 2 d array

# i.e 4x4

# A = 
#  [1,2,3,4]
#  [5,6,7,8]
#  [9,10,11,12]
#  [13,14,15,16]

# D = [i][j]




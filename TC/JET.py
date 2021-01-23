import numpy as np
# --- Constants
STONE = '%'
BRICK = '*'
ROPE = '#'
CHAIN = '-'
CHEST = '@'
EMPTY = ' '
# --- Getting input info.
parm = list(map(int,input().split()))
C = parm[0]
R = parm[1]
iX = parm[2]
iY = parm[3]
world = R*[C*[]]
for y in range(R):
    world[y] = list(input())
world = np.transpose(world)
# --- Variables
currentX = iX
currentY = iY
# --- Functions
def isVisible(cell):
	if cell ==  STONE:
		return -1
	elif cell == Br:
		pass
def DFS(iX,iY):           
    visited = []  
    # Create a stack for DFS  
    stack = [] 
    # Push the current source node.  
    stack.append((iX,iY))  
    while (len(stack)):  
    	# Pop a vertex from stack and print it  
	    s = stack.pop() 
        # Stack may contain same vertex twice. So  
        # we need to print the popped item only  
        # if it is not visited.  
        if (not visited[s]):  
            
            visited[s] = True 
		# Get all adjacent vertices of the popped vertex s  
        # If a adjacent has not been visited, then push it  
        # to the stack.  
        for node in self.adj[s]:  
            if (not visited[node]):  
                stack.append(node) 
#--- process
if __name__ == '__main__':
	visited = []

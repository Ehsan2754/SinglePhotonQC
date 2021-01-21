
if __name__ == "__main__":
    N = int(input())
    N_cuts = (N+3)*[0]
    N_cuts[0] = -1
    N_cuts[1] = 0
    N_cuts[2] = 1
    for i in range(3,N+1):
        if i%2 == 1:
            N_cuts[i] = N_cuts[i-1]+1
        else:
            N_cuts[i] = N_cuts[i//2]+1 
    print (N_cuts[N])
  

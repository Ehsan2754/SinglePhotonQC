def newCordination(x,y,shiftRef,vector):
    return(
        round(shiftRef[0]+x*vector[0],4)
        ,
        round(shiftRef[1]+y*vector[1],4)
        )
if __name__ == "__main__":
    x,y = map(float,input().split())
    paper= list(map(float,input().split()))
    vector = (x/(paper[4]-paper[0]),y/(paper[5]-paper[1]))
    shiftRef = (paper[0],paper[1])
    x_d = shiftRef[0]/(1-vector[0])
    y_d = shiftRef[1]/(1-vector[1])
    print(x_d,y_d)
    
  

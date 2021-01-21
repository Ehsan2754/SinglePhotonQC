'''
    heaviside(arg): standard heaviside mathematical function
'''


def heaviside(arg):
    return 1 if arg > 0 else 0


if __name__ == "__main__":
    '''
    data = input numbers of user such that :
    data[0] => A #--- subscription fee
    data[1] => B #--- amount of granted traffic on subscription
    data[2] => C #--- cost of each MB of traffic out of subscription
    data[3] => D #--- total used traffic
    '''
    data = list(map(int, input().split()))
    '''
     TOTAL FEE = (subscription fee) +
     ( 
         heaviside(total used traffic MB - granted traffic in MB)
         *(total used traffic MB - granted traffic in MB)
         * (cost of each MB of traffic out of subscription)
        )
    '''

    print(data[0] + (heaviside(data[3] - data[1])) *
          (data[3] - data[1]) * data[2])

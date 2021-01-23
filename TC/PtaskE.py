if __name__ == "__main__":
    nDay = int(input())
    bill = []
    ticket = []
    totalFee = 0
    for i in range(nDay):
        t = int(input())
        bill.append(t)
        if(t>100):
            ticket.append(i)
    for item in ticket:
        tmp = sorted(bill[item:-1])
        j = 0
        while tmp[-1-j]>100:
            j +=1
        bill[bill.index(tmp[-1-j])+item-1] = 0
    for i in  bill:
        totalFee += i
    print(totalFee)
        

n = 1
flag = 0
result = 0
while True:
    x = n / 6
    y = n / 9
    z = n / 20
    for a in range(x + 1):
        for b in range(y + 1):
            for c in range(z + 1):
                if 6 * a + 9 * b + 20 * c == n:
                    flag = flag + 1
                    print(str(a) + " " + str(b) + " " + str(c) + " " + str(n))
                    if flag == 6:
                        print("biggest number is " + str(result))
                        print(result)
                    else:
                        n = n + 1
                    break
                else:
                    flag = 0;
                    result = n;
            if flag > 0:
                break
        if flag > 0:
            break
    if flag == 6:
        print("End")
        break
    else:
        n = n + 1
    print(n)
                    

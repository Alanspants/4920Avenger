a=["-","-"]
if a[0] != "-":
    if a[0] > 4:
        print("4")
    elif a[1] != "-":
        if a[1] < 6:
            print("6")
        else:
            print("7 pass")
    else:
        print("8 pass")

elif a[1] != "-":
    if a[1] < 6:
        print("9")
    else:
        print("10 pass")

else:
    print("11 pass")

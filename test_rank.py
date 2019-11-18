import operator

temp = {}
temp['Alan'] = 5000
temp['Dolly'] = 4500
temp['Harry'] = 3000

sorted_x = sorted(temp.items(), key=lambda kv: kv[1], reverse=True)
print(temp)
print(sorted_x)
print(sorted_x[0][0])
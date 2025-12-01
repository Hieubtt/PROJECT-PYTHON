letters = ["A", "B", "C", "D"] 

print("List đảo ngược" + str(letters[::-1]))



print("List đảo ngược" + str(letters[-1]+letters[-2]+letters[-3]+letters[-4]))
a=''
for x in reversed(letters):
    a += x   
    print (a)
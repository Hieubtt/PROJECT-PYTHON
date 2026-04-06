n = int(input('Nhập số n : '))
flag=False
dem_so_nguyen_to = 0 
for i in range (1,n):
    if i > 1 :
        flag = True
        for j in range (2,i):
            if i % j == 0:
                flag = False
                break
        if flag == True:
            dem_so_nguyen_to = dem_so_nguyen_to + 1
            print(f'{i} là số nguyên tố')

print(f'Có {dem_so_nguyen_to} số nguyên tố')



        
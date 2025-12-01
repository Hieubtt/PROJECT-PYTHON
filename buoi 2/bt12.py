n = int(input('Nhập số n : '))

print('---------Kết quả------------')
for i in range (1,n+1):
    tong_so_uoc= 0
    for j in range (1,i):
        if i % j == 0:
            tong_so_uoc = tong_so_uoc + j
            
    if tong_so_uoc == i:
        print(f'{i} là số hoan hao')
    
    
    

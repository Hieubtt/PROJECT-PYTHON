dau_vao = int(input('Hãy nhập vào 1 số bất kì :'))
dem_so = 0 
for i in range(1,dau_vao+1):
    if dau_vao % i == 0:
        print(i , 'chia hết cho ',dau_vao)
        dem_so = dem_so + 1
print(f'   {dem_so} chia hết cho {dau_vao}')
    
        
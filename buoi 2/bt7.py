n = int(input('Nhập 1 số nguyên dương : '))
tong_so_le=0

for i in range (1,n):
    if i % 2 != 0 :
        tong_so_le = tong_so_le + 1
print(f'Tổng số lẻ là : {tong_so_le}')
 
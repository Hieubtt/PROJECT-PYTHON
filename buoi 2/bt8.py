n = int(input('Nhập 1 số lượng n : '))
tong_sl_n=0
for i in range (0,n):
    a = int(input(f'Nhập số thứ {i+1} : '))
    tong_sl_n = tong_sl_n + a

print('Tổng của số n đã nhập là : ',tong_sl_n)
n  =  int(input('Hãy nhập số lượng n trong List : '))
so_can_tim = int(input('Nhập số cần tìm : '))
List_number_le = []
List_number_chan = []
for i in range(n):
    number_1 = int(input(f'Nhập số lượng phần tử thứ {i+1}  : '))
    if number_1 % 2 == 0:
        List_number_chan.append(number_1)
    else:
        List_number_le.append(number_1)

List_number_chan.sort()
List_number_le.sort()
print('Danh sách số chẵn là : ',List_number_chan)
print()
print('Danh sách số lẻ là : ',List_number_le)



n  =  int(input('Hãy nhập số lượng n trong List : '))
so_can_tim = int(input('Nhập số cần tìm : '))
List_number = []
for i in range(n):
    number_1 = int(input(f'Nhập số lượng phần tử thứ {i+1}  : '))
    List_number.append(number_1)

count_1 = 0 
for x in List_number:
    if x == so_can_tim:
        count_1 +=1
print(count_1)


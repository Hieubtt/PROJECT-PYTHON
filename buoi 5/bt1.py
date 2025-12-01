n = int(input('Nhập số lượng n : '))
List_number = []

for i in range(n):
    number_1 = int(input(f'Nhập số lượng {n} phần tử'))
    List_number.append(number_1)
print(List_number) 

print('Số tổng trong List là :' ,sum(List_number) )



    
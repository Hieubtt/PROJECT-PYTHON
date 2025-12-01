n  =  int(input('Hãy nhập số lượng n trong List : '))
List_number = []
for i in range(n):
    number_1 = int(input(f'Nhập số lượng phần tử thứ {i+1}  : '))
    List_number.append(number_1)
List_number.reverse()
List_result = List_number
print(List_result)
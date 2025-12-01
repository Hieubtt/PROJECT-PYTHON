n  =  int(input('Hãy nhập số lượng n trong List : '))
List_number = []
for i in range(n):
    number_1 = int(input(f'Nhập số lượng phần tử thứ {i+1}  : '))
    List_number.append(number_1)
List_number.sort(reverse=True)
List_result = List_number[0]
print('Phần tử lớn nhất trong List là : ',List_result)

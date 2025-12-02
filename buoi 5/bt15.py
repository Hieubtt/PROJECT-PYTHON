n = int(input('Nhập vào số lượng phần tử : '))

List_1 = []
for i in range(n):
    number_1 = int(input(f'Nhập vào phần tử thứ {i+1} : '))
    List_1.append(number_1)
print(List_1)
List_result = []
so_tong_check = int(input('Nhập vào 1 số K :'))
for i in range (len(List_1)):  #Lấy giá trị trong List
    for k in range (i+1,len(List_1)):
        if List_1[i]+List_1[k] == so_tong_check:
            List_result.append((List_1[i],List_1[k]))
         
if List_result:
    for a in List_result: #Lấy phần tử trong List
        print(f'Các cặp số có tổng = {so_tong_check} : {a}')            
else:
    print('Không tìm thấy cặp số nào.!')



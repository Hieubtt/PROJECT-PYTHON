n = int(input('Hãy nhập số lượng n : '))
Set_so_nguyen = set()
for i in range(n):
    number_so_nguyen = int(input(f'Nhập số lượng phần tử thứ {i+1} : '))
    
    Set_so_nguyen.add(number_so_nguyen)
List_so_nguyen = list(Set_so_nguyen)
print('Danh sách sau khi loại bỏ trùng lặp: ',List_so_nguyen)
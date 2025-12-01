data = [1, 2, 2, 3, 4, 4, 5]  

list_ko_trung = []

[list_ko_trung.append(i) for i in data if i not in list_ko_trung]
print(list_ko_trung)
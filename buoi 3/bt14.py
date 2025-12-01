text = "Hello Python"


list_new = list(text)

dem_tong = 0
for i in list_new:
    if i == 'o':
        dem_tong +=1

print(dem_tong)
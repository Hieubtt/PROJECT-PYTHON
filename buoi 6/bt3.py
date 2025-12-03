def dem_tu(chuoi):
    cac_tu = chuoi.split()
    so_tu = len(cac_tu)
    return f"Số từ trong chuỗi: {so_tu}"
chuoi="Python là ngôn ngữ lập trình thú vị"    
cac_tu = chuoi.split()
so_tu = len(cac_tu)
print (f"Số từ trong chuỗi: {cac_tu}")
print(dem_tu("Python là ngôn ngữ lập trình thú vị"))

        
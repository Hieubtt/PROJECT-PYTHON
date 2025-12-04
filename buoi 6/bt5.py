def tim_so_nho_nhat(ds):
    so_nho_nhat=0
    for i in range(len(ds)):
        for j in range (i+1,len(ds)):
            if ds[i] < ds[j]:
                so_nho_nhat = ds[i]
            else:
                so_nho_nhat = ds[j]
    return so_nho_nhat


print(f'Số nhỏ nhất trong danh sách cần tìm là : {tim_so_nho_nhat([2,45,6,7,8,89,0,-1,2,-9])}')
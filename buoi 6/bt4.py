def tim_so_lon_nhat(ds):
    #ds=[]
    so_lon_nhat = 0
    for i in  range(len(ds)):
        for j in range(i+1,len(ds)):
            if ds[i] > ds[j] :
                so_lon_nhat = ds[i]
            else:
                so_lon_nhat = ds[j]
    return so_lon_nhat


print('Số lớn nhất trong danh sách là : ',tim_so_lon_nhat([100,22,38,43,54,556]))

        
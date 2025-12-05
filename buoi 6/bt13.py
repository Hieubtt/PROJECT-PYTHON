def dem_tu(ds):
    dict_ds = {}
    ds = ds.strip().replace(',', '').replace('!', '').replace('.', '').replace(' ','')
    ds = ds.lower()
    ds_list = list(ds)
    #print(ds_list)

    for x in ds_list:
        dict_ds[x] = dict_ds.get(x,0)+1
    
    return dict_ds
print(dem_tu("Hello world! Hello Python. Python is great, Python is fun."))
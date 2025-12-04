def tinh_so_nguyen_to(x):
    try:
        x=int(x)
    except TypeError:
        raise TypeError('Nhập sai kiểu dữ liệu !')
    else : 
        if x <= 1 :
            return f'{x} không phải là số nguyên tố'
        else:
            for i in range(2,x):
                if x % i == 0:
                    return f'{x} không phải là số nguyên tố'
            return f'{x} là số nguyên tố'



print(tinh_so_nguyen_to(11))




        
